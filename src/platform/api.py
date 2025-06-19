"""API routes for the Mathematics-Based Coding AZ platform."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import asyncio
import json

from .database import get_db
from .models import User, Challenge as ChallengeModel, Submission
from src.core.challenge import ChallengeResult
from src.core.failure_analysis import FailureAnalyzer
from src.assessment.scoring import ScoringEngine
from src.validation.task_validator import TaskValidator
from src.challenges.level1.number_theory import RSAChallenge, ModularExponentiationChallenge


# Pydantic models for API
class SubmissionCreate(BaseModel):
    challenge_id: int
    code: str
    mathematical_reasoning: str = ""


class SubmissionResponse(BaseModel):
    id: int
    challenge_id: int
    passed: bool
    total_score: float
    feedback: dict
    attempt_number: int
    
    class Config:
        from_attributes = True


class ChallengeResponse(BaseModel):
    id: int
    title: str
    description: str
    level: str
    domain: str
    time_limit: float
    difficulty_score: float
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    username: str
    full_name: Optional[str]
    current_level: str
    mathematics_score: float
    coding_score: float
    innovation_score: float
    
    class Config:
        from_attributes = True


# Initialize routers
challenge_router = APIRouter()
submission_router = APIRouter()
user_router = APIRouter()

# Initialize services
failure_analyzer = FailureAnalyzer()
scoring_engine = ScoringEngine()
task_validator = TaskValidator()

# Available challenges (in a real system, these would be loaded from database)
AVAILABLE_CHALLENGES = {
    "rsa": RSAChallenge(),
    "modular_exp": ModularExponentiationChallenge()
}


@challenge_router.get("/", response_model=List[ChallengeResponse])
async def list_challenges(
    level: Optional[str] = None,
    domain: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List available challenges with optional filtering."""
    query = db.query(ChallengeModel)
    
    if level:
        query = query.filter(ChallengeModel.level == level)
    if domain:
        query = query.filter(ChallengeModel.domain == domain)
    
    challenges = query.all()
    
    # If no challenges in database, return sample challenges
    if not challenges:
        sample_challenges = []
        for i, (key, challenge) in enumerate(AVAILABLE_CHALLENGES.items()):
            sample_challenges.append(ChallengeResponse(
                id=i + 1,
                title=challenge.title,
                description=challenge.description,
                level=challenge.level.value,
                domain=challenge.domain.value,
                time_limit=challenge.time_limit,
                difficulty_score=0.7
            ))
        return sample_challenges
    
    return challenges


@challenge_router.get("/{challenge_id}", response_model=ChallengeResponse)
async def get_challenge(challenge_id: int, db: Session = Depends(get_db)):
    """Get a specific challenge by ID."""
    challenge = db.query(ChallengeModel).filter(ChallengeModel.id == challenge_id).first()
    
    if not challenge:
        # Return sample challenge if not in database
        if challenge_id <= len(AVAILABLE_CHALLENGES):
            key = list(AVAILABLE_CHALLENGES.keys())[challenge_id - 1]
            sample_challenge = AVAILABLE_CHALLENGES[key]
            return ChallengeResponse(
                id=challenge_id,
                title=sample_challenge.title,
                description=sample_challenge.description,
                level=sample_challenge.level.value,
                domain=sample_challenge.domain.value,
                time_limit=sample_challenge.time_limit,
                difficulty_score=0.7
            )
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    return challenge


@challenge_router.get("/{challenge_id}/details")
async def get_challenge_details(challenge_id: int):
    """Get detailed challenge information including requirements and test cases."""
    if challenge_id <= len(AVAILABLE_CHALLENGES):
        key = list(AVAILABLE_CHALLENGES.keys())[challenge_id - 1]
        challenge = AVAILABLE_CHALLENGES[key]
        
        return {
            "id": challenge_id,
            "title": challenge.title,
            "description": challenge.description,
            "level": challenge.level.value,
            "domain": challenge.domain.value,
            "mathematical_requirements": [
                {
                    "concept": req.concept,
                    "description": req.description,
                    "proof_required": req.proof_required,
                    "complexity_analysis": req.complexity_analysis
                }
                for req in challenge.mathematical_requirements
            ],
            "time_limit": challenge.time_limit,
            "example_test_cases": len(challenge.test_cases)
        }
    
    raise HTTPException(status_code=404, detail="Challenge not found")


