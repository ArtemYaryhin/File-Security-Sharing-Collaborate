import sqlite3
import os
from datatime import datetime

DB_NAME = "fsss_scanner.db"

def init_db():
	"""Initialize the databse and create necessary tables if they don't exist"""
	conn = sqlite3.connect(DB_NAME)
	cursor = conn.cursor()
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS file_reposrts(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		file_hash TEXT UNIQUE,
		file_name TEXT,
		scan_result TEXT,
		scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
		''')
	conn.commit()
	conn.close()

def save_scan_result(file_hash, file_name, scan_result):
	"""Save the scan result to the database"""
	conn = sqlite3.connect(DB_NAME)
	cursor = conn.cursor()
	try:
		cursor.execute('''
		INSERT INTO file_reports (file_hash, file_name, scan_result)
		VALUES (?, ?, ?)
		''', (file_hash, file_name, scan_result))
		conn.commit()
	except sqlite3.IntegrityError:
		print(f"Record with hash {file_hash} already exists")
	finally:
			conn.close()

def is_file_clean(file_hash):
	"""Check if a file with the given hash is marked as clean in the databse"""
	conn = sqlite3.connect(DB_NAME)
	cursor = conn.cursor()
	cursor.execute('''
	SELECT scan_result FROM file_reports WHERE file_hash = ?
	''', (file_hash,))
	result = cursor.fetchone()
	conn.close()
	return result is not None and result[0] == "clean"

def get_all_reports():
	"""Retrieve all scan reports from the database"""
	conn = sqlite3.connect(DB_NAME)
	cursor = conn.cursor()
	cursor.execute('SELECT file_hash, file_name, scan_result, scanned_at FROM file_reports')
	reports = cursor.fetchall()
	conn.close()
	return reports

if __name__ == "__main__":
	init_db()
	print("Database initialized successfully")
