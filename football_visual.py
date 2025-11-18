# visualizations.py
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect('player_finance.db')

# 1. Top 10 most valuable players
top_players = pd.read_sql("""
    SELECT name, value_euro, wage_euro, overall_rating, positions
    FROM players 
    ORDER BY value_euro DESC 
    LIMIT 10
""", conn)

plt.figure(figsize=(12, 6))
sns.barplot(data=top_players, x='value_euro', y='name', hue='positions')
plt.title('Top 10 Most Valuable Players')
plt.xlabel('Market Value (€)')
plt.ticklabel_format(style='plain', axis='x')
plt.tight_layout()
plt.show()

# 2. Value distribution by age group
age_value = pd.read_sql("""
    SELECT age, AVG(value_euro) as avg_value
    FROM players
    WHERE value_euro > 0
    GROUP BY age
    ORDER BY age
""", conn)

plt.figure(figsize=(12, 6))
plt.plot(age_value['age'], age_value['avg_value'], marker='o')
plt.title('Average Player Value by Age')
plt.xlabel('Age')
plt.ylabel('Average Value (€)')
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. Skill rating vs Market value
skill_value = pd.read_sql("""
    SELECT overall_rating, AVG(value_euro) as avg_value
    FROM players
    GROUP BY overall_rating
    ORDER BY overall_rating
""", conn)

plt.figure(figsize=(12, 6))
plt.scatter(skill_value['overall_rating'], skill_value['avg_value'], alpha=0.7)
plt.title('Player Skill Rating vs Market Value')
plt.xlabel('Overall Rating')
plt.ylabel('Average Market Value (€)')
plt.grid(True)
plt.tight_layout()
plt.show()

conn.close()