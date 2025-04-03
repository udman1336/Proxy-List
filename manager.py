import os
import subprocess
import threading
import time
import git
import schedule
import shutil

REPO_PATH = "/root/Proxy-List"
OUTPUT_DIR = "/root/ProxyCheck/out/"

def run_scraper():
    """Runs the proxy scraper in a separate thread"""
    while True:
        print("[*] Starting Proxy Scraper...")
        subprocess.run(["sh", "start.sh"], cwd="/root/ProxyCheck")
        print("[*] Scraper finished. Waiting 30 minutes before next run...")

def copy_json_files(src_dir, dest_dir):
    """Copies all .json files from src_dir to dest_dir, including subdirectories"""
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                # Create the corresponding path in the destination directory
                dest_path = os.path.join(dest_dir, os.path.relpath(root, src_dir), file)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)  # Create directories if they don't exist
                shutil.copy(file_path, dest_path)  # Copy the file

        # Add directories if they are empty, GitHub will not track empty directories
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            dest_dir_path = os.path.join(dest_dir, os.path.relpath(dir_path, src_dir))
            os.makedirs(dest_dir_path, exist_ok=True)

def upload_to_github():
    """Uploads all .json files and directories containing them from OUTPUT_DIR to GitHub"""
    try:
        repo = git.Repo(REPO_PATH)
        repo.git.pull()

        # Copy all .json files from OUTPUT_DIR to the repository
        copy_json_files(OUTPUT_DIR, REPO_PATH)

        repo.git.add(A=True)  # Adds all new or modified files
        repo.index.commit("Updated proxy list with latest .json files and folders")
        origin = repo.remote(name="origin")
        origin.push()

        print("[+] All .json files and directories uploaded successfully.")
    except Exception as e:
        print(f"[!] Error uploading to GitHub: {e}")

# Uncomment this line to run the scraper in a separate thread
# threading.Thread(target=run_scraper, daemon=True).start()

# Start uploading files initially
upload_to_github()

# Schedule the upload every 30 minutes
# schedule.every(30).minutes.do(upload_to_github)

while True:
    schedule.run_pending()
    time.sleep(10)
