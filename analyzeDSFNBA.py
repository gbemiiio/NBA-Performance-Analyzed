import sqlite3
import pandas as pd

conn = sqlite3.connect("nba_team_scoring.db")

#How many games per team?

query = """
SELECT
    team,
    COUNT(*) AS games_played
FROM team_game_scoring
GROUP BY team
ORDER BY games_played DESC;
"""
df = pd.read_sql_query(query, conn)
print(df)

#average scoring breakdown by team 
query = """
SELECT
    team,
    ROUND(AVG(pctpts_2pt), 2) AS avg_2pt,
    ROUND(AVG(pctpts_3pt), 2) AS avg_3pt,
    ROUND(AVG(pctpts_pitp), 2) AS avg_paint
FROM team_game_scoring
GROUP BY team
ORDER BY avg_3pt DESC;
"""
df = pd.read_sql_query(query, conn)
print(df)

#do teams win more when they rely on 3pt shooting?
query = '''
SELECT
    "w/l",
    ROUND(AVG(pctpts_3pt), 2) AS avg_3pt_scoring,
    ROUND(AVG(pctpts_pitp), 2) AS avg_paint_scoring
FROM team_game_scoring
GROUP BY "w/l";
'''
df = pd.read_sql_query(query, conn)
print(df)

#high 3pt games, are they more likely to win?
query = '''
SELECT
    CASE 
        WHEN pctpts_3pt > 40 THEN 'High 3PT'
        ELSE 'Normal 3PT'
    END AS three_pt_category,
    "w/l",
    COUNT(*) AS games
FROM team_game_scoring
GROUP BY three_pt_category, "w/l";
'''
df = pd.read_sql_query(query, conn)
print(df)

#teams more dependent on paint scoring
query = """
SELECT
    team,
    ROUND(AVG(pctpts_pitp), 2) AS avg_paint_scoring
FROM team_game_scoring
GROUP BY team
ORDER BY avg_paint_scoring DESC
LIMIT 5;
"""
df = pd.read_sql_query(query, conn)
print(df)

#win rate by team 
query = '''
SELECT
    team,
    ROUND(
        SUM(CASE WHEN "w/l" = 'W' THEN 1 ELSE 0 END) * 1.0 /
        COUNT(*),
        2
    ) AS win_rate
FROM team_game_scoring
GROUP BY team
ORDER BY win_rate DESC;
'''
df = pd.read_sql_query(query, conn)
print(df)

#visualization of win rate by team
import matplotlib.pyplot as plt

df.plot(kind="bar", x="team", y="win_rate")
plt.title("Win Rate by Team")
plt.ylabel("Win Rate")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

conn.close()