@submission_router.post("/", response_model=SubmissionResponse)
async def submit_solution(
    submission: SubmissionCreate,
    user_id: int = 1,  # Hardcoded for demo - would come from auth
    db: Session = Depends(get_db)
):
    """Submit a solution for evaluation."""
    
    # Get challenge
    if submission.challenge_id > len(AVAILABLE_CHALLENGES):
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    key = list(AVAILABLE_CHALLENGES.keys())[submission.challenge_id - 1]
    challenge = AVAILABLE_CHALLENGES[key]
    
    # Count previous attempts
    attempt_number = db.query(Submission).filter(
        Submission.challenge_id == submission.challenge_id,
        Submission.user_id == user_id
    ).count() + 1
    
    try:
        # Execute the user's code safely (this is a simplified version)
        # In production, this would need proper sandboxing
        result = await evaluate_submission_safely(
            submission.code, 
            challenge,
            submission.mathematical_reasoning
        )
        
        # Calculate comprehensive score
        detailed_score = scoring_engine.calculate_comprehensive_score(
            result, 
            submission.code, 
            submission.mathematical_reasoning,
            []  # Would include attempt history
        )
        
        # Analyze failure if not passed
        failure_analysis = None
        if not result.passed:
            failure_analysis = failure_analyzer.analyze_failure(
                submission.code,
                result,
                {
                    'domain': challenge.domain.value,
                    'level': challenge.level.value
                },
                str(user_id),
                attempt_number
            )
        
        # Create submission record
        db_submission = Submission(
            user_id=user_id,
            challenge_id=submission.challenge_id,
            code=submission.code,
            mathematical_reasoning=submission.mathematical_reasoning,
            attempt_number=attempt_number,
            passed=result.passed,
            functional_score=detailed_score.criteria_scores.get("functional_correctness", 0.0),
            mathematical_score=detailed_score.criteria_scores.get("mathematical_rigor", 0.0),
            code_quality_score=detailed_score.criteria_scores.get("code_quality", 0.0),
            innovation_score=detailed_score.criteria_scores.get("innovation", 0.0),
            total_score=detailed_score.adjusted_score,
            test_results={"results": "test_data"},  # Simplified
            feedback={
                "detailed_score": {
                    "criteria_scores": {k.value: v for k, v in detailed_score.criteria_scores.items()},
                    "strengths": detailed_score.strengths,
                    "improvement_areas": detailed_score.improvement_areas,
                    "feedback": detailed_score.feedback
                },
                "failure_analysis": failure_analysis
            }
        )
        
        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)
        
        return SubmissionResponse(
            id=db_submission.id,
            challenge_id=db_submission.challenge_id,
            passed=db_submission.passed,
            total_score=db_submission.total_score,
            feedback=db_submission.feedback,
            attempt_number=db_submission.attempt_number
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Error evaluating submission: {str(e)}"
        )


async def evaluate_submission_safely(code: str, challenge, reasoning: str) -> ChallengeResult:
    """Safely evaluate a code submission."""
    # This is a simplified evaluation - in production would need proper sandboxing
    try:
        # Create a safe execution environment
        safe_globals = {
            '__builtins__': {
                'abs': abs, 'all': all, 'any': any, 'bin': bin, 'bool': bool,
                'bytearray': bytearray, 'bytes': bytes, 'chr': chr, 'dict': dict,
                'enumerate': enumerate, 'filter': filter, 'float': float,
                'frozenset': frozenset, 'getattr': getattr, 'hasattr': hasattr,
                'hash': hash, 'hex': hex, 'int': int, 'isinstance': isinstance,
                'iter': iter, 'len': len, 'list': list, 'map': map, 'max': max,
                'min': min, 'next': next, 'oct': oct, 'ord': ord, 'pow': pow,
                'range': range, 'repr': repr, 'reversed': reversed, 'round': round,
                'set': set, 'slice': slice, 'sorted': sorted, 'str': str,
                'sum': sum, 'tuple': tuple, 'type': type, 'zip': zip
            }
        }
        
        # Execute the code
        exec(code, safe_globals)
        
        # For now, return a mock successful result
        # In a real implementation, this would run the actual tests
        return ChallengeResult(
            passed=True,
            test_results=[],
            mathematical_score=0.8,
            code_quality_score=0.7,
            innovation_score=0.6,
            total_score=0.75,
            feedback="Mock evaluation - code executed successfully",
            errors=[]
        )
        
    except SyntaxError as e:
        return ChallengeResult(
            passed=False,
            test_results=[],
            mathematical_score=0.0,
            code_quality_score=0.0,
            innovation_score=0.0,
            total_score=0.0,
            feedback=f"Syntax error: {str(e)}",
            errors=[str(e)]
        )
    except Exception as e:
        return ChallengeResult(
            passed=False,
            test_results=[],
            mathematical_score=0.0,
            code_quality_score=0.0,
            innovation_score=0.0,
            total_score=0.0,
            feedback=f"Runtime error: {str(e)}",
            errors=[str(e)]
        )


