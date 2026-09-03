# Generic Blog RSS Archive Generator

A flexible Python tool to scrape historical blog archives across various platforms (WordPress, Ghost, Blogger, static sites, etc.) and compile them into a complete master RSS feed for your feed reader.

Many blogs limit their standard RSS feeds to the most recent 10–20 posts. This project allows you to crawl monthly archive pages and generate a full historical RSS timeline for any target blog.

---

## 🤖 AI-Generated Project Disclosure

**Note:** This repository, including the script logic, structural design, and documentation, was built through an iterative collaboration with an **AI Assistant**.

---

## 🛠️ How it Works (Scraper Script)

The repository includes a Python script that programmatically crawls a target blog's native monthly archive directories using **BeautifulSoup**. It extracts valid article links and fetches individual post content to build an RSS-compatible XML file.

### Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

### Installation & Setup

1. Install the required dependencies:

   ```bash
   pip install requests beautifulsoup4
   ```

2. Open the script and modify the **Configuration Section** at the top to match your target blog:

```python
CONFIG = {
    "blog_name": "My Target Blog",
    "base_url": "[https://example.com/](https://example.com/)",
    "archive_url_format": "{base_url}archives/{year}/{month:02d}/",
    "start_year": 2015,
    "end_year": 2026,
    "end_month": 12,
    "post_link_selector": "article h2 a, .post-title a",
    "post_content_selector": "article, .post-content, .entry-content"
}
```

3. Run the script:

```bash
python archive_scraper.py

```

This generates a standardized RSS 2.0 file named `[blog_name]_archive.xml`.

---

## ⚙️ Feed Reader Import Guide

To load your compiled historical index into your feed reader (FreshRSS, NetNewsWire, Tiny Tiny RSS, etc.):

1. Open your terminal in the directory containing your generated `.xml` file and serve it using Python's built-in HTTP server:

```bash
python -m http.server 8080

```

2. Go to your feed reader -> **Subscription management** -> **Add a feed or category**.
3. Paste `http://localhost:8080/your_blog_archive.xml` into the **Feed URL** box and save.

---

## 📄 License

This project is licensed under the **MIT License**.

```text
MIT License

Copyright (c) 2026 Geipeg

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

```
