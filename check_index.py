import os
import sys
import time
import argparse
import urllib.request
import urllib.parse
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def install_and_import(package, import_name=None):
    if not import_name:
        import_name = package
    try:
        return __import__(import_name)
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
        return __import__(import_name)

pd = install_and_import("pandas")
openpyxl = install_and_import("openpyxl")

# Safe console printing for Windows cp1252
def safe_print(msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", "ignore").decode("ascii"))

# ===============================================================
# SERPER GOOGLE SERP API ENGINE
# ===============================================================
def check_url_index_via_serper(serper_api_key, url):
    """Kiem tra index tren Google Search bang Serper API"""
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    payload = json.dumps({"q": f"site:{url}", "gl": "vn", "hl": "vi"}).encode("utf-8")
    
    for attempt in range(5):
        try:
            req = urllib.request.Request("https://google.serper.dev/search", headers=headers, data=payload)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                organic = data.get("organic", [])
                if organic:
                    return "Da index"
                return "Chua index"
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(1.0 * (attempt + 1))
            else:
                time.sleep(0.5)
        except Exception:
            time.sleep(0.5)
            
    return "Loi API"

# ===============================================================
# MAIN
# ===============================================================
def main():
    parser = argparse.ArgumentParser(description="Kiem tra trang thai index cua danh sach URL.")
    parser.add_argument("-f", "--file", type=str, help="Duong dan den file txt chua danh sach URL.")
    parser.add_argument("-u", "--urls", type=str, help="Danh sach URL, cach nhau boi dau phay.")
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    urls = []
    if args.file:
        if os.path.exists(args.file):
            with open(args.file, "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip()]
        else:
            safe_print(f"[-] File khong ton tai: {args.file}")
            sys.exit(1)
    elif args.urls:
        urls = [u.strip() for u in args.urls.split(",") if u.strip()]
    else:
        default_urls_file = os.path.join(script_dir, "urls.txt")
        if os.path.exists("urls.txt"):
            with open("urls.txt", "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip()]
        elif os.path.exists(default_urls_file):
            with open(default_urls_file, "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip()]
        else:
            safe_print("[-] Vui long cung cap danh sach URL.")
            sys.exit(1)
            
    if not urls:
        safe_print("[-] Khong tim thay URL nao de kiem tra.")
        sys.exit(1)
        
    # Doc Serper API Key tu config.json
    serper_api_key = None
    config_file = os.path.join(script_dir, "config.json")
    if os.path.exists("config.json"):
        config_file = "config.json"
        
    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as cf:
                cfg = json.load(cf)
                serper_api_key = cfg.get("serper_api_key") or cfg.get("api_key")
        except Exception:
            pass

    if not serper_api_key:
        safe_print("[-] Trong tệp config.json thiếu serper_api_key.")
        sys.exit(1)

    safe_print(f"[*] Bat dau kiem tra {len(urls)} URL bang Serper Google Search API...")
    
    results_map = {}
    
    def process_url(item):
        idx, url = item
        time.sleep(0.05 * (idx % 3)) # Small offset delay
        st = check_url_index_via_serper(serper_api_key, url)
        return idx, url, st, "Serper Google API"

    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {executor.submit(process_url, (i, url)): (i, url) for i, url in enumerate(urls, 1)}
        for future in as_completed(future_to_url):
            idx, url, status, source = future.result()
            safe_print(f"[{idx}/{len(urls)}] {url} -> [{status}] ({source})")
            results_map[idx] = {
                "URL": url,
                "Trang thai index": status,
                "Nguon check": source
            }

    results = [results_map[i] for i in range(1, len(urls) + 1)]
    
    # Xuat ket qua ra Markdown
    md_file = os.path.join(script_dir, "Index_Report.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("# BÁO CÁO GOOGLE INDEX (SERPER API)\n\n")
        f.write(f"*Thời gian quét: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("| STT | URL | Trạng thái index | Nguồn kiểm tra |\n")
        f.write("| :---: | :--- | :---: | :---: |\n")
        for idx, res in enumerate(results, 1):
            icon = "✅" if "Da index" in res['Trang thai index'] else "❌"
            f.write(f"| {idx} | {res['URL']} | {icon} **{res['Trang thai index']}** | {res['Nguon check']} |\n")
    safe_print("\n[+] Da xuat bao cao Markdown.")
    
    if pd:
        df = pd.DataFrame(results)
        excel_file = os.path.join(script_dir, f"Index_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        df.to_excel(excel_file, index=False)
        safe_print(f"[+] Da xuat file Excel.")

if __name__ == "__main__":
    main()