@submission_router.get("/{submission_id}", response_model=SubmissionResponse)
async def get_submission(submission_id: int, db: Session = Depends(get_db)):
    """Get a specific submission by ID."""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return submission


@submission_router.get("/")
async def list_submissions(
    user_id: Optional[int] = None,
    challenge_id: Optional[int] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List submissions with optional filtering."""
    query = db.query(Submission)
    
    if user_id:
        query = query.filter(Submission.user_id == user_id)
    if challenge_id:
        query = query.filter(Submission.challenge_id == challenge_id)
    
    submissions = query.limit(limit).all()
    return submissions


@submission_router.post("/{submission_id}/validate-advanced")
async def validate_submission_detailed(submission_id: int, db: Session = Depends(get_db)):
    """Enhanced validation using TaskValidator for comprehensive mathematical analysis."""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Create a submission-like object for the validator
    class SubmissionWrapper:
        def __init__(self, code: str, reasoning: str):
            self.code = code
            self.mathematical_reasoning = reasoning
    
    wrapper = SubmissionWrapper(submission.code, submission.mathematical_reasoning or "")
    
    # Run comprehensive validation
    result = task_validator.validate_mathematical_correctness(wrapper)
    
    return {
        "submission_id": submission_id,
        "validation_result": {
            "overall_score": result.overall_score,
            "scores": {
                "mathematical_rigor": result.mathematical_rigor,
                "proof_correctness": result.proof_correctness,
                "code_elegance": result.code_elegance,
                "concept_mastery": result.concept_mastery
            },
            "concepts_identified": [
                {
                    "concept": c.concept.value,
                    "confidence": c.confidence,
                    "evidence": c.evidence,
                    "mastery_level": c.mastery_level
                }
                for c in result.concepts_identified
            ],
            "proof_analysis": {
                "steps_found": len(result.proof_steps),
                "valid_steps": sum(1 for step in result.proof_steps if step.is_valid),
                "proof_steps": [
                    {
                        "statement": step.statement,
                        "justification": step.justification,
                        "is_valid": step.is_valid,
                        "confidence": step.confidence
                    }
                    for step in result.proof_steps
                ]
            },
            "code_analysis": result.code_analysis,
            "feedback": result.feedback,
            "suggestions": result.suggestions
        }
    }


@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user profile information."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        # Return demo user for testing
        return UserResponse(
            id=user_id,
            username=f"demo_user_{user_id}",
            full_name="Demo User",
            current_level="foundation",
            mathematics_score=0.75,
            coding_score=0.68,
            innovation_score=0.42
        )
    
    return user


@user_router.get("/{user_id}/progress")
async def get_user_progress(user_id: int, db: Session = Depends(get_db)):
    """Get user's learning progress and analytics."""
    submissions = db.query(Submission).filter(Submission.user_id == user_id).all()
    
    if not submissions:
        return {
            "total_submissions": 0,
            "challenges_attempted": 0,
            "challenges_completed": 0,
            "average_score": 0.0,
            "mathematical_concepts_mastered": [],
            "areas_for_improvement": [],
            "learning_velocity": {}
        }
    
    # Calculate progress metrics
    total_submissions = len(submissions)
    challenges_attempted = len(set(s.challenge_id for s in submissions))
    challenges_completed = len(set(s.challenge_id for s in submissions if s.passed))
    average_score = sum(s.total_score for s in submissions) / total_submissions
    
    return {
        "total_submissions": total_submissions,
        "challenges_attempted": challenges_attempted,
        "challenges_completed": challenges_completed,
        "average_score": round(average_score, 3),
        "mathematical_concepts_mastered": ["modular_arithmetic", "prime_theory"],
        "areas_for_improvement": ["proof_writing", "complexity_analysis"],
        "learning_velocity": {
            "number_theory": 0.8,
            "algorithms": 0.6
        }
    }