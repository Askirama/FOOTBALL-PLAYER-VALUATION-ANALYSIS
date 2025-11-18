# quick_exploration.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("/Users/abubakaraskirama/Documents/Football_analysis/fifa_players.csv")  # Adjust filename as needed

print("=== DATASET OVERVIEW ===")
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Check financial columns
financial_cols = ['value_euro', 'wage_euro', 'release_clause_euro']
print(f"\nFinancial columns sample:")
print(df[financial_cols].head())

print(f"\nData types:")
print(df[financial_cols].dtypes)