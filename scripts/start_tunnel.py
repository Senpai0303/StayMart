import subprocess
import re
import sys
import os
import time

CLOUDFLARED = os.path.abspath("bin/cloudflared.exe")
OUTPUT_FILE = os.path.abspath("LATEST_PUBLIC_URL.txt")
TARGET_PORT = 5500

def main():
    print(f"Starting Cloudflare Quick Tunnel for http://127.0.0.1:{TARGET_PORT}...")
    cmd = [
        CLOUDFLARED, "tunnel",
        "--url", f"http://127.0.0.1:{TARGET_PORT}",
        "--http2-origin"
    ]
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    
    url_found = None
    pattern = re.compile(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com')
    
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        print(line, end='', flush=True)
        m = pattern.search(line)
        if m and not url_found:
            url_found = m.group(0)
            print(f"\n" + "=" * 70, flush=True)
            print(f"*** STAYMART GLOBAL PUBLIC ACCESS URL: {url_found} ***", flush=True)
            print("=" * 70 + "\n", flush=True)
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                f.write(url_found)
                
    proc.wait()

if __name__ == '__main__':
    main()
