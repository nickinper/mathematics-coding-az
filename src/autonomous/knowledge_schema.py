"""
Knowledge Database Schema for Mathematical Learning System
Uses SQLAlchemy for structured storage of concepts, patterns, and learning history.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import UniqueConstraint

Base = declarative_base()

# Association tables for many-to-many relationships
concept_prerequisites = Table('concept_prerequisites', Base.metadata,
    Column('concept_id', Integer, ForeignKey('concepts.id'), primary_key=True),
    Column('prerequisite_id', Integer, ForeignKey('concepts.id'), primary_key=True)
)

pattern_concepts = Table('pattern_concepts', Base.metadata,
    Column('pattern_id', Integer, ForeignKey('patterns.id'), primary_key=True),
    Column('concept_id', Integer, ForeignKey('concepts.id'), primary_key=True)
)


class Concept(Base):
    """Mathematical concepts that agents learn."""
    __tablename__ = 'concepts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    domain = Column(String(50), nullable=False)  # number_theory, algebra, etc.
    description = Column(Text)
    difficulty_level = Column(Integer, default=1)  # 1-10 scale
    
    # Mathematical properties stored as JSON
    mathematical_properties = Column(JSON, default=dict)
    # Example: {"commutative": true, "associative": true, "identity_element": "1"}
    
    # Relationships
    prerequisites = relationship(
        "Concept",
        secondary=concept_prerequisites,
        primaryjoin=(concept_prerequisites.c.concept_id == id),
        secondaryjoin=(concept_prerequisites.c.prerequisite_id == id),
        backref="dependent_concepts"
    )
    
    patterns = relationship("Pattern", secondary=pattern_concepts, back_populates="concepts")
    learning_records = relationship("LearningHistory", back_populates="concept")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'description': self.description,
            'difficulty_level': self.difficulty_level,
            'mathematical_properties': self.mathematical_properties,
            'prerequisites': [p.name for p in self.prerequisites],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Pattern(Base):
    """Code patterns representing mathematical concepts."""
    __tablename__ = 'patterns'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50), nullable=False)  # algorithmic, mathematical, optimization
    code_template = Column(Text)
    description = Column(Text)
    complexity = Column(String(50))  # O(n), O(log n), etc.
    confidence = Column(Float, default=0.5)
    
    # Usage statistics
    usage_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    
    # Mathematical properties as JSON
    mathematical_properties = Column(JSON, default=list)
    
    # Relationships
    concepts = relationship("Concept", secondary=pattern_concepts, back_populates="patterns")
    implementations = relationship("PatternImplementation", back_populates="pattern")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'code_template': self.code_template,
            'description': self.description,
            'complexity': self.complexity,
            'confidence': self.confidence,
            'usage_count': self.usage_count,
            'success_rate': self.success_rate,
            'mathematical_properties': self.mathematical_properties,
            'concepts': [c.name for c in self.concepts]
        }


class LearningHistory(Base):
    """Records of agent learning attempts."""
    __tablename__ = 'learning_history'
    
    id = Column(Integer, primary_key=True)
    agent_id = Column(String(100), nullable=False)
    concept_id = Column(Integer, ForeignKey('concepts.id'), nullable=False)
    challenge_name = Column(String(200))
    
    # Performance metrics
    attempt_number = Column(Integer, default=1)
    success = Column(Integer, default=0)  # 0 or 1
    score = Column(Float, default=0.0)
    time_taken = Column(Float)  # seconds
    
    # Learning details
    patterns_discovered = Column(JSON, default=list)
    errors_made = Column(JSON, default=list)
    feedback_received = Column(Text)
    
    # Code submitted
    submitted_code = Column(Text)
    mathematical_reasoning = Column(Text)
    
    # Relationships
    concept = relationship("Concept", back_populates="learning_records")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('agent_id', 'concept_id', 'challenge_name', 'attempt_number', 
                        name='_agent_concept_challenge_attempt_uc'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'concept': self.concept.name if self.concept else None,
            'challenge_name': self.challenge_name,
            'attempt_number': self.attempt_number,
            'success': bool(self.success),
            'score': self.score,
            'time_taken': self.time_taken,
            'patterns_discovered': self.patterns_discovered,
            'errors_made': self.errors_made,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class PatternImplementation(Base):
    """Successful pattern implementations by agents."""
    __tablename__ = 'pattern_implementations'
    
    id = Column(Integer, primary_key=True)
    agent_id = Column(String(100), nullable=False)
    pattern_id = Column(Integer, ForeignKey('patterns.id'), nullable=False)
    challenge_name = Column(String(200))
    
    implementation_code = Column(Text, nullable=False)
    performance_score = Column(Float, default=0.0)
    correctness_score = Column(Float, default=0.0)
    
    # Relationships
    pattern = relationship("Pattern", back_populates="implementations")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'pattern': self.pattern.name if self.pattern else None,
            'challenge_name': self.challenge_name,
            'performance_score': self.performance_score,
            'correctness_score': self.correctness_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ConceptRelationship(Base):
    """Relationships between concepts beyond prerequisites."""
    __tablename__ = 'concept_relationships'
    
    id = Column(Integer, primary_key=True)
    concept_from_id = Column(Integer, ForeignKey('concepts.id'), nullable=False)
    concept_to_id = Column(Integer, ForeignKey('concepts.id'), nullable=False)
    relationship_type = Column(String(50), nullable=False)  # 'generalizes', 'specializes', 'relates_to'
    strength = Column(Float, default=0.5)  # 0.0 to 1.0
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('concept_from_id', 'concept_to_id', 'relationship_type',
                        name='_concept_relationship_uc'),
    )


class KnowledgeDatabase:
    """Interface for knowledge database operations."""
    
    def __init__(self, db_path: str = "sqlite:///knowledge.db"):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def add_concept(self, name: str, domain: str, description: str,
                   difficulty: int = 1, properties: Dict[str, Any] = None,
                   prerequisites: List[str] = None) -> Concept:
        """Add a new mathematical concept."""
        session = self.Session()
        try:
            concept = Concept(
                name=name,
                domain=domain,
                description=description,
                difficulty_level=difficulty,
                mathematical_properties=properties or {}
            )
            
            session.add(concept)
            
            # Add prerequisites if provided
            if prerequisites:
                for prereq_name in prerequisites:
                    prereq = session.query(Concept).filter_by(name=prereq_name).first()
                    if prereq:
                        concept.prerequisites.append(prereq)
            
            session.commit()
            session.refresh(concept)
            
            # Create a detached copy to return
            result = Concept(
                name=concept.name,
                domain=concept.domain,
                description=concept.description,
                difficulty_level=concept.difficulty_level,
                mathematical_properties=concept.mathematical_properties
            )
            result.id = concept.id
            return result
        finally:
            session.close()
    
    def add_pattern(self, name: str, category: str, template: str,
                   description: str, complexity: str = None,
                   properties: List[str] = None) -> Pattern:
        """Add a new code pattern."""
        session = self.Session()
        try:
            pattern = Pattern(
                name=name,
                category=category,
                code_template=template,
                description=description,
                complexity=complexity,
                mathematical_properties=properties or []
            )
            session.add(pattern)
            session.commit()
            session.refresh(pattern)
            
            # Create a detached copy to return
            result = Pattern(
                name=pattern.name,
                category=pattern.category,
                code_template=pattern.code_template,
                description=pattern.description,
                complexity=pattern.complexity,
                mathematical_properties=pattern.mathematical_properties
            )
            result.id = pattern.id
            return result
        finally:
            session.close()
    
    def record_learning_attempt(self, agent_id: str, concept_name: str,
                              challenge_name: str, success: bool,
                              score: float, time_taken: float,
                              code: str, reasoning: str,
                              patterns: List[str] = None,
                              errors: List[str] = None) -> LearningHistory:
        """Record an agent's learning attempt."""
        session = self.Session()
        try:
            concept = session.query(Concept).filter_by(name=concept_name).first()
            if not concept:
                raise ValueError(f"Concept '{concept_name}' not found")
            
            # Get attempt number
            previous_attempts = session.query(LearningHistory).filter_by(
                agent_id=agent_id,
                concept_id=concept.id,
                challenge_name=challenge_name
            ).count()
            
            record = LearningHistory(
                agent_id=agent_id,
                concept_id=concept.id,
                challenge_name=challenge_name,
                attempt_number=previous_attempts + 1,
                success=1 if success else 0,
                score=score,
                time_taken=time_taken,
                submitted_code=code,
                mathematical_reasoning=reasoning,
                patterns_discovered=patterns or [],
                errors_made=errors or []
            )
            
            session.add(record)
            session.commit()
            session.refresh(record)
            
            # Create dictionary before closing session
            result_dict = record.to_dict()
            
            return result_dict
        finally:
            session.close()
    
    def get_agent_knowledge(self, agent_id: str) -> Dict[str, Any]:
        """Get an agent's current knowledge state."""
        session = self.Session()
        try:
            # Get all successful learning records
            successful_records = session.query(LearningHistory).filter_by(
                agent_id=agent_id,
                success=1
            ).all()
            
            # Extract mastered concepts
            mastered_concepts = list(set(r.concept.name for r in successful_records))
            
            # Get patterns used
            all_patterns = []
            for record in successful_records:
                all_patterns.extend(record.patterns_discovered or [])
            
            pattern_counts = {}
            for pattern in all_patterns:
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
            
            return {
                'agent_id': agent_id,
                'mastered_concepts': mastered_concepts,
                'total_attempts': session.query(LearningHistory).filter_by(agent_id=agent_id).count(),
                'success_rate': len(successful_records) / max(1, session.query(LearningHistory).filter_by(agent_id=agent_id).count()),
                'pattern_usage': pattern_counts,
                'last_attempt': max((r.created_at for r in successful_records), default=None)
            }
        finally:
            session.close()
    
    def get_concept_graph(self) -> Dict[str, List[str]]:
        """Get the concept prerequisite graph."""
        session = self.Session()
        try:
            concepts = session.query(Concept).all()
            graph = {}
            
            for concept in concepts:
                graph[concept.name] = [p.name for p in concept.prerequisites]
            
            return graph
        finally:
            session.close()
    
    def suggest_next_concept(self, agent_id: str) -> Optional[str]:
        """Suggest the next concept for an agent to learn."""
        session = self.Session()
        try:
            # Get mastered concepts
            knowledge = self.get_agent_knowledge(agent_id)
            mastered = set(knowledge['mastered_concepts'])
            
            # Get all concepts
            all_concepts = session.query(Concept).all()
            
            # Find concepts where all prerequisites are mastered
            candidates = []
            for concept in all_concepts:
                if concept.name not in mastered:
                    prereqs = set(p.name for p in concept.prerequisites)
                    if prereqs.issubset(mastered):
                        candidates.append((concept.name, concept.difficulty_level))
            
            # Return easiest unlearned concept with satisfied prerequisites
            if candidates:
                candidates.sort(key=lambda x: x[1])
                return candidates[0][0]
            
            return None
        finally:
            session.close()


