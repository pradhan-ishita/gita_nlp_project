import json
import re
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://vedabase.io"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\xa0", " ")
    text = re.sub(r"\r", "", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_section_text(soup: BeautifulSoup, heading_text: str) -> str:
    """
    Extracts content under headings like:
    Devanagari
    Verse Text
    Translation
    Purport
    """
    heading = soup.find(
        lambda tag: tag.name in ["h2", "h3"] and heading_text.lower() in tag.get_text(" ", strip=True).lower()
    )

    if not heading:
        return ""

    collected = []
    for sibling in heading.find_next_siblings():
        if sibling.name in ["h2", "h3"]:
            break

        text = sibling.get_text("\n", strip=True)
        if text:
            collected.append(text)

    return clean_text("\n".join(collected))


def scrape_verse(chapter_num: int, verse_num: int, chapter_title: str, verse_url: str) -> dict:
    soup = get_soup(verse_url)

    return {
        "chapter": chapter_num,
        "verse": verse_num,
        "reference": f"Bg. {chapter_num}.{verse_num}",
        "title": chapter_title,
        "devanagari": extract_section_text(soup, "Devanagari"),
        "verse_text": extract_section_text(soup, "Verse Text"),
        "translation": extract_section_text(soup, "Translation"),
        "purport": extract_section_text(soup, "Purport"),
        "source": verse_url
    }


def scrape_chapter(chapter_num: int) -> list:
    chapter_url = f"{BASE_URL}/en/library/bg/{chapter_num}/"
    soup = get_soup(chapter_url)

    title_tag = soup.find("h1")
    chapter_title = title_tag.get_text(" ", strip=True) if title_tag else f"Chapter {chapter_num}"

    verse_links = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()

        # matches /en/library/bg/2/47/
        match = re.fullmatch(rf"/en/library/bg/{chapter_num}/(\d+)/?", href)
        if match:
            verse_num = int(match.group(1))
            if verse_num not in seen:
                seen.add(verse_num)
                verse_links.append((verse_num, BASE_URL + href))

    verse_links.sort(key=lambda x: x[0])

    chapter_data = []
    for verse_num, verse_url in verse_links:
        try:
            verse_data = scrape_verse(chapter_num, verse_num, chapter_title, verse_url)

            # keep only valid verse pages
            if verse_data["translation"]:
                chapter_data.append(verse_data)
                print(f"Scraped {verse_data['reference']}")
            else:
                print(f"Skipped {chapter_num}.{verse_num} (no translation found)")

            time.sleep(0.4)

        except Exception as e:
            print(f"Failed Bg. {chapter_num}.{verse_num}: {e}")

    return chapter_data


def main():
    all_verses = []

    for chapter in range(1, 19):
        print(f"\nScraping Chapter {chapter}...")
        chapter_verses = scrape_chapter(chapter)
        all_verses.extend(chapter_verses)

    with open("gita_vedabase.json", "w", encoding="utf-8") as f:
        json.dump(all_verses, f, ensure_ascii=False, indent=2)

    print(f"\nDone. Saved {len(all_verses)} verses to gita_vedabase.json")


if __name__ == "__main__":
    main()