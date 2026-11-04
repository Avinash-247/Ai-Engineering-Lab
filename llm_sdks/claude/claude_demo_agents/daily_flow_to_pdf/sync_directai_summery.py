"""
Sync "Summary of Today's ..." classroom posts from https://directai.blog/
into a local folder as PDFs (one PDF per post, date included in the file name).

Every run:
  - scans the blog pages (newest -> oldest) down to START_DATE
  - skips posts whose PDF already exists in the folder
  - downloads only the NEW ones

One-time setup (Windows, in your venv / terminal):
    pip install requests beautifulsoup4 playwright
    playwright install chromium

Run:
    python sync_directai_summaries.py
"""

import re
import sys
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# ----------------------------- SETTINGS ------------------------------------
BASE_URL = "https://directai.blog"
START_DATE = date(2026, 9, 24)          # from this date ... till today
END_DATE = date.today()

AGENT_DIR = Path(r"C:\Users\vempa\learnning_rag\llm_sdks\claude\claude_Agent_classes_pdf")
MCP_DIR = Path(r"C:\Users\vempa\learnning_rag\MCP\MCP_classes_pdf")

# (title prefixes, folder) - checked in order. First match wins.
# Anything that matches none of these (e.g. Python classes) is NOT synced.
ROUTES = [
    (["Summary of Today's Gen AI MCP Session"], MCP_DIR),
    (["Summary of Today's Gen AI Classroom",
      "Summary of Today's Gen AI Agents Session",
      "Summary of Today's Gen AI Foundation Session",
      "Context Engineering, Memory and Human"], AGENT_DIR),
]

MAX_PAGES = 60                          # safety limit for pagination
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; directai-sync/1.0)"}

# CSS injected before printing so the PDF contains only the article
HIDE_CSS = """
header, nav, footer, aside, .site-header, .site-footer, .main-navigation,
.comments-area, #comments, #respond, .sharedaddy, .jp-relatedposts,
.post-navigation, .nav-links, .widget-area, #wpadminbar, .wpcnt,
.entry-meta, .cat-links, .tags-links, iframe { display: none !important; }
body { background: #fff !important; }
"""
# ---------------------------------------------------------------------------


def norm(text: str) -> str:
    """Normalise curly quotes / spaces so title matching is reliable."""
    return (
        text.replace("\u2019", "'").replace("\u2018", "'")
        .replace("\u201c", '"').replace("\u201d", '"')
        .replace("\xa0", " ").strip()
    )


def safe_name(text: str, limit: int = 110) -> str:
    text = norm(text)
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", text)   # illegal on Windows
    text = re.sub(r"\s+", " ", text).strip(" .")
    return text[:limit].rstrip(" .")


def route_folder(title: str):
    """Return the target folder for a post title, or None if it isn't wanted."""
    t = norm(title).lower()
    for prefixes, folder in ROUTES:
        if any(t.startswith(norm(p).lower()) for p in prefixes):
            return folder
    return None


def collect_posts():
    """Walk /page/1, /page/2 ... and return matching posts in the date range."""
    found, seen = [], set()

    for page in range(1, MAX_PAGES + 1):
        url = BASE_URL + "/" if page == 1 else f"{BASE_URL}/page/{page}/"
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 404:
            break
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        reached_older = False
        any_post = False

        for a in soup.select("h1 a[href], h2 a[href], h3 a[href]"):
            href = a["href"]
            m = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", href)
            if not m:
                continue
            any_post = True
            post_date = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

            if post_date < START_DATE:
                reached_older = True
                continue
            if post_date > END_DATE:
                continue

            title = norm(a.get_text(" ", strip=True))
            folder = route_folder(title)
            if folder is None:                 # Python / notes posts: skip
                continue
            if href in seen:
                continue
            seen.add(href)
            found.append({"date": post_date, "title": title,
                          "url": href, "dir": folder})

        print(f"  scanned page {page}")
        if not any_post or reached_older:
            break

    found.sort(key=lambda p: (p["date"], p["title"]))
    return found


def pdf_path(post) -> Path:
    return post["dir"] / f"{post['date'].isoformat()} - {safe_name(post['title'])}.pdf"


def save_pdfs(posts):
    saved = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        for post in posts:
            target = pdf_path(post)
            print(f"  downloading: {target.name}")
            try:
                page.goto(post["url"], wait_until="load", timeout=60000)
                page.add_style_tag(content=HIDE_CSS)
                page.emulate_media(media="screen")
                page.pdf(
                    path=str(target),
                    format="A4",
                    print_background=True,
                    margin={"top": "15mm", "bottom": "15mm",
                            "left": "12mm", "right": "12mm"},
                )
                saved += 1
            except Exception as exc:                      # keep going on errors
                print(f"    FAILED ({exc})")
                if target.exists():
                    target.unlink()                       # no half-written file
        browser.close()
    return saved


def main():
    for folder in (AGENT_DIR, MCP_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    print(f"Checking {BASE_URL} from {START_DATE} to {END_DATE} ...")
    posts = collect_posts()
    print(f"Found {len(posts)} matching post(s) on the blog.")

    new_posts = [p for p in posts if not pdf_path(p).exists()]
    already = len(posts) - len(new_posts)
    print(f"Already saved: {already} | New to download: {len(new_posts)}")

    if not new_posts:
        print("Everything is up to date.")
        return

    saved = save_pdfs(new_posts)
    print(f"\nDone. {saved} new PDF(s) saved in:\n  {AGENT_DIR}\n  {MCP_DIR}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nStopped.")