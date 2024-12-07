API Documentation
Overview
This document provides an overview of the available API endpoints for the File Security and Sharing project. The API allows users to upload, scan, and retrieve files using the VirusTotal and Hybrid Analysis engines.
Base URL
http://<your-domain-or-localhost>:<port>/
Endpoints
1. Home Page
GET /
Description:
Returns the main HTML page of the web interface.
Request Example:
GET /
Response Example:
Returns an HTML page.
2. Upload File
POST /upload
Description:
Uploads a file to be scanned using VirusTotal or Hybrid Analysis.
Request Parameters:
• file (form-data) – The file to upload.
Example Request (using curl):
curl -X POST "http://localhost:8000/upload" \
    -F "file=@/path/to/your/file.exe"
Response Example:
{
   "message": "File scanned successfully.",
   "status": "safe"
}
Possible Statuses:
• "safe" – No threats detected.
• "malicious" – Threats detected.
• "uploaded" – File uploaded to VirusTotal for analysis.
• "error" – An error occurred during the upload or scan process.
3. List Files
GET /files
Description:
Lists all files that are marked as trusted (clean) and available for download.
Request Example:
GET /files
Response Example:
[
   {
       "name": "file1.exe",
       "link": "/download/file1.exe"
   },
   {
       "name": "file2.doc",
       "link": "/download/file2.doc"
   }
]
4. Download File
GET /download/{file_name}
Description:
Downloads a specific file from the trusted folder.
Path Parameter:
• file_name – The name of the file to download.
Request Example:
GET /download/file1.exe
Response:
Returns the file for download.
Error Response:
{
   "error": "File not found"
}
Error Responses
For all endpoints, the API returns error responses in the following format:
{
   "error": "Description of the error"
}
Common Errors:
• 400 Bad Request – Invalid request parameters.
• 404 Not Found – Resource not found.
• 500 Internal Server Error – Unexpected server error.
Notes
• Ensure that API keys for VirusTotal and Hybrid Analysis are correctly configured in the config.env file.
• The upload folder is limited to specific file types for security purposes.
Example config.env
vt_api_key=your_virustotal_api_key
ha_api_key=your_hybrid_analysis_api_key
