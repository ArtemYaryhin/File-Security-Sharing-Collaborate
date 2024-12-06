import hashlib
import aiohttp
import os

VT_API_KEY = os.getenv("vt_api_key")
VT_URL = "https://www.virustotal.com/api/v3/files"
VT_HEADERS = {"x-apikey": VT_API_KEY}
HA_URL = "https://www.hybrid-analysis.com/api/v2"
HA_API_KEY = os.getenv("ha_api_key")
HA_HEADERS = {"api-key": HA_API_KEY}

async def calculate_file_hash(file_path):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

async def scan_with_virustotal(file_path):
    """Scan a file using VirusTotal."""
    file_hash = await calculate_file_hash(file_path)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{VT_URL}/{file_hash}", headers=VT_HEADERS) as response:
            if response.status == 200:
                result = await response.json()
                stats = result.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                return {"status": "found", "result": stats}
            elif response.status == 404:
                with open(file_path, "rb") as f:
                    files = {"file": f}
                    async with session.post(VT_URL, headers=VT_HEADERS, data=files) as upload_response:
                        if upload_response.status == 200:
                            return {"status": "uploaded", "result": "File uploaded to VirusTotal for analysis."}
                        else:
                            return {"status": "error", "message": await upload_response.text()}
            else:
                return {"status": "error", "message": f"Error: {response.status}"}

async def scan_with_hybrid_analysis(file_path):
    """Scan a file using Hybrid Analysis."""
    file_size = os.path.getsize(file_path)
    if file_size > 100 * 1024 * 1024:
        return {"status": "error", "message": "File exceeds maximum upload size for Hybrid Analysis (100 MB)"}

    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            files = {"file": f}
            async with session.post(f"{HA_URL}/quick-scan/file", headers=HA_HEADERS, data=files) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "status": "success",
                        "result": {
                            "verdict": result.get("verdict"),
                            "threat_score": result.get("threat_score"),
                            "scanners": result.get("scanners", []),
                        },
                    }
                else:
                    return {"status": "error", "message": f"Error from Hybrid Analysis: {response.status}"}

async def scan_file(file_path, engine="vt"):
    """Scan a file using the specified engine."""
    if engine == "vt":
        return await scan_with_virustotal(file_path)
    elif engine == "ha":
        return await scan_with_hybrid_analysis(file_path)
    else:
        return {"status": "error", "message": "Unsupported engine"} 