# Initialize default concepts and patterns
def initialize_default_knowledge(db: KnowledgeDatabase):
    """Initialize the database with default number theory concepts."""
    
    # Add domain concept
    db.add_concept(
        name="number_theory",
        domain="mathematics",
        description="Study of integers and integer-valued functions",
        difficulty=1,
        properties={"fundamental": True}
    )
    
    # Add fundamental concepts
    db.add_concept(
        name="arithmetic",
        domain="number_theory",
        description="Basic arithmetic operations",
        difficulty=1,
        properties={"operations": ["addition", "subtraction", "multiplication", "division"]},
        prerequisites=["number_theory"]
    )
    
    db.add_concept(
        name="divisibility",
        domain="number_theory", 
        description="Understanding when one number divides another",
        difficulty=2,
        properties={"notation": "a|b", "transitive": True},
        prerequisites=["arithmetic", "number_theory"]
    )
    
    db.add_concept(
        name="gcd",
        domain="number_theory",
        description="Greatest Common Divisor",
        difficulty=3,
        properties={"commutative": True, "associative": True},
        prerequisites=["divisibility", "number_theory"]
    )
    
    db.add_concept(
        name="modular_arithmetic",
        domain="number_theory",
        description="Arithmetic modulo n",
        difficulty=4,
        properties={"forms_ring": True},
        prerequisites=["arithmetic", "divisibility", "number_theory"]
    )
    
    # Add patterns
    db.add_pattern(
        name="euclidean_algorithm",
        category="algorithmic",
        template="while b != 0:\n    a, b = b, a % b\nreturn a",
        description="Efficient GCD computation",
        complexity="O(log(min(a,b)))",
        properties=["iterative", "modular_reduction"]
    )