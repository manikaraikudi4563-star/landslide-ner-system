import sqlite3
import json

conn = sqlite3.connect("app/landslide_ner.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]

print("=== ACTUAL DATABASE TABLES ===")
for tbl in tables:
    cursor.execute(f"PRAGMA table_info({tbl})")
    cols = [r[1] for r in cursor.fetchall()]
    cursor.execute(f"SELECT COUNT(*) FROM {tbl}")
    count = cursor.fetchone()[0]
    print(f"Table: {tbl} | Rows: {count} | Columns: {len(cols)} -> {', '.join(cols)}")

cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND sql IS NOT NULL")
indexes = cursor.fetchall()
print("\n=== ACTUAL INDEXES ===")
for idx in indexes:
    print(f"Index: {idx[0]} -> {idx[1]}")

conn.close()
