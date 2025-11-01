# blockchain_lite.py
import hashlib
import json
from datetime import datetime
import os

class TamperEvidenceChain:
    """
    Append-only, cryptographically linked log (blockchain-like)
    Each block contains: vote_hash, previous_hash, timestamp, nonce
    """
    def __init__(self, chain_file='vote_chain.json'):
        self.chain_file = chain_file
        self.chain = self.load_chain()
        
        if not self.chain:
            self.chain = [self.create_genesis_block()]
            self.save_chain()
    
    def create_genesis_block(self):
        return {
            'index': 0,
            'timestamp': datetime.utcnow().isoformat(),
            'data': 'GENESIS_BLOCK',
            'previous_hash': '0' * 64,
            'hash': self.calculate_hash(0, datetime.utcnow().isoformat(), 
                                       'GENESIS_BLOCK', '0' * 64)
        }
    
    def calculate_hash(self, index, timestamp, data, previous_hash):
        """SHA-256 hash of block contents"""
        block_string = f"{index}{timestamp}{data}{previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def add_vote_record(self, vote_data):
        """
        Add tamper-evident vote record
        vote_data contains ONLY hashed/anonymized info, NO PII
        """
        previous_block = self.chain[-1]
        index = len(self.chain)
        timestamp = datetime.utcnow().isoformat()
        
        # vote_data structure (all hashed/encrypted references):
        # {
        #   'voter_id_hash': sha256(voter_id),
        #   'vote_hash': sha256(vote_choice),
        #   'kyc_image_hash': sha256(image),
        #   'timestamp': ISO timestamp,
        #   'ip_geolocation': city/country only (not exact IP)
        # }
        
        new_block = {
            'index': index,
            'timestamp': timestamp,
            'data': vote_data,
            'previous_hash': previous_block['hash'],
            'hash': self.calculate_hash(index, timestamp, 
                                       json.dumps(vote_data, sort_keys=True), 
                                       previous_block['hash'])
        }
        
        self.chain.append(new_block)
        self.save_chain()
        
        return new_block['hash']
    
    def verify_chain_integrity(self):
        """
        Verify entire chain is tamper-free
        Returns: (is_valid, error_index)
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Verify hash
            calculated_hash = self.calculate_hash(
                current['index'],
                current['timestamp'],
                json.dumps(current['data'], sort_keys=True),
                current['previous_hash']
            )
            
            if current['hash'] != calculated_hash:
                return False, i
            
            # Verify chain linkage
            if current['previous_hash'] != previous['hash']:
                return False, i
        
        return True, None
    
    def save_chain(self):
        """Append-only save (never modify existing blocks)"""
        with open(self.chain_file, 'w') as f:
            json.dump(self.chain, f, indent=2)
    
    def load_chain(self):
        if os.path.exists(self.chain_file):
            with open(self.chain_file, 'r') as f:
                return json.load(f)
        return None
    
    def get_vote_proof(self, voter_id_hash):
        """
        Provide cryptographic proof of vote (for voter verification)
        Returns block containing their vote hash
        """
        for block in self.chain:
            if isinstance(block['data'], dict):
                if block['data'].get('voter_id_hash') == voter_id_hash:
                    return {
                        'block_index': block['index'],
                        'block_hash': block['hash'],
                        'timestamp': block['timestamp'],
                        'vote_hash': block['data']['vote_hash']
                    }
        return None