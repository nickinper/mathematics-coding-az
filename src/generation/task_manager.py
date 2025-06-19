"""
Task Manager for managing challenge generation and scheduling.

This module handles:
- Challenge queue management
- Scheduling new challenges
- Tracking challenge generation and usage
"""

import os
import json
import time
import random
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

from src.core.challenge import Challenge, ChallengeLevel, MathematicalDomain
from src.generation.challenge_generator import ChallengeGenerator, GenerationStrategy


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskManager:
    """Manages the generation and scheduling of challenges."""
    
    def __init__(
        self,
        generator: Optional[ChallengeGenerator] = None,
        cache_dir: str = "cache/challenges"
    ):
        """
        Initialize the task manager.
        
        Args:
            generator: Challenge generator to use
            cache_dir: Directory for caching generated challenges
        """
        self.generator = generator or ChallengeGenerator()
        self.cache_dir = cache_dir
        self.challenge_queue = defaultdict(list)
        self.usage_stats = defaultdict(int)
        
        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Load cached challenges
        self._load_cached_challenges()
    
    def _load_cached_challenges(self):
        """Load cached challenges from disk."""
        for domain_dir in os.listdir(self.cache_dir):
            domain_path = os.path.join(self.cache_dir, domain_dir)
            if os.path.isdir(domain_path):
                domain = MathematicalDomain(domain_dir)
                
                for level_dir in os.listdir(domain_path):
                    level_path = os.path.join(domain_path, level_dir)
                    if os.path.isdir(level_path):
                        level = ChallengeLevel(level_dir)
                        key = (domain, level)
                        
                        for challenge_file in os.listdir(level_path):
                            if challenge_file.endswith(".json"):
                                challenge_path = os.path.join(level_path, challenge_file)
                                try:
                                    # Load challenge metadata
                                    with open(challenge_path, 'r') as f:
                                        challenge_meta = json.load(f)
                                        self.challenge_queue[key].append(challenge_meta)
                                except Exception as e:
                                    logger.error(f"Error loading cached challenge {challenge_path}: {str(e)}")
    
    def get_challenge(
        self,
        domain: MathematicalDomain,
        level: ChallengeLevel,
        user_id: Optional[str] = None,
        regenerate: bool = False
    ) -> Dict[str, Any]:
        """
        Get a challenge for the given domain and level.
        
        Args:
            domain: Mathematical domain
            level: Difficulty level
            user_id: ID of the user requesting the challenge
            regenerate: Whether to force regeneration of a new challenge
            
        Returns:
            Challenge metadata
        """
        key = (domain, level)
        
        # If we need to regenerate or the queue is empty
        if regenerate or not self.challenge_queue[key]:
            # Generate a new challenge
            challenge = self.generator.generate_challenge(domain, level)
            
            # Convert challenge to metadata
            challenge_meta = self._challenge_to_meta(challenge, user_id)
            
            # Cache the challenge
            self._cache_challenge(challenge_meta)
            
            # Add to queue
            self.challenge_queue[key].append(challenge_meta)
        
        # Get a challenge from the queue
        challenge_meta = random.choice(self.challenge_queue[key])
        
        # Update usage stats
        challenge_id = challenge_meta.get("id", "unknown")
        self.usage_stats[challenge_id] += 1
        
        # Update the challenge's last used timestamp
        challenge_meta["last_used"] = datetime.now().isoformat()
        
        # Update the cache
        self._update_cached_challenge(challenge_meta)
        
        return challenge_meta
    
    def schedule_generation(
        self,
        domains: Optional[List[MathematicalDomain]] = None,
        levels: Optional[List[ChallengeLevel]] = None,
        count: int = 1
    ):
        """
        Schedule the generation of new challenges.
        
        Args:
            domains: List of domains to generate challenges for
            levels: List of levels to generate challenges for
            count: Number of challenges to generate per domain/level combination
        """
        domains = domains or list(MathematicalDomain)
        levels = levels or list(ChallengeLevel)
        
        for domain in domains:
            for level in levels:
                for _ in range(count):
                    try:
                        challenge = self.generator.generate_challenge(domain, level)
                        challenge_meta = self._challenge_to_meta(challenge)
                        self._cache_challenge(challenge_meta)
                        self.challenge_queue[(domain, level)].append(challenge_meta)
                        logger.info(f"Generated challenge {challenge_meta['id']} for {domain.value}/{level.value}")
                    except Exception as e:
                        logger.error(f"Error generating challenge for {domain.value}/{level.value}: {str(e)}")
    
    def _challenge_to_meta(
        self,
        challenge: Challenge,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Convert a Challenge object to metadata for caching."""
        # Generate a unique ID for the challenge
        challenge_id = f"{challenge.domain.value}_{challenge.level.value}_{int(time.time())}"
        
        return {
            "id": challenge_id,
            "title": challenge.title,
            "description": challenge.description,
            "domain": challenge.domain.value,
            "level": challenge.level.value,
            "created_at": datetime.now().isoformat(),
            "last_used": datetime.now().isoformat(),
            "created_for": user_id,
            "usage_count": 0,
            "mathematical_requirements": [
                {
                    "concept": req.concept,
                    "description": req.description,
                    "proof_required": req.proof_required,
                    "complexity_analysis": req.complexity_analysis
                }
                for req in challenge.mathematical_requirements
            ],
            "test_cases": [
                {
                    "input_data": tc.input_data,
                    "expected_output": tc.expected_output,
                    "description": tc.description
                }
                for tc in challenge.test_cases
            ],
            "time_limit": challenge.time_limit
        }
    
    def _cache_challenge(self, challenge_meta: Dict[str, Any]):
        """Cache a challenge to disk."""
        domain = challenge_meta["domain"]
        level = challenge_meta["level"]
        challenge_id = challenge_meta["id"]
        
        # Create directory if it doesn't exist
        domain_dir = os.path.join(self.cache_dir, domain)
        os.makedirs(domain_dir, exist_ok=True)
        
        level_dir = os.path.join(domain_dir, level)
        os.makedirs(level_dir, exist_ok=True)
        
        # Write challenge to file
        challenge_path = os.path.join(level_dir, f"{challenge_id}.json")
        with open(challenge_path, 'w') as f:
            json.dump(challenge_meta, f, indent=2)
    
    def _update_cached_challenge(self, challenge_meta: Dict[str, Any]):
        """Update a cached challenge on disk."""
        domain = challenge_meta["domain"]
        level = challenge_meta["level"]
        challenge_id = challenge_meta["id"]
        
        challenge_path = os.path.join(self.cache_dir, domain, level, f"{challenge_id}.json")
        if os.path.exists(challenge_path):
            with open(challenge_path, 'w') as f:
                json.dump(challenge_meta, f, indent=2)
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics for challenges."""
        return {
            "total_challenges": sum(len(queue) for queue in self.challenge_queue.values()),
            "challenges_by_domain": {
                domain.value: sum(1 for key, queue in self.challenge_queue.items() if key[0] == domain for _ in queue)
                for domain in MathematicalDomain
            },
            "challenges_by_level": {
                level.value: sum(1 for key, queue in self.challenge_queue.items() if key[1] == level for _ in queue)
                for level in ChallengeLevel
            },
            "most_used_challenges": sorted(
                self.usage_stats.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10],
            "total_usage": sum(self.usage_stats.values())
        }
    
    def clean_old_challenges(self, days: int = 30):
        """
        Clean up challenges that haven't been used in a while.
        
        Args:
            days: Remove challenges older than this many days
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.isoformat()
        
        for key, queue in self.challenge_queue.items():
            domain, level = key
            
            # Filter out old challenges
            new_queue = []
            for challenge_meta in queue:
                last_used = datetime.fromisoformat(challenge_meta.get("last_used", "2000-01-01T00:00:00"))
                
                if last_used > cutoff_date:
                    new_queue.append(challenge_meta)
                else:
                    # Remove from disk
                    challenge_id = challenge_meta.get("id", "unknown")
                    challenge_path = os.path.join(self.cache_dir, domain.value, level.value, f"{challenge_id}.json")
                    if os.path.exists(challenge_path):
                        os.remove(challenge_path)
                    
                    logger.info(f"Removed old challenge {challenge_id}")
            
            self.challenge_queue[key] = new_queue