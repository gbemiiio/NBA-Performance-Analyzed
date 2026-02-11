import pandas as pd
import sqlite3

# -----------------------------
# Loading CSV data
# -----------------------------
df = pd.read_csv("games_scoring.csv")

# -----------------------------
# Cleaned column names
# -----------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("%", "pct")
)

print("Columns after cleaning:")
print(df.columns.tolist())

# -----------------------------
# Limiting to the first 500 rows
# -----------------------------
df = df.head(500)

# -----------------------------
# Select only useful columns & (Update names after cleaning)
# -----------------------------
columns_to_keep = [
    "team_id",
    "game_id",
    "team",
    "match_up",      
    "game_date",     
    "w/l",           
    "min",
    "pctpts_2pt",
    "pctpts_3pt",
    "pctpts_ft",
    "pctpts_pitp"
]

# Only keep columns that actually exist
columns_to_keep = [col for col in columns_to_keep if col in df.columns]

df = df[columns_to_keep]
print(df)
# -----------------------------
# Write to SQLite
# -----------------------------
conn = sqlite3.connect("nba_team_scoring.db")
df.to_sql("team_game_scoring", conn, if_exists="replace", index=False)
conn.close()

print("✅ Cleaned NBA team scoring data loaded into SQLite.")
