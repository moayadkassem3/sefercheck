# scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from pathlib import Path

URL = "https://sehirhatlari.istanbul/tr/iptal-seferler"
UA = {"User-Agent": "Mozilla/5.0"}
OUT_DIR = Path("output")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "cancellations.txt"

def scrape():
    r = requests.get(URL, headers=UA, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    items = [el.get_text("\n", strip=True) for el in soup.select(".notice-detail-text-content")]
    text = "\n\n---\n\n".join(items).strip()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    header = f"# Sehir Hatlari – İptal Seferler\n# Last update (UTC): {ts}\n\n"
    return header + (text if text else "(no content found)")

def main():
    new_content = scrape()
    # Only write if content changed to avoid unnecessary commits
    old = OUT_FILE.read_text(encoding="utf-8") if OUT_FILE.exists() else ""
    if old.strip() != new_content.strip():
        OUT_FILE.write_text(new_content, encoding="utf-8")
        print("CHANGED")
    else:
        print("NOCHANGE")

if __name__ == "__main__":
    main()
