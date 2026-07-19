import sqlite3

conn = sqlite3.connect("sec_rag.db")
tables = conn.execute("SELECT * FROM sqlite_master WHERE type='table';").fetchall()
print(tables)
conn.close()