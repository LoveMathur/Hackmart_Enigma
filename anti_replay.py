# anti_replay.py
import hashlib
import os
from datetime import datetime, timedelta

class AntiReplayProtection:
    def __init__(self):
        self.used_nonces = set()
        self.vote_timestamps = {}
        self.voted_ids = set()
    
    def check_duplicate_vote(self, voter_id_hash):
        """Prevent same voter from voting twice"""
        if voter_id_hash in self.voted_ids:
            return False, "Voter has already cast a vote"
        return True, None
    
    def register_vote(self, voter_id_hash, nonce, timestamp):
        """Register vote to prevent replay attacks"""
        # Check nonce uniqueness
        if nonce in self.used_nonces:
            return False, "Duplicate transaction detected"
        
        # Check timestamp freshness (within 5 minutes)
        try:
            vote_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            # Remove timezone info to compare with naive datetime
            if vote_time.tzinfo is not None:
                vote_time = vote_time.replace(tzinfo=None)
            
            time_diff = abs((datetime.utcnow() - vote_time).total_seconds())
            if time_diff > 300:
                return False, "Transaction timestamp expired"
        except Exception as e:
            # If timestamp parsing fails, just skip the freshness check
            print(f"Timestamp parsing warning: {e}")
        
        # Register vote
        self.used_nonces.add(nonce)
        self.voted_ids.add(voter_id_hash)
        self.vote_timestamps[voter_id_hash] = timestamp
        
        return True, None
    
    def generate_nonce(self, voter_id, timestamp):
        """Generate unique transaction nonce"""
        data = f"{voter_id}{timestamp}{os.urandom(16).hex()}"
        return hashlib.sha256(data.encode()).hexdigest()