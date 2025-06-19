"""Web platform and API for Mathematics-Based Coding AZ."""

from .server import create_app
from .models import User, Submission, Challenge as ChallengeModel
from .api import challenge_router, submission_router, user_router

__all__ = [
    "create_app",
    "User",
    "Submission", 
    "ChallengeModel",
    "challenge_router",
    "submission_router",
    "user_router",
]