import pandas as pd

df = pd.read_excel('voter_registry.xlsx')
print("Voter Registry Data:")
print(df[['VoterID', 'DOB', 'Email']].head())
print("\nData types:")
print(df[['VoterID', 'DOB', 'Email']].dtypes)
print("\nSample DOB value:")
print(repr(df.iloc[0]['DOB']))
