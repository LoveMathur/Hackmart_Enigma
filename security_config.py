# security_config.py
from cryptography.fernet import Fernet
import os

class SecurityConfig:
    """Centralized security configuration"""
    
    @staticmethod
    def generate_keys():
        """Generate encryption keys (run once during setup)"""
        keys = {
            'session_key': Fernet.generate_key(),
            'pii_encryption_key': Fernet.generate_key(),
            'vote_encryption_key': Fernet.generate_key()
        }
        
        # Store keys securely (environment variables or key management service)
        with open('.env.keys', 'wb') as f:
            for key_name, key_value in keys.items():
                f.write(f"{key_name}={key_value.decode()}\n".encode())
        
        os.chmod('.env.keys', 0o600)  # Restrict file permissions
        
        return keys
    
    @staticmethod
    def load_keys():
        """Load encryption keys from secure storage"""
        keys = {}
        with open('.env.keys', 'r') as f:
            for line in f:
                key_name, key_value = line.strip().split('=')
                keys[key_name] = key_value.encode()
        return keys

# Data classification rules
DATA_CLASSIFICATION = {
    'PUBLIC_CHAIN': [
        'voter_id_hash',  # SHA-256 hash, not reversible
        'vote_hash',       # SHA-256 hash of vote + salt
        'kyc_image_hash',  # SHA-256 hash of image
        'timestamp',       # ISO format
        'geolocation'      # City/country only, NO exact IP
    ],
    'ENCRYPTED_STORAGE': [
        'voter_id',        # Encrypted with PII key
        'voter_name',      # Encrypted with PII key
        'vote_choice',     # Encrypted with vote key
        'kyc_image',       # Encrypted image binary
        'email',           # Encrypted with PII key
        'ip_address'       # Encrypted, NEVER in public logs
    ],
    'EXCEL_OUTPUT': [
        'timestamp',
        'voter_id',        # Plain (authorized personnel only)
        'voter_name',      # Plain (authorized personnel only)
        'vote_choice',     # Plain (authorized personnel only)
        'geolocation_city',
        'geolocation_country',
        'kyc_image_hash',  # Hash reference to encrypted image
        'block_hash',      # Tamper-evidence proof
        'vote_hash'        # Verification hash
    ]
}