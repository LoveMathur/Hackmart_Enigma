# excel_manager.py
import pandas as pd
from datetime import datetime
import os

class ExcelManager:
    def __init__(self, voter_registry_excel, vote_records_excel, candidates_excel):
        self.voter_registry_excel = voter_registry_excel
        self.vote_records_excel = vote_records_excel
        self.candidates_excel = candidates_excel
        self.voter_db = None
        self.vote_records_db = None
        self.candidates_db = None
    
    def load_voter_registry(self):
        """
        Load existing voter database from Excel
        Expected columns: VoterID, Name, DOB, Email, Phone, Address
        """
        try:
            # Use openpyxl engine with read_only=False for better file handling
            self.voter_db = pd.read_excel(self.voter_registry_excel, engine='openpyxl')
            required_cols = ['VoterID', 'Name', 'DOB', 'Email']
            
            if not all(col in self.voter_db.columns for col in required_cols):
                raise ValueError(f"Excel must contain columns: {required_cols}")
            
            # Add HasVoted column if not exists
            if 'HasVoted' not in self.voter_db.columns:
                self.voter_db['HasVoted'] = False
            
            return True, len(self.voter_db)
        except PermissionError:
            print("ERROR: voter_registry.xlsx is locked. Please close Excel and restart the server.")
            return False, "File is locked by another process"
        except Exception as e:
            return False, str(e)
    
    def load_candidates(self):
        """Load candidates from Excel"""
        try:
            self.candidates_db = pd.read_excel(self.candidates_excel, engine='openpyxl')
            required_cols = ['CandidateID', 'CandidateName', 'PoliticalParty']
            
            if not all(col in self.candidates_db.columns for col in required_cols):
                raise ValueError(f"Candidates Excel must contain columns: {required_cols}")
            
            return True, len(self.candidates_db)
        except Exception as e:
            print(f"Error loading candidates: {e}")
            return False, str(e)
    
    def get_candidates(self):
        """Return list of candidates"""
        if self.candidates_db is None:
            self.load_candidates()
        
        return self.candidates_db.to_dict('records')
    
    def load_vote_records(self):
        """Load existing vote records"""
        try:
            if os.path.exists(self.vote_records_excel):
                self.vote_records_db = pd.read_excel(self.vote_records_excel, engine='openpyxl')
            else:
                # Create empty dataframe with required columns
                self.vote_records_db = pd.DataFrame(columns=[
                    'VoterID', 'VoterName', 'CandidateVoted', 'Timestamp', 
                    'IPAddress', 'GeolocationCity', 'GeolocationCountry',
                    'VotedStatus', 'KYCImageHash', 'BlockHash', 'VoteHash'
                ])
            return True
        except Exception as e:
            print(f"Error loading vote records: {e}")
            return False
    
    def export_vote_log(self, vote_records):
        """
        Export comprehensive vote log to Excel (DEPRECATED - use add_vote_record instead)
        vote_records format: list of dicts with:
        - Name, VoterID, Vote, Timestamp, Geolocation, KYCImageHash
        """
        df = pd.DataFrame(vote_records)
        
        # Reorder columns for clarity
        column_order = [
            'Timestamp',
            'VoterID',
            'Name',
            'Vote',
            'GeolocationCity',
            'GeolocationCountry',
            'KYCImageHash',
            'BlockHash',
            'VoteHash'
        ]
        
        df = df[column_order]
        
        # Format timestamp
        df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.strftime(
            '%Y-%m-%d %H:%M:%S'
        )
        
        # Create Excel writer with formatting
        with pd.ExcelWriter(self.vote_records_excel, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Vote Log', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Vote Log']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        return True
    
    def add_vote_record(self, voter_id, voter_name, candidate_voted, ip_address, 
                        geolocation_city, geolocation_country, kyc_image_hash, 
                        block_hash, vote_hash):
        """
        Add a new vote record to the vote_records.xlsx file
        """
        try:
            # Load existing records
            if self.vote_records_db is None:
                self.load_vote_records()
            
            # Create new record
            new_record = {
                'VoterID': voter_id,
                'VoterName': voter_name,
                'CandidateVoted': candidate_voted,
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'IPAddress': ip_address,
                'GeolocationCity': geolocation_city,
                'GeolocationCountry': geolocation_country,
                'VotedStatus': True,
                'KYCImageHash': kyc_image_hash,
                'BlockHash': block_hash,
                'VoteHash': vote_hash
            }
            
            # Append to dataframe
            self.vote_records_db = pd.concat([
                self.vote_records_db, 
                pd.DataFrame([new_record])
            ], ignore_index=True)
            
            # Save to Excel with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    self.vote_records_db.to_excel(self.vote_records_excel, index=False, engine='openpyxl')
                    print(f"✓ Vote record added for {voter_id}")
                    return True
                except PermissionError as e:
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(0.5)
                        continue
                    else:
                        print(f"Warning: Could not update vote records Excel: {e}")
                        return False
        except Exception as e:
            print(f"Error adding vote record: {e}")
            return False
    
    def mark_voter_as_voted(self, voter_id):
        """Update voter registry to prevent duplicate votes"""
        try:
            self.voter_db.loc[
                self.voter_db['VoterID'] == voter_id, 
                'HasVoted'
            ] = True
            
            # Save updated registry with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    self.voter_db.to_excel(self.voter_registry_excel, index=False, engine='openpyxl')
                    return True
                except PermissionError as e:
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(0.5)  # Wait 500ms before retry
                        continue
                    else:
                        # If all retries fail, log but don't crash
                        print(f"Warning: Could not update Excel file: {e}")
                        print("Vote is still recorded in memory and blockchain")
                        return False
        except Exception as e:
            print(f"Error in mark_voter_as_voted: {e}")
            return False
    
    def update_candidate_vote_count(self, candidate_name):
        """Update vote count for a candidate"""
        try:
            if self.candidates_db is None:
                self.load_candidates()
            
            # Find and increment vote count
            mask = self.candidates_db['CandidateName'] == candidate_name
            if mask.any():
                self.candidates_db.loc[mask, 'VoteCount'] = \
                    self.candidates_db.loc[mask, 'VoteCount'] + 1
                
                # Save with retry logic
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        self.candidates_db.to_excel(self.candidates_excel, index=False, engine='openpyxl')
                        return True
                    except PermissionError:
                        if attempt < max_retries - 1:
                            import time
                            time.sleep(0.5)
                            continue
                        else:
                            print(f"Warning: Could not update candidates Excel")
                            return False
            return False
        except Exception as e:
            print(f"Error updating candidate vote count: {e}")
            return False