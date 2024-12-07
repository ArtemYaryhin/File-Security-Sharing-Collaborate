import cmd
import os
import asyncio
from backend.scan_engines import scan_file
from utils import ensure_folder_exists, log_info, log_error  

UPLOAD_FOLDER = "uploaded_files"

class AnalyzerShell(cmd.Cmd):
    intro = "Welcome to the FSS Analyzer CLI. Type 'help' or '?' to list commands.\n"
    prompt = "(analyzer) > "

    def __init__(self):
        super().__init__()
        ensure_folder_exists(UPLOAD_FOLDER)

    def do_scan(self, line):
        """Scan a file using VirusTotal or Hybrid Analysis.
        Usage: scan <file_path> --engine <vt|ha>
        Options:
          file_path    Path to the file to scan.
          --engine     Select 'vt' for VirusTotal or 'ha' for Hybrid Analysis. Default is 'vt'.
        Example:
          scan test.exe --engine vt
        """

        args = line.split()
        if not args:
            log_error("No file path provided. Usage: scan <file_path> --engine <vt|ha>")
            return

        file_path = args[0]
        engine = "vt"  # Default engine
        if "--engine" in args:
            engine_index = args.index("--engine") + 1
            if engine_index < len(args):
                engine = args[engine_index].lower()
            else:
                log_error("No engine specified after '--engine'. Defaulting to 'vt'.")

        if not os.path.isfile(file_path):
            log_error(f"File not found: {file_path}")
            return

        log_info(f"Scanning {file_path} with {engine.upper()} engine...")
        asyncio.run(self.scan_file(file_path, engine))

    async def scan_file(self, file_path, engine):
        try:
            result = await scan_file(file_path, engine)
            if result["status"] == "found":
                print(f"\nScan Result: {result['result']}")
            elif result["status"] == "uploaded":
                print(f"\n{result['result']}")
            else:
                log_error(f"Scan Error: {result['message']}")
        except Exception as e:
            log_error(f"Error scanning file: {e}")

    def do_exit(self, line):
        """Exit the Malware Analyzer CLI."""
        print("Exiting the Malware Analyzer CLI. Goodbye!")
        return True

    def do_clear(self, line):
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    AnalyzerShell().cmdloop() 
