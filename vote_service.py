# vote_service.py
import hashlib
import json
from datetime import datetime
import requests

class VoteProcessor:
    def __init__(self, auth_service, kyc_service, tamper_chain):
        self.auth_service = auth_service
        self.kyc_service = kyc_service
        self.tamper_chain = tamper_chain
        self.votes_encrypted = {}  # voter_id_hash -> encrypted vote
    
    def process_vote(self, session_token, vote_choice, kyc_image_hash, ip_address):
        """
        Complete vote processing workflow
        Returns: (success, vote_receipt)
        """
        # 1. Verify session
        voter_info = self.auth_service.verify_session(session_token)
        if not voter_info:
            return False, {'error': 'Invalid session'}
        
        voter_id = voter_info['voter_id']
        
        # 2. Check duplicate vote (replay protection)
        voter_id_hash = hashlib.sha256(voter_id.encode()).hexdigest()
        if voter_id_hash in self.votes_encrypted:
            return False, {'error': 'Vote already recorded'}
        
        # 3. Hash vote choice (privacy)
        vote_hash = hashlib.sha256(
            f"{vote_choice}{voter_id}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()
        
        # 4. Get geolocation (IP-derived, city-level only)
        geolocation = self.get_geolocation(ip_address)
        
        # 5. Create tamper-evident record (NO PII)
        public_record = {
            'voter_id_hash': voter_id_hash,
            'vote_hash': vote_hash,
            'kyc_image_hash': kyc_image_hash,
            'timestamp': datetime.utcnow().isoformat(),
            'geolocation': geolocation  # City/country only
        }
        
        block_hash = self.tamper_chain.add_vote_record(public_record)
        
        # 6. Store encrypted vote mapping (for decryption if needed)
        encrypted_vote = self.auth_service.cipher.encrypt(
            json.dumps({
                'voter_id': voter_id,
                'voter_name': voter_info['name'],
                'vote_choice': vote_choice,
                'timestamp': public_record['timestamp'],
                'block_hash': block_hash
            }).encode()
        )
        self.votes_encrypted[voter_id_hash] = encrypted_vote
        
        # 7. Generate voter receipt
        receipt = {
            'voter_id_hash': voter_id_hash,
            'vote_hash': vote_hash,
            'block_hash': block_hash,
            'timestamp': public_record['timestamp'],
            'verification_url': f"/api/verify/{voter_id_hash}"
        }
        
        return True, receipt
    
    def get_geolocation(self, ip_address):
        """
        Get city/country from IP (privacy-preserving)
        Uses free IP geolocation service
        """
        try:
            # Example using ipapi.co (replace with preferred service)
            response = requests.get(f'https://ipapi.co/{ip_address}/json/', 
                                   timeout=2)
            data = response.json()
            return {
                'city': data.get('city', 'Unknown'),
                'country': data.get('country_name', 'Unknown')
            }
        except:
            return {'city': 'Unknown', 'country': 'Unknown'}