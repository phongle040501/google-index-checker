import os
import sys
import time
import random
import argparse
import urllib.request
import urllib.parse
import json
import re
import shutil
from datetime import datetime

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
bs4_mod = install_and_import("beautifulsoup4", "bs4")
BeautifulSoup = bs4_mod.BeautifulSoup if bs4_mod else None

def get_playwright():
    """Lay sync_playwright hoac tu dong cai dat neu thieu"""
    try:
        from playwright.sync_api import sync_playwright
        return sync_playwright
    except ImportError:
        import subprocess
        print("[*] Dang cai dat thu vien Playwright va Chromium driver...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        try:
            subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        except Exception:
            pass
        from playwright.sync_api import sync_playwright
        return sync_playwright

# ===============================================================
# LOP 1: PLAYWRIGHT STEALTH GOOGLE CHROMIUM ENGINE
# ===============================================================
def check_url_index_via_playwright_google(page, url):
    """Kiem tra index tren Google Search bang Playwright Stealth (Gia lap nguoi dung nhap lieu)"""
    try:
        page.goto("https://www.google.com", timeout=15000)
        time.sleep(random.uniform(0.8, 1.5))
        
        search_box = page.query_selector("textarea[name='q']") or page.query_selector("input[name='q']")
        if not search_box:
            raise Exception("Khong tim thay o tim kiem Google")
            
        search_box.fill(f"site:{url}")
        time.sleep(0.5)
        page.keyboard.press("Enter")
        time.sleep(random.uniform(2.2, 3.0))
        
        current_url = page.url.lower()
        if "/sorry/index" in current_url or "captcha" in current_url:
            raise Exception("Bi chan CAPTCHA/JS Challenge")
            
        html = page.content().lower()
        try:
            text_content = page.inner_text("body").lower()
        except Exception:
            text_content = html
            
        no_results_patterns = [
            "không tìm thấy kết quả nào cho",
            "không tìm thấy tài liệu nào khớp với",
            "không khớp với bất kỳ tài liệu nào",
            "did not match any documents",
            "no results found for",
            "không tìm thấy trang nào trùng khớp",
            "không tìm thấy site:"
        ]
        
        for pattern in no_results_patterns:
            if pattern in text_content:
                return "Chua index"
                
        target_norm = url.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/").lower()
        
        links = page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")
        for href in links:
            if not href or not href.startswith("http"):
                continue
            link_norm = href.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/").lower()
            if target_norm == link_norm or link_norm.startswith(target_norm + "/"):
                return "Da index"
                
        h3_texts = page.eval_on_selector_all("h3", "elements => elements.map(e => e.innerText)")
        meaningful_h3 = [h for h in h3_texts if len(h.strip()) > 5 and "search" not in h.lower() and "console" not in h.lower()]
        if meaningful_h3:
            return "Da index"
            
        return "Chua index"
        
    except Exception as e:
        raise Exception(f"Playwright Google Error: {str(e)}")

# ===============================================================
# LOP 2: PLAYWRIGHT STEALTH BING ENGINE FALLBACK
# ===============================================================
def check_url_index_via_playwright_bing(page, url):
    """Kiem tra index tren Bing Search bang Playwright Stealth (Lop 2 Fallback)"""
    try:
        page.goto("https://www.bing.com", timeout=15000)
        time.sleep(random.uniform(0.8, 1.5))
        
        search_box = page.query_selector("input[name='q']") or page.query_selector("textarea[name='q']")
        if not search_box:
            raise Exception("Khong tim thay o tim kiem Bing")
            
        search_box.fill(f"site:{url}")
        time.sleep(0.5)
        page.keyboard.press("Enter")
        time.sleep(random.uniform(2.0, 3.0))
        
        html = page.content().lower()
        try:
            text_content = page.inner_text("body").lower()
        except Exception:
            text_content = html
            
        if "challenges.cloudflare.com" in html or "turnstile" in html:
            raise Exception("Bing Cloudflare Turnstile Blocked")
            
        no_results_patterns = [
            "không tìm thấy kết quả nào cho",
            "không khớp với bất kỳ tài liệu nào",
            "did not match any documents",
            "no results found for",
            "we couldn't find any results for",
            "thử các cụm từ tìm kiếm khác"
        ]
        
        for pattern in no_results_patterns:
            if pattern in text_content:
                return "Chua index"
                
        target_norm = url.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/").lower()
        links = page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")
        for href in links:
            if not href or not href.startswith("http"):
                continue
            link_norm = href.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/").lower()
            if target_norm == link_norm or link_norm.startswith(target_norm + "/"):
                return "Da index"
                
        b_algo_count = page.locator(".b_algo").count()
        if b_algo_count > 0:
            return "Da index"
            
        return "Chua index"
        
    except Exception as e:
        raise Exception(f"Playwright Bing Error: {str(e)}")

# ===============================================================
# MAIN
# ===============================================================
def main():
    parser = argparse.ArgumentParser(description="Kiem tra trang thai index cua danh sach URL.")
    parser.add_argument("-f", "--file", type=str, help="Duong dan den file txt chua danh sach URL.")
    parser.add_argument("-u", "--urls", type=str, help="Danh sach URL, cach nhau boi dau phay.")
    args = parser.parse_args()
    
    urls = []
    if args.file:
        if os.path.exists(args.file):
            with open(args.file, "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip()]
        else:
            print(f"[-] File khong ton tai: {args.file}")
            sys.exit(1)
    elif args.urls:
        urls = [u.strip() for u in args.urls.split(",") if u.strip()]
    else:
        if os.path.exists("urls.txt"):
            with open("urls.txt", "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip()]
        else:
            print("[-] Vui long cung cap danh sach URL.")
            sys.exit(1)
            
    if not urls:
        print("[-] Khong tim thay URL nao de kiem tra.")
        sys.exit(1)
        
    print(f"[*] Bat dau kiem tra {len(urls)} URL bang Playwright Stealth Engine...")
    
    sync_playwright = get_playwright()
    
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            locale="vi-VN",
            viewport={"width": 1366, "height": 768}
        )
        
        # An co navigator.webdriver
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        page = context.new_page()
        
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] Dang kiem tra: {url} ...", end="", flush=True)
            status = "Chua index"
            source = "None"
            
            # Lop 1: Playwright Stealth Google
            try:
                status = check_url_index_via_playwright_google(page, url)
                source = "Playwright Google"
            except Exception as e1:
                # Lop 2: Playwright Stealth Bing Fallback
                try:
                    status = check_url_index_via_playwright_bing(page, url)
                    source = "Playwright Bing"
                except Exception as e2:
                    status = f"Loi ({str(e1)})"
                    source = "Failed"
                        
            print(f" [{status}] (Nguon: {source})")
            results.append({
                "URL": url,
                "Trang thai index": status,
                "Nguon check": source
            })
            
        browser.close()
        
    # Xuat ket qua ra Markdown
    md_file = "Index_Report.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("# BÁO CÁO GOOGLE INDEX\n\n")
        f.write(f"*Thời gian quét: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("| STT | URL | Trạng thái index | Nguồn kiểm tra |\n")
        f.write("| :---: | :--- | :---: | :---: |\n")
        for idx, res in enumerate(results, 1):
            icon = "✅" if "Da index" in res['Trang thai index'] else "❌"
            f.write(f"| {idx} | {res['URL']} | {icon} **{res['Trang thai index']}** | {res['Nguon check']} |\n")
    print(f"\n[+] Da xuat bao cao Markdown: {md_file}")
    
    if pd:
        df = pd.DataFrame(results)
        excel_file = f"Index_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(excel_file, index=False)
        print(f"[+] Da xuat file Excel: {excel_file}")

if __name__ == "__main__":
    main()
