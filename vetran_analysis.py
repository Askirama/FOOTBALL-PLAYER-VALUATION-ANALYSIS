# veteran_visualizations.py
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_all_visualizations():
    # Create images folder if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')
    
    conn = sqlite3.connect('player_finance.db')
    
    # Get the data
    veterans_query = """
    SELECT name, age, positions, value_euro, wage_euro, overall_rating,
           (overall_rating * 1000000) as expected_value,
           (overall_rating * 1000000 - value_euro) as value_gap,
           ROUND(value_euro / NULLIF(wage_euro, 0), 2) as value_ratio
    FROM players
    WHERE age >= 30 AND overall_rating >= 75 AND value_euro > 0 AND wage_euro > 0
    ORDER BY value_gap DESC
    LIMIT 25
    """
    
    comparison_query = """
    SELECT 
        CASE 
            WHEN age >= 30 THEN 'Veteran (30+)'
            WHEN age <= 23 THEN 'Young (23-)'
            ELSE 'Prime (24-29)'
        END as age_group,
        ROUND(AVG(value_euro / NULLIF(wage_euro, 0)), 2) as avg_value_ratio,
        ROUND(AVG(overall_rating / NULLIF(wage_euro, 0) * 1000), 2) as avg_performance_per_k
    FROM players
    WHERE value_euro > 0 AND wage_euro > 0
    GROUP BY age_group
    """
    
    veterans = pd.read_sql(veterans_query, conn)
    comparison = pd.read_sql(comparison_query, conn)
    conn.close()
    
    # Set style
    plt.style.use('seaborn-v0_8')
    
    # CHART 1: Top 10 Undervalued Veterans
    plt.figure(figsize=(12, 8))
    top_undervalued = veterans.head(10)
    bars = plt.barh(top_undervalued['name'], top_undervalued['value_gap'] / 1000000)
    plt.xlabel('Undervaluation (Millions €)')
    plt.title('Top 10 Most Undervalued Veterans\n(Expected Value vs Actual Value)')
    plt.bar_label(bars, fmt='€%.1fM')
    plt.tight_layout()
    plt.savefig('images/value_gap_chart.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # CHART 2: Value Efficiency by Age Group
    plt.figure(figsize=(10, 6))
    age_groups = comparison['age_group']
    value_ratios = comparison['avg_value_ratio']
    bars = plt.bar(age_groups, value_ratios, color=['red', 'blue', 'green'])
    plt.ylabel('Value per Wage Euro')
    plt.title('Value Efficiency by Age Group\n(Higher = Better Value)')
    plt.bar_label(bars, fmt='%.0f')
    plt.tight_layout()
    plt.savefig('images/value_efficiency_chart.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # CHART 3: Performance per €1000 Wage
    plt.figure(figsize=(10, 6))
    performance_data = comparison[['age_group', 'avg_performance_per_k']]
    bars = plt.bar(performance_data['age_group'], performance_data['avg_performance_per_k'],
                  color=['red', 'blue', 'green'])
    plt.ylabel('Performance Rating per €1000 Wage')
    plt.title('Cost Efficiency: Performance per Wage Spend')
    plt.bar_label(bars, fmt='%.1f')
    plt.tight_layout()
    plt.savefig('images/performance_efficiency_chart.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # CHART 4: Veteran Deals Scatter Plot
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(veterans['value_euro'] / 1000000, 
                         veterans['overall_rating'],
                         s=100, alpha=0.7, c=veterans['age'], cmap='viridis')
    plt.xlabel('Market Value (Millions €)')
    plt.ylabel('Skill Rating')
    plt.title('High-Skill Veterans: Value vs Rating\n(Bubble color = Age)')
    plt.colorbar(scatter, label='Age')
    
    # Add top 5 player names
    for i, row in veterans.head(5).iterrows():
        plt.annotate(row['name'], 
                    (row['value_euro'] / 1000000, row['overall_rating']),
                    xytext=(5, 5), textcoords='offset points', fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('images/veteran_deals_scatter.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ All charts saved to /images folder!")

if __name__ == "__main__":
    create_all_visualizations()