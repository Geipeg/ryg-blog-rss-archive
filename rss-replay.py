import random
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# ==================== CONFIGURATION ====================
CONFIG = {
    "blog_name": "Generic Blog Archive",
    "base_url": "https://example.com/",
    
    # How archive pages are structured (e.g., /archives/2023/10/)
    "archive_url_format": "{base_url}archives/{year}/{month:02d}/",
    "start_year": 2020,
    "end_year": 2026,
    "end_month": 12,
    
    # CSS Selectors for finding posts on an archive/index page
    # (Matches the container for each post link/title)
    "post_link_selector": "article h2 a, .post-title a, .archive-list a",
    
    # CSS Selector for extracting the main body text on an individual post page
    "post_content_selector": "article, .post-content, .entry-content, main"
}
# =======================================================

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
}

seen_links = set()
all_entries = []

# Generate archive months chronologically backwards
archive_months = []
for year in range(CONFIG["start_year"], CONFIG["end_year"] + 1):
    for month in range(1, 12 + 1):
        if year == CONFIG["end_year"] and month > CONFIG["end_month"]:
            break
        archive_months.append((year, month))

archive_months.reverse()

print(f"Scraping '{CONFIG['blog_name']}' ({len(archive_months)} archive months generated)...")

for index, (year, month) in enumerate(archive_months, 1):
    month_url = CONFIG["archive_url_format"].format(
        base_url=CONFIG["base_url"], year=year, month=month
    )
    
    try:
        response = requests.get(month_url, headers=headers, timeout=5)
        if response.status_code != 200:
            continue
            
        print(f"[{index}/{len(archive_months)}] Scanning archive: {year}/{month:02d}... ", end="", flush=True)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all matching post links using the configured CSS selector
        link_elements = soup.select(CONFIG["post_link_selector"])
        
        new_items = 0
        for tag in link_elements:
            link = tag.get("href")
            if not link:
                continue
                
            link = urljoin(CONFIG["base_url"], link)

            if link not in seen_links:
                seen_links.add(link)
                new_items += 1
                
                clean_title = tag.get_text(strip=True)
                
                # Fetch individual post content
                post_content = f"Read full post at: {link}"
                try:
                    post_res = requests.get(link, headers=headers, timeout=5)
                    if post_res.status_code == 200:
                        post_soup = BeautifulSoup(post_res.text, "html.parser")
                        content_tag = post_soup.select_one(CONFIG["post_content_selector"])
                        if content_tag:
                            post_content = str(content_tag) # Keeps HTML formatting
                    time.sleep(random.uniform(0.1, 0.3))
                except Exception:
                    pass
                
                pub_date = f"{year}-{month:02d}-01T00:00:00Z"
                
                all_entries.append(f"""    <item>
        <title>{clean_title}</title>
        <link>{link}</link>
        <pubDate>{pub_date}</pubDate>
        <description><![CDATA[{post_content}]]></description>
    </item>""")
                
        print(f"Success (+{new_items} articles mapped)")
        time.sleep(random.uniform(0.3, 0.6))
        
    except Exception as e:
        print(f"\nError scanning {year}/{month:02d} ({type(e).__name__})")
        continue

# Output compiled RSS file
output_filename = f"{CONFIG['blog_name'].lower().replace(' ', '_')}_archive.xml"
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(f'<?xml version="1.0" encoding="utf-8"?><rss version="2.0"><channel><title>{CONFIG["blog_name"]} (Master Archive)</title><link>{CONFIG["base_url"]}</link><description>Full timeline compilation</description>\n')
    f.write("\n".join(all_entries))
    f.write('\n</channel></rss>')

print(f"\nDone! File written: {output_filename} ({len(all_entries)} total posts collected).")
