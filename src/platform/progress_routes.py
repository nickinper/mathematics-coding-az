"""API routes for user progress tracking."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

from .database import get_db
from .models import User, Submission, ChallengeProgress, UserFailureProfile, LearnabilityReward, Challenge
from .authentication import get_current_active_user


# Initialize router
progress_router = APIRouter()


class ProgressSummary(BaseModel):
    total_submissions: int
    challenges_attempted: int
    challenges_completed: int
    average_score: float
    current_streak: int
    best_streak: int
    mathematical_concepts_mastered: List[str]
    areas_for_improvement: List[str]
    learning_velocity: dict


class ProgressDetail(BaseModel):
    domain: str
    score: float
    completion_rate: float
    strengths: List[str]
    weaknesses: List[str]
    recommended_challenges: List[int]


@progress_router.get("/summary")
async def get_progress_summary(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get summary of user's learning progress."""
    # Get submission data
    submissions = db.query(Submission).filter(Submission.user_id == current_user.id).all()
    
    if not submissions:
        return {
            "total_submissions": 0,
            "challenges_attempted": 0,
            "challenges_completed": 0,
            "average_score": 0.0,
            "current_streak": 0,
            "best_streak": 0,
            "mathematical_concepts_mastered": [],
            "areas_for_improvement": [],
            "learning_velocity": {}
        }
    
    # Calculate basic metrics
    total_submissions = len(submissions)
    challenges_attempted = db.query(Submission.challenge_id).filter(
        Submission.user_id == current_user.id
    ).distinct().count()
    
    challenges_completed = db.query(Submission.challenge_id).filter(
        Submission.user_id == current_user.id,
        Submission.passed == True
    ).distinct().count()
    
    # Calculate average score
    average_score = sum(s.total_score for s in submissions) / total_submissions if total_submissions > 0 else 0
    
    # Get current streak
    current_streak = 0
    best_streak = 0
    streak_days = set()
    
    for submission in submissions:
        submission_date = submission.submitted_at.date()
        streak_days.add(submission_date)
    
    # Check if the user has a submission today
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    if today in streak_days:
        current_streak = 1
        check_date = yesterday
        
        while check_date in streak_days:
            current_streak += 1
            check_date = check_date - timedelta(days=1)
    
    # Calculate best streak
    streak_days = sorted(list(streak_days))
    current_best = 1
    current_count = 1
    
    for i in range(1, len(streak_days)):
        if (streak_days[i] - streak_days[i-1]) == timedelta(days=1):
            current_count += 1
        else:
            current_best = max(current_best, current_count)
            current_count = 1
    
    best_streak = max(current_best, current_count)
    
    # Get mastered concepts and areas for improvement
    mastered_concepts = []
    improvement_areas = []
    
    # In a real implementation, this would be determined from challenge progress and concept mastery
    # For demo purposes, use placeholder data
    mastered_concepts = ["modular_arithmetic", "binary_exponentiation", "matrix_operations"]
    improvement_areas = ["proof_writing", "complexity_analysis", "algorithm_optimization"]
    
    # Calculate learning velocity per domain
    learning_velocity = {}
    domain_submissions = {}
    
    for submission in submissions:
        challenge = db.query(Challenge).filter(Challenge.id == submission.challenge_id).first()
        if challenge:
            domain = challenge.domain
            if domain not in domain_submissions:
                domain_submissions[domain] = []
            domain_submissions[domain].append((submission.submitted_at, submission.total_score))
    
    for domain, submissions_data in domain_submissions.items():
        # Sort by date
        submissions_data.sort(key=lambda x: x[0])
        
        # Calculate velocity as average improvement per submission
        if len(submissions_data) >= 2:
            first_score = submissions_data[0][1]
            last_score = submissions_data[-1][1]
            improvement = max(0, last_score - first_score)
            velocity = improvement / (len(submissions_data) - 1) if len(submissions_data) > 1 else 0
            learning_velocity[domain] = round(velocity * 10, 2)  # Scale for better visibility
        else:
            learning_velocity[domain] = 0.0
    
    return {
        "total_submissions": total_submissions,
        "challenges_attempted": challenges_attempted,
        "challenges_completed": challenges_completed,
        "average_score": round(average_score, 3),
        "current_streak": current_streak,
        "best_streak": best_streak,
        "mathematical_concepts_mastered": mastered_concepts,
        "areas_for_improvement": improvement_areas,
        "learning_velocity": learning_velocity
    }


