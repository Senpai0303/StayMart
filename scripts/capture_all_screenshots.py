import os
import subprocess
import json
import urllib.parse
import urllib.request
import time
import shutil

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE_TEMP = r"C:\Users\divya\AppData\Local\Temp"
OUTPUT_DIR = r"D:\Mini5th\report\screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_auth(email, password):
    req = urllib.request.Request(
        'http://localhost:8080/api/auth/login',
        data=json.dumps({'email': email, 'password': password}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode('utf-8'))
    return data['data']['token'], json.dumps(data['data']['user'])

print("Logging in as Admin...")
admin_token, admin_user = get_auth("admin@staymart.com", "Admin@123")

print("Logging in as User...")
user_token, user_user = get_auth("rohit.rawat@staymart.com", "User@123")

pages = [
    # Public pages (use guest session)
    ("landing_page.png", "http://localhost:5500/index.html?v=" + str(int(time.time())), 1400, 1000, 3500, False),
    ("search_properties.png", "http://localhost:5500/search-properties.html?v=" + str(int(time.time())), 1400, 950, 4000, False),
    ("search_products.png", "http://localhost:5500/search-products.html?v=" + str(int(time.time())), 1400, 950, 4000, False),
    ("property_detail.png", "http://localhost:5500/property-detail.html?id=1&v=" + str(int(time.time())), 1400, 1000, 4000, False),
    ("product_detail.png", "http://localhost:5500/product-detail.html?id=5&v=" + str(int(time.time())), 1400, 1000, 4000, False),
    ("login_page.png", "http://localhost:5500/login.html?v=" + str(int(time.time())), 1400, 850, 2500, False),
    ("register_page.png", "http://localhost:5500/register.html?v=" + str(int(time.time())), 1400, 900, 2500, False),
    ("swagger_api.png", "http://localhost:8080/swagger-ui.html", 1400, 950, 4000, False),

    # Admin pages (authenticated)
    ("admin_dashboard.png", f"http://localhost:5500/auth-bridge.html?token={admin_token}&user={urllib.parse.quote(admin_user)}&to=pages/admin/dashboard.html", 1400, 1000, 5000, True),
    ("admin_pending_properties.png", f"http://localhost:5500/auth-bridge.html?token={admin_token}&user={urllib.parse.quote(admin_user)}&to=pages/admin/pending-properties.html", 1400, 950, 4000, True),
    ("admin_all_users.png", f"http://localhost:5500/auth-bridge.html?token={admin_token}&user={urllib.parse.quote(admin_user)}&to=pages/admin/all-users.html", 1400, 950, 4000, True),

    # User pages (authenticated)
    ("user_dashboard.png", f"http://localhost:5500/auth-bridge.html?token={user_token}&user={urllib.parse.quote(user_user)}&to=pages/user/dashboard.html", 1400, 950, 4000, True),
    ("post_property.png", f"http://localhost:5500/auth-bridge.html?token={user_token}&user={urllib.parse.quote(user_user)}&to=post-property.html", 1400, 1000, 4000, True),
    ("post_product.png", f"http://localhost:5500/auth-bridge.html?token={user_token}&user={urllib.parse.quote(user_user)}&to=post-product.html", 1400, 1000, 4000, True),
    ("user_bookings.png", f"http://localhost:5500/auth-bridge.html?token={user_token}&user={urllib.parse.quote(user_user)}&to=pages/user/bookings.html", 1400, 950, 4000, True),
    ("user_chat.png", f"http://localhost:5500/auth-bridge.html?token={user_token}&user={urllib.parse.quote(user_user)}&to=pages/user/chat.html", 1400, 950, 4000, True)
]

for filename, url, width, height, budget, is_auth in pages:
    profile_dir = os.path.join(BASE_TEMP, f"chrome_prof_{'auth' if is_auth else 'guest'}")
    if not is_auth and os.path.exists(profile_dir):
        shutil.rmtree(profile_dir, ignore_errors=True)
    os.makedirs(profile_dir, exist_ok=True)

    out_path = os.path.join(OUTPUT_DIR, filename)
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--disable-application-cache",
        "--disk-cache-size=1",
        f"--window-size={width},{height}",
        f"--virtual-time-budget={budget}",
        f"--user-data-dir={profile_dir}",
        f"--screenshot={out_path}",
        url
    ]
    print(f"Capturing {filename}...")
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        print(f"  -> Saved {filename} ({size} bytes)")
    else:
        print(f"  FAILED to capture {filename}")

print("All screenshots captured successfully!")
