# ryg-blog-rss-archive

A tool and pre-compiled RSS feed to bypass WordPress.com feed limits and backfill the entire historical archive of **The ryg blog** (Fabian Giesen) into your RSS feed reader.

Standard WordPress RSS feeds cap their output to the most recent 10–20 posts. This project generates a complete historical RSS timeline stretching from the blog's inception in October 2009 up to August 2026.

---

## 🤖 AI-Generated Project Disclosure

**Note:** This repository, including the script logic, structural design, and documentation, was built through an iterative collaboration with an **AI Assistant**.

---

## 🚀 Quick Start (For Feed Reader Users)

If you just want to import the historical articles into your feed reader (FreshRSS, NetNewsWire, Tiny Tiny RSS, etc.), you don't need to run any code.

1. Download or copy the raw URL of the `ryg_history.xml` file from this repository.
2. Import or add it to your feed reader as a standard **RSS/Atom** feed.

---

## 🛠️ How it Works (Scraper Script)

The repository includes `rss-replay.py`, a lightweight Python script that programmatically crawls the ryg blog's native monthly archive directories. It extracts every valid article link, mapping the real titles and publication dates directly from the live web headers to bypass aggressive Internet Archive/Wayback Machine rate limits.

### Requirements

- Python 3.x
- `requests` library

### Running the Scraper

If you want to update the archive or run it yourself:

```bash
pip install requests
python rss-replay.py
```

This generates a standardized RSS 2.0 file named `ryg_history.xml`.

---

## ⚙️ FreshRSS Import Guide

To populate your dashboard queue with your compiled historical index:

### 1. Import the Feed

1. Open your terminal in the directory containing `ryg_history.xml` and serve it using Python's built-in HTTP server:
   ```bash
   python -m http.server 8080
   ```
2. Go to FreshRSS -> **Subscription management** -> **Add a feed or category**.
3. Paste `http://localhost:8080/ryg_history.xml` into the **Feed URL** box.
4. Keep the **Type of feed source** as standard **RSS / Atom** and click add.

_Note: Once your historical archive is processed, add his active feed (`https://wordpress.com`) as a standard independent subscription to track any future posts going forward._

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
