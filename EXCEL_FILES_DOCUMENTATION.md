# Three Excel Files System - Documentation

## Overview
The voting system now uses three separate Excel files for better organization and data management.

---

## 📋 File 1: voter_registry.xlsx
**Purpose**: Store voter registration information

**Columns**:
- `VoterID` - Unique voter identification (e.g., V001, V002)
- `Name` - Full name of the voter
- `DOB` - Date of birth (YYYY-MM-DD format)
- `Email` - Email address
- `Phone` - Phone number
- `Address` - Physical address
- `HasVoted` - Boolean (True/False) indicating if voter has cast their vote

**Usage**: 
- Used for voter authentication during login
- Updated when voter casts a vote (HasVoted = True)
- Read by: `auth_service.py`, `excel_manager.py`

---

## 📊 File 2: vote_records.xlsx
**Purpose**: Store detailed records of all votes cast

**Columns**:
- `VoterID` - ID of the voter who cast the vote
- `VoterName` - Name of the voter
- `CandidateVoted` - Name of the candidate voted for
- `Timestamp` - Date and time when vote was cast
- `IPAddress` - IP address from which vote was submitted
- `GeolocationCity` - City location (can be enhanced)
- `GeolocationCountry` - Country location (can be enhanced)
- `VotedStatus` - Always True (indicates vote was successfully cast)
- `KYCImageHash` - Hash of the KYC image for verification
- `BlockHash` - Blockchain hash for tamper evidence
- `VoteHash` - Hash of the vote for verification

**Usage**:
- New record added each time a vote is cast
- Provides complete audit trail
- Can be used for analysis and reporting
- Updated by: `excel_manager.add_vote_record()`

---

## 🎯 File 3: candidates.xlsx
**Purpose**: Store candidate information and vote counts

**Columns**:
- `CandidateID` - Unique candidate ID (e.g., C001, C002)
- `CandidateName` - Name shown to voters (e.g., Candidate A, Candidate B)
- `PoliticalParty` - Political party affiliation
- `PartySymbol` - Symbol/emoji for the party
- `VoteCount` - Running count of votes received (starts at 0)
- `Slogan` - Campaign slogan

**Usage**:
- Loaded dynamically in the voting page
- Vote count incremented when vote is cast
- Used for displaying results
- Read/Updated by: `excel_manager.py`

---

## 🔄 Data Flow

### Login Process:
1. User enters credentials
2. System checks `voter_registry.xlsx`
3. If valid, session created

### Voting Process:
1. User takes KYC photo
2. System loads candidates from `candidates.xlsx`
3. User selects candidate and submits
4. System:
   - Updates `HasVoted` in `voter_registry.xlsx`
   - Adds record to `vote_records.xlsx`
   - Increments `VoteCount` in `candidates.xlsx`
   - Creates blockchain entry

---

## 🛠️ Key Functions

### In excel_manager.py:

**`load_voter_registry()`**
- Loads voter_registry.xlsx
- Initializes voter database

**`load_candidates()`**
- Loads candidates.xlsx
- Returns candidate information

**`get_candidates()`**
- Returns list of all candidates
- Used by API endpoint

**`load_vote_records()`**
- Loads existing vote records
- Creates file if doesn't exist

**`add_vote_record(voter_id, voter_name, candidate_voted, ...)`**
- Adds new vote to vote_records.xlsx
- Includes all voting metadata

**`mark_voter_as_voted(voter_id)`**
- Updates HasVoted to True in voter_registry.xlsx
- Prevents duplicate voting

**`update_candidate_vote_count(candidate_name)`**
- Increments VoteCount in candidates.xlsx
- Tracks election results

---

## 🚀 Setup Instructions

1. Run the setup script:
   ```bash
   python create_excel_files.py
   ```

2. This creates:
   - ✅ voter_registry.xlsx (5 sample voters)
   - ✅ vote_records.xlsx (empty, will be populated)
   - ✅ candidates.xlsx (3 sample candidates)

3. Start the Flask server:
   ```bash
   python app.py
   ```

4. The system will automatically:
   - Load all three Excel files
   - Display candidates dynamically
   - Track all votes in real-time

---

## 📈 Benefits

1. **Separation of Concerns**: Each file has a specific purpose
2. **Better Organization**: Easy to understand and maintain
3. **Audit Trail**: Complete record of all transactions
4. **Real-time Results**: Vote counts updated automatically
5. **Scalability**: Easy to add more voters or candidates
6. **Data Integrity**: Multiple backups of voting data

---

## ⚠️ Important Notes

- Always close Excel files before running the application
- Files are updated with retry logic to handle locks
- Vote is recorded in blockchain even if Excel update fails
- All three files work together to maintain data consistency

---

## 🎉 Test Credentials

**Sample Voter**:
- Voter ID: V001
- DOB: 1990-01-15
- Email: john.doe@example.com

**Candidates**:
- Candidate A (Democratic Party)
- Candidate B (Republican Party)
- Candidate C (Independent)
