import pandas as pd
from datetime import datetime

# ============================================
# 1. Voter Registry (already exists, but let's ensure it has the right structure)
# ============================================
print("Creating voter_registry.xlsx...")
voter_data = {
    'VoterID': ['V001', 'V002', 'V003', 'V004', 'V005'],
    'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
    'DOB': ['1990-01-15', '1985-05-20', '1992-03-10', '1988-11-30', '1995-07-25'],
    'Email': ['john.doe@example.com', 'jane.smith@example.com', 'bob.johnson@example.com', 
              'alice.brown@example.com', 'charlie.wilson@example.com'],
    'Phone': ['+1-555-0001', '+1-555-0002', '+1-555-0003', '+1-555-0004', '+1-555-0005'],
    'Address': ['123 Main St', '456 Oak Ave', '789 Pine Rd', '321 Elm St', '654 Maple Dr'],
    'HasVoted': [False, False, False, False, False]
}
df_voters = pd.DataFrame(voter_data)
df_voters.to_excel('voter_registry.xlsx', index=False, engine='openpyxl')
print(f"✓ voter_registry.xlsx created with {len(df_voters)} voters")

# ============================================
# 2. Vote Records (who voted, when, for whom, etc.)
# ============================================
print("\nCreating vote_records.xlsx...")
vote_records_data = {
    'VoterID': [],
    'VoterName': [],
    'CandidateVoted': [],
    'Timestamp': [],
    'IPAddress': [],
    'GeolocationCity': [],
    'GeolocationCountry': [],
    'VotedStatus': [],
    'KYCImageHash': [],
    'BlockHash': [],
    'VoteHash': []
}
df_vote_records = pd.DataFrame(vote_records_data)
df_vote_records.to_excel('vote_records.xlsx', index=False, engine='openpyxl')
print("✓ vote_records.xlsx created (empty, will be populated as votes are cast)")

# ============================================
# 3. Candidates Registry
# ============================================
print("\nCreating candidates.xlsx...")
candidates_data = {
    'CandidateID': ['C001', 'C002', 'C003'],
    'CandidateName': ['Candidate A', 'Candidate B', 'Candidate C'],
    'PoliticalParty': ['Democratic Party', 'Republican Party', 'Independent'],
    'PartySymbol': ['🔵 Donkey', '🔴 Elephant', '⭐ Star'],
    'VoteCount': [0, 0, 0],
    'Slogan': ['Together We Progress', 'Freedom and Prosperity', 'Voice of the People']
}
df_candidates = pd.DataFrame(candidates_data)
df_candidates.to_excel('candidates.xlsx', index=False, engine='openpyxl')
print(f"✓ candidates.xlsx created with {len(df_candidates)} candidates")

print("\n" + "="*50)
print("All Excel files created successfully!")
print("="*50)
print("\nFiles created:")
print("1. voter_registry.xlsx - Voter information")
print("2. vote_records.xlsx - Vote transaction records")
print("3. candidates.xlsx - Candidate information")
print("\nYou can now restart the Flask application.")