@progress_router.get("/domains/{domain}")
async def get_domain_progress(
    domain: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed progress for a specific mathematical domain."""
    # Get challenges in this domain
    domain_challenges = db.query(Challenge).filter(Challenge.domain == domain).all()
    
    if not domain_challenges:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No challenges found for domain: {domain}"
        )
    
    # Get user's submissions for challenges in this domain
    challenge_ids = [c.id for c in domain_challenges]
    submissions = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.challenge_id.in_(challenge_ids)
    ).all()
    
    # Calculate domain metrics
    total_challenges = len(domain_challenges)
    attempted_challenges = db.query(Submission.challenge_id).filter(
        Submission.user_id == current_user.id,
        Submission.challenge_id.in_(challenge_ids)
    ).distinct().count()
    
    completed_challenges = db.query(Submission.challenge_id).filter(
        Submission.user_id == current_user.id,
        Submission.challenge_id.in_(challenge_ids),
        Submission.passed == True
    ).distinct().count()
    
    # Calculate domain score
    domain_score = 0.0
    if submissions:
        # Get highest score for each challenge
        best_scores = {}
        for submission in submissions:
            if submission.challenge_id not in best_scores or submission.total_score > best_scores[submission.challenge_id]:
                best_scores[submission.challenge_id] = submission.total_score
        
        domain_score = sum(best_scores.values()) / len(best_scores) if best_scores else 0.0
    
    completion_rate = completed_challenges / total_challenges if total_challenges > 0 else 0.0
    
    # Identify strengths and weaknesses (in a real system, would be more sophisticated)
    strengths = []
    weaknesses = []
    
    # For demo purposes, use placeholder data based on domain
    if domain == "number_theory":
        strengths = ["Prime number theory", "Modular arithmetic"]
        weaknesses = ["Proof techniques", "Number theoretic algorithms"]
    elif domain == "linear_algebra":
        strengths = ["Matrix operations", "Linear transformations"]
        weaknesses = ["Eigenvalues", "Vector spaces"]
    else:
        strengths = ["Basic concepts"]
        weaknesses = ["Advanced applications"]
    
    # Get recommended challenges
    # In a real system, this would use a recommendation algorithm
    # For demo, just recommend challenges the user hasn't completed
    completed_challenge_ids = [s.challenge_id for s in submissions if s.passed]
    recommended_challenges = [c.id for c in domain_challenges if c.id not in completed_challenge_ids][:3]
    
    return {
        "domain": domain,
        "total_challenges": total_challenges,
        "attempted_challenges": attempted_challenges,
        "completed_challenges": completed_challenges,
        "domain_score": round(domain_score, 3),
        "completion_rate": round(completion_rate, 3),
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommended_challenges": recommended_challenges
    }


@progress_router.get("/concepts")
async def get_concept_mastery(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get the user's mastery level of mathematical concepts."""
    # In a real implementation, this would query a concept mastery table
    # For demo purposes, use placeholder data
    return {
        "concepts": [
            {
                "concept": "modular_arithmetic",
                "mastery_level": 0.85,
                "challenges_used_in": [1, 2, 5],
                "last_used": "2025-06-17T10:30:00Z"
            },
            {
                "concept": "binary_exponentiation",
                "mastery_level": 0.75,
                "challenges_used_in": [1, 3],
                "last_used": "2025-06-16T14:20:00Z"
            },
            {
                "concept": "matrix_operations",
                "mastery_level": 0.9,
                "challenges_used_in": [2, 4],
                "last_used": "2025-06-18T09:15:00Z"
            },
            {
                "concept": "proof_by_induction",
                "mastery_level": 0.6,
                "challenges_used_in": [1, 5],
                "last_used": "2025-06-15T16:45:00Z"
            },
            {
                "concept": "complexity_analysis",
                "mastery_level": 0.5,
                "challenges_used_in": [3, 4, 5],
                "last_used": "2025-06-14T11:10:00Z"
            }
        ]
    }


@progress_router.get("/achievements")
async def get_achievements(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get the user's earned achievements."""
    # In a real implementation, this would query an achievements table
    # For demo purposes, use placeholder data
    return {
        "achievements": [
            {
                "id": 1,
                "name": "First Steps",
                "description": "Complete your first challenge",
                "earned_at": "2025-06-14T10:30:00Z",
                "icon": "beginner_badge"
            },
            {
                "id": 2,
                "name": "Number Theorist",
                "description": "Complete 3 number theory challenges",
                "earned_at": "2025-06-16T14:20:00Z",
                "icon": "number_theory_badge"
            },
            {
                "id": 3,
                "name": "Perfect Proof",
                "description": "Receive a perfect score on mathematical reasoning",
                "earned_at": "2025-06-17T09:15:00Z",
                "icon": "proof_badge"
            }
        ],
        "upcoming_achievements": [
            {
                "id": 4,
                "name": "3-Day Streak",
                "description": "Complete challenges on 3 consecutive days",
                "progress": 0.67,  # 2/3 days
                "icon": "streak_badge"
            },
            {
                "id": 5,
                "name": "Code Elegance",
                "description": "Receive a perfect score on code quality",
                "progress": 0.85,  # Best code quality score so far
                "icon": "code_badge"
            }
        ]
    }


@progress_router.get("/learning-path")
async def get_learning_path(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get the user's personalized learning path."""
    # In a real implementation, this would generate a customized learning path
    # based on the user's progress, strengths, and weaknesses
    # For demo purposes, use placeholder data
    return {
        "current_level": current_user.current_level,
        "progress_to_next_level": 0.75,
        "recommended_path": [
            {
                "step": 1,
                "status": "completed",
                "challenges": [1, 2],
                "concepts": ["modular_arithmetic", "prime_numbers"]
            },
            {
                "step": 2,
                "status": "in_progress",
                "challenges": [3, 4, 5],
                "concepts": ["binary_exponentiation", "complexity_analysis"]
            },
            {
                "step": 3,
                "status": "upcoming",
                "challenges": [6, 7],
                "concepts": ["matrix_operations", "linear_transformations"]
            }
        ],
        "mastery_goals": [
            {
                "concept": "proof_writing",
                "current_level": 0.6,
                "target_level": 0.8,
                "recommended_challenges": [5, 8]
            },
            {
                "concept": "algorithm_optimization",
                "current_level": 0.5,
                "target_level": 0.7,
                "recommended_challenges": [3, 9]
            }
        ]
    }