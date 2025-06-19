"""API routes for challenge generation."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from .challenge_generator import ChallengeGenerator, GenerationStrategy, ChallengeFactory
from .task_manager import TaskManager
from src.core.challenge import ChallengeLevel, MathematicalDomain
from src.platform.authentication import get_current_active_user
from src.platform.database import get_db
from src.platform.models import User, Challenge as ChallengeModel


# Initialize services
challenge_generator = ChallengeGenerator()
challenge_factory = ChallengeFactory(generator=challenge_generator)
task_manager = TaskManager(generator=challenge_generator)


# Pydantic models for API
class GenerateChallengeRequest(BaseModel):
    domain: str
    level: str
    strategy: Optional[str] = "template_based"
    parameters: Optional[Dict[str, Any]] = None


class ScheduleGenerationRequest(BaseModel):
    domains: Optional[List[str]] = None
    levels: Optional[List[str]] = None
    count: int = 1


class GenerateChallengeResponse(BaseModel):
    id: str
    title: str
    description: str
    domain: str
    level: str
    mathematical_requirements: List[Dict[str, Any]]
    test_cases: List[Dict[str, Any]]
    time_limit: float


# Initialize router
generation_router = APIRouter()


@generation_router.post("/generate", response_model=GenerateChallengeResponse)
async def generate_challenge(
    request: GenerateChallengeRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate a new challenge."""
    try:
        # Convert string to enum
        domain = MathematicalDomain(request.domain)
        level = ChallengeLevel(request.level)
        strategy = GenerationStrategy(request.strategy)
        
        # Generate challenge
        challenge_meta = task_manager.get_challenge(
            domain=domain,
            level=level,
            user_id=str(current_user.id),
            regenerate=True
        )
        
        return challenge_meta
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid parameters: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating challenge: {str(e)}"
        )


@generation_router.post("/schedule")
async def schedule_generation(
    request: ScheduleGenerationRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Schedule the generation of new challenges."""
    try:
        # Convert strings to enums
        domains = [MathematicalDomain(d) for d in request.domains] if request.domains else None
        levels = [ChallengeLevel(l) for l in request.levels] if request.levels else None
        
        # Schedule generation
        task_manager.schedule_generation(
            domains=domains,
            levels=levels,
            count=request.count
        )
        
        return {
            "status": "success",
            "message": f"Scheduled generation of {request.count} challenges per domain/level combination"
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid parameters: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error scheduling generation: {str(e)}"
        )


@generation_router.get("/stats")
async def get_generation_stats(
    current_user: User = Depends(get_current_active_user)
):
    """Get statistics about challenge generation."""
    return task_manager.get_usage_stats()


@generation_router.post("/save")
async def save_generated_challenge(
    challenge_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Save a generated challenge to the database."""
    try:
        # Create a new challenge model
        challenge = ChallengeModel(
            title=challenge_data["title"],
            description=challenge_data["description"],
            level=challenge_data["level"],
            domain=challenge_data["domain"],
            time_limit=challenge_data.get("time_limit", 600.0),
            difficulty_score=0.7,  # Default value
            test_cases=challenge_data["test_cases"],
            mathematical_requirements=challenge_data["mathematical_requirements"],
            author_id=current_user.id
        )
        
        db.add(challenge)
        db.commit()
        db.refresh(challenge)
        
        return {
            "status": "success",
            "message": "Challenge saved to database",
            "challenge_id": challenge.id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving challenge: {str(e)}"
        )


@generation_router.post("/clean")
async def clean_old_challenges(
    days: int = 30,
    current_user: User = Depends(get_current_active_user)
):
    """Clean up old challenges that haven't been used recently."""
    try:
        task_manager.clean_old_challenges(days=days)
        
        return {
            "status": "success",
            "message": f"Cleaned up challenges older than {days} days"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error cleaning challenges: {str(e)}"
        )