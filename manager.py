import os
import subprocess
import threading
import time
import git
import schedule

REPO_PATH = "/root/Proxy-List"
OUTPUT_DIR = "/root/ProxyCheck/out/"

def run_scraper():
    """Runs the proxy scraper in a separate thread"""
    while True:
        print("[*] Starting Proxy Scraper...")
        subprocess.run(["sh", "start.sh"], cwd="/root/ProxyCheck")
        print("[*] Scraper finished. Waiting 30 minutes before next run...")

def upload_to_github():
    """Uploads all files from OUTPUT_DIR to GitHub"""
    try:
        repo = git.Repo(REPO_PATH)
        repo.git.pull()
        
        for file in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, file)
            if os.path.isfile(file_path):
                os.system(f"cp {file_path} {REPO_PATH}/")

        repo.git.add(A=True)
        repo.index.commit("Updated proxy list with latest files")
        origin = repo.remote(name="origin")
        origin.push()
        
        print("[+] All proxy files uploaded successfully.")
    except Exception as e:
        print(f"[!] Error uploading to GitHub: {e}")

#threading.Thread(target=run_scraper, daemon=True).start()
upload_to_github()
#schedule.every(30).minutes.do(upload_to_github)

time.sleep(1800)

while True:
    schedule.run_pending()
    time.sleep(10)
