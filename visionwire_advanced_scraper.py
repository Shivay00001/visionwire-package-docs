"""VisionWire Advanced Scraper — REAL web scraper.

Fetches real educational content for a topic from Wikipedia (REST API +
article HTML parsed with BeautifulSoup), with a local file cache.
No simulated / mock content anywhere in this module.
"""
import os
import re
import requests
from bs4 import BeautifulSoup

USER_AGENT = "VisionWireScraper/1.0 (educational study-pack generator)"
REQUEST_TIMEOUT = 20


class AdvancedScraper:
    def __init__(self, cache_dir="cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def scrape_topic(self, topic):
        """Return real scraped educational text for *topic* (Wikipedia)."""
        cache_path = os.path.join(
            self.cache_dir, f"{re.sub(r'[^a-z0-9]+', '_', topic.lower()).strip('_')}.txt"
        )
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return f.read()

        content = self._fetch_wikipedia(topic)
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(content)
        return content

    # -- Wikipedia -----------------------------------------------------------
    def _fetch_wikipedia(self, topic):
        """Real fetch: Wikipedia summary API, falling back to article HTML."""
        # 1) Summary REST API (real JSON endpoint)
        try:
            r = self.session.get(
                "https://en.wikipedia.org/api/rest_v1/page/summary/"
                + requests.utils.quote(topic.replace(" ", "_")),
                timeout=REQUEST_TIMEOUT,
            )
            if r.status_code == 200:
                data = r.json()
                extract = (data.get("extract") or "").strip()
                if extract:
                    return self._wrap(topic, data.get("content_urls", {})
                                      .get("desktop", {}).get("page", ""), extract)
        except requests.RequestException:
            pass

        # 2) Fallback: parse the article HTML itself with BeautifulSoup
        search = self.session.get(
            "https://en.wikipedia.org/w/index.php",
            params={"search": topic, "title": "Special:Search", "fulltext": "1"},
            timeout=REQUEST_TIMEOUT,
        )
        search.raise_for_status()
        soup = BeautifulSoup(search.text, "html.parser")

        # Direct hit redirects to the article; search results page otherwise.
        article = soup.select_one("#mw-content-text .mw-parser-output")
        paras = []
        if article:
            for p in article.find_all("p", recursive=False):
                text = p.get_text(" ", strip=True)
                if len(text) > 60:
                    paras.append(text)
                if sum(len(x) for x in paras) > 4000:
                    break
        if not paras:
            raise RuntimeError(f"Wikipedia returned no usable content for topic: {topic!r}")
        return self._wrap(topic, search.url, "\n\n".join(paras))

    @staticmethod
    def _wrap(topic, source_url, body):
        return (
            f"TOPIC: {topic}\n"
            f"SOURCE: {source_url or 'https://en.wikipedia.org'}\n\n{body}"
        )
