
import random
import re
import time
from html import unescape

import requests

base_url = "https://fgiesen.wordpress.com/"
seen_links = set()
all_entries = []

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
}

# Programmatically generate every month from January 2000 to August 2026
archive_months = []
for year in range(2000, 2027):
    for month in range(1, 12 + 1):
        if year == 2026 and month > 8:  # Stop at the current month
            break
        archive_months.append(f"{year}/{month:02d}")

# Reverse to crawl chronologically from newest backward
archive_months.reverse()

print(f"Scraping links directly via monthly pages ({len(archive_months)} months generated)...")

for index, month in enumerate(archive_months, 1):
    month_url = f"{base_url}{month}/"
    
    try:
        response = requests.get(month_url, headers=headers, timeout=5)
        
        # Silently skip empty/inactive month pages
        if response.status_code != 200:
            continue
            
        print(f"[{index}/{len(archive_months)}] Scanning active archive: {month}... ", end="", flush=True)
        html = response.text
        
        # Isolate the main layout container if present to block matching sidebar links
        if 'id="content"' in html:
            html = html.split('id="content"')[1].split('id="sidebar"')[0]
            
        # Target the layout hierarchy pattern: <li><span><a href="URL">Title</a></span></li>
        # This scans the structural links inside the main page timeline index cleanly
        pattern = r'<a\s+[^>]*href="(https://fgiesen\.wordpress\.com/' + month + r'/\d{2}/[^"/]+/?)".*?>(.*?)</a>'
        matches = re.findall(pattern, html, re.DOTALL)
        
        new_items = 0
        for link, title_raw in matches:
            if link not in seen_links:
                seen_links.add(link)
                new_items += 1
                
                # Clean up HTML characters and tags in the title text
                clean_title = unescape(re.sub(r'<[^>]*>', '', title_raw).strip())
                
                # Extract exact day structure for the RSS timestamp
                date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', link)
                pub_date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}T00:00:00Z" if date_match else f"{month.replace('/', '-')}-01T00:00:00Z"
                
                all_entries.append(f"""    <item>
        <title>{clean_title}</title>
        <link>{link}</link>
        <pubDate>{pub_date}</pubDate>
        <description><![CDATA[Historical archive item discovered via monthly directory scraper.]]></description>
    </item>""")
                
        print(f"Success (+{new_items} articles mapped)")
        
        # Polite throttling pause
        time.sleep(random.uniform(0.3, 0.6))
        
    except Exception as e:
        print(f"\nError scanning {month} ({type(e).__name__})")
        continue

# Save out compiled RSS file
with open("ryg_history.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?><rss version="2.0"><channel><title>The ryg blog (Scraped Master Archive)</title><link>https://fgiesen.wordpress.com/</link><description>Full timeline compilation via monthly parsing</description>\n')
    f.write("\n".join(all_entries))
    f.write('\n</channel></rss>')

print(f"\nDone! File written: ryg_history.xml ({len(all_entries)} total posts collected).")

