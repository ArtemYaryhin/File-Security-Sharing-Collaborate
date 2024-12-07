import hashlib
import mimetypes
from msilib.schema import MIME
import os
import logging
from pathlib import Path

from charset_normalizer import is_binary

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def calculate_file_hash(file_paath):
	"""Calculate and return the SHA-256 hash of a file"""
	sha256_hash = hashlib.sha256()
	try:
		with open(file_path, "rb") as f:
			for byte_block in iter(lambda: f.read(4096), b""):
				sha256_hash.update(byte_block)
			return sha256_hash.hexdigest()
	except FileNotFoundError:
			logger.error(f"Error calculating hash for {file_path}: {e}")
			return None

def is_binary_file(file_path):
	"""Check if the file is a binary file based on its MIME type"""
	mime_type, _ = mimetypes.guess_type(file_path)
	return mime_type is None or mime_type.startswith('application/')

def is_pe_file(file_path):
	"""Check if the file is a Windows Portable Executable (PE) file"""
	try:
		with open(file_path, 'rb') as f:
			return f.read(2) == b'MZ'
	except Exception as e:
		logger.error(f"Error checking if file is PE file: {e}")
		return False

def ensure_folder_exists(folder_path):
	"""Ensure the spcified folder eexists; create it if it doesn't"""
	Path(folder_path).mkdir(parents=True, exist_ok=True)
	logger.info(f"Ensured folder exists: {folder_path}")

def batch_files(files, batch_size):
	"""Yield successive batches of files of the specified size"""
	for i in range(0, len(files), batch_size):
		yield files[i:i + batch_size]

def log_error(message):
	"""Log an error message"""
	logger.error(message)

def log_info(message):
	"""log an info message"""
	logger.info(message)

if __name__ == "__main__":
	test_file = "test.exe"
	ensure_folder_exists("uploaded_files")
	file_hash = calculate_file_hash(test_file)
	if file_hash:
		log_info(f"SHA-256 hash of {test_file}: {file_hash}")
