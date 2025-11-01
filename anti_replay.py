# anti_replay.py
import hashlib
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
        vote_time = datetime.fromisoformat(timestamp)
        if abs((datetime.utcnow() - vote_time).total_seconds()) > 300:
            return False, "Transaction timestamp expired"
        
        # Register vote
        self.used_nonces.add(nonce)
        self.voted_ids.add(voter_id_hash)
        self.vote_timestamps[voter_id_hash] = timestamp
        
        return True, None
    
    def generate_nonce(self, voter_id, timestamp):
        """Generate unique transaction nonce"""
        data = f"{voter_id}{timestamp}{os.urandom(16).hex()}"
        return hashlib.sha256(data.encode()).hexdigest()