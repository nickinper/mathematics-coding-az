"""Database models for the platform."""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    """User model for student accounts."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    
    # Academic tracking
    current_level = Column(String(20), default="foundation")
    mathematics_score = Column(Float, default=0.0)
    coding_score = Column(Float, default=0.0)
    innovation_score = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    submissions = relationship("Submission", back_populates="user")
    failure_profiles = relationship("UserFailureProfile", back_populates="user")


class Challenge(Base):
    """Challenge model for mathematical coding problems."""
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    level = Column(String(20), nullable=False)  # foundation, intermediate, advanced
    domain = Column(String(50), nullable=False)  # number_theory, linear_algebra, etc.
    
    # Mathematical requirements (stored as JSON)
    mathematical_requirements = Column(JSON)
    test_cases = Column(JSON)
    
    # Metadata
    time_limit = Column(Float, default=300.0)
    difficulty_score = Column(Float, default=0.5)
    pass_rate = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    submissions = relationship("Submission", back_populates="challenge")


class Submission(Base):
    """Submission model for student solutions."""
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    
    # Submission content
    code = Column(Text, nullable=False)
    mathematical_reasoning = Column(Text)
    attempt_number = Column(Integer, default=1)
    
    # Results
    passed = Column(Boolean, default=False)
    functional_score = Column(Float, default=0.0)
    mathematical_score = Column(Float, default=0.0)
    code_quality_score = Column(Float, default=0.0)
    innovation_score = Column(Float, default=0.0)
    total_score = Column(Float, default=0.0)
    
    # Detailed results (stored as JSON)
    test_results = Column(JSON)
    feedback = Column(JSON)
    
    # Timestamps
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    execution_time = Column(Float)
    
    # Relationships
    user = relationship("User", back_populates="submissions")
    challenge = relationship("Challenge", back_populates="submissions")


class UserFailureProfile(Base):
    """Model for tracking user failure patterns and learning progress."""
    __tablename__ = "user_failure_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Failure analysis
    mathematical_concept = Column(String(100), nullable=False)
    failure_count = Column(Integer, default=1)
    total_time_spent = Column(Float, default=0.0)
    
    # Learning tracking
    first_failure_at = Column(DateTime(timezone=True), server_default=func.now())
    last_failure_at = Column(DateTime(timezone=True), onupdate=func.now())
    success_achieved = Column(Boolean, default=False)
    success_achieved_at = Column(DateTime(timezone=True))
    recovery_method = Column(String(100))
    
    # Learning velocity
    learning_velocity = Column(Float, default=0.0)
    
    # Relationships
    user = relationship("User", back_populates="failure_profiles")


class FailureAttempt(Base):
    """Model for individual failure attempts."""
    __tablename__ = "failure_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    
    # Failure details
    failure_type = Column(String(50), nullable=False)
    mathematical_concept = Column(String(100), nullable=False)
    specific_issue = Column(Text)
    severity = Column(Float, default=0.5)
    
    # Context
    attempt_number = Column(Integer, default=1)
    time_spent = Column(Float, default=0.0)
    mathematical_concepts_used = Column(JSON)
    
    # Response
    hints_provided = Column(JSON)
    alternative_paths_suggested = Column(JSON)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LearnabilityReward(Base):
    """Model for tracking learnability rewards."""
    __tablename__ = "learnability_rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    
    # Reward components
    exploration_bonus = Column(Float, default=0.0)
    mathematical_insight_bonus = Column(Float, default=0.0)
    failed_attempt_learning_bonus = Column(Float, default=0.0)
    alternative_approach_bonus = Column(Float, default=0.0)
    proof_attempt_bonus = Column(Float, default=0.0)
    
    # Total
    total_reward = Column(Float, default=0.0)
    
    # Timestamp
    awarded_at = Column(DateTime(timezone=True), server_default=func.now())


class ChallengeProgress(Base):
    """Model for tracking user progress through challenges."""
    __tablename__ = "challenge_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    
    # Progress tracking
    status = Column(String(20), default="not_started")  # not_started, in_progress, completed, mastered
    best_score = Column(Float, default=0.0)
    attempts = Column(Integer, default=0)
    time_spent = Column(Float, default=0.0)
    
    # Learning insights
    mathematical_concepts_mastered = Column(JSON)
    areas_for_improvement = Column(JSON)
    
    # Timestamps
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    last_attempt_at = Column(DateTime(timezone=True), onupdate=func.now())