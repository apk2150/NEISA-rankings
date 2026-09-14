from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from html import unescape
from html.parser import HTMLParser
from functools import lru_cache
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import re


SEASON_URL = "https://scores.collegesailing.org/f26/"


@dataclass(frozen=True)
class Regatta:
    name: str
    link: str
    start_date: datetime
    week: str


class _SeasonPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.regattas = []
        self._in_season_table = False
        self._current_row = None
        self._current_cell = None
        self._current_cell_text = ""
        self._current_week = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "table" and "season-summary" in attributes.get("class", "").split():
            self._in_season_table = True
        elif self._in_season_table and tag == "tr":
            self._current_row = {"cells": [], "link": None}
        elif self._current_row is not None and tag in ("th", "td"):
            self._current_cell = tag
            self._current_cell_text = ""
        elif self._current_row is not None and tag == "a":
            self._current_row["link"] = attributes.get("href")

    def handle_data(self, data):
        if self._current_row is not None and self._current_cell is not None:
            self._current_cell_text += data.strip()

    def handle_endtag(self, tag):
        if tag in ("th", "td") and self._current_row is not None:
            self._current_row["cells"].append(self._current_cell_text)
            self._current_cell = None
        elif tag == "tr" and self._current_row is not None:
            row = self._current_row
            if row["cells"] and row["cells"][0].startswith("Week "):
                self._current_week = row["cells"][0]
            elif row["link"] and len(row["cells"]) >= 5:
                self.regattas.append(
                    Regatta(
                        name=unescape(row["cells"][0]).strip(),
                        link=row["link"],
                        start_date=datetime.strptime(row["cells"][4].strip(), "%m/%d/%Y"),
                        week=self._current_week or "",
                    )
                )
            self._current_row = None
        elif tag == "table" and self._in_season_table:
            self._in_season_table = False

def _normalize_name(name):
    name = unescape(str(name)).casefold().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", " ", name).strip()


@lru_cache(maxsize=None)
def get_season_regattas(season_url=SEASON_URL):
    request = Request(season_url, headers={"User-Agent": "NEISA-rankings"})
    with urlopen(request, timeout=30) as response:
        page = response.read().decode("utf-8")

    parser = _SeasonPageParser()
    parser.feed(page)
    if not parser.regattas:
        raise RuntimeError(f"No regattas found at {season_url}")

    return [
        Regatta(
            name=regatta.name,
            link=urljoin(season_url, regatta.link),
            start_date=regatta.start_date,
            week=regatta.week,
        )
        for regatta in parser.regattas
    ]


def find_regatta_link(regatta_name, season_url=SEASON_URL):
    regattas = get_season_regattas(season_url)
    weeks = {}
    for regatta in regattas:
        weeks.setdefault(regatta.week, []).append(regatta)
    latest_week_regattas = max(
        weeks.values(), key=lambda week: max(regatta.start_date for regatta in week)
    )

    normalized_name = _normalize_name(regatta_name)
    exact_matches = [
        regatta
        for regatta in latest_week_regattas
        if _normalize_name(regatta.name) == normalized_name
    ]
    if exact_matches:
        return exact_matches[0].link

    if not latest_week_regattas:
        raise RuntimeError(f"No regattas found in the most recent week at {season_url}")

    closest = max(
        latest_week_regattas,
        key=lambda regatta: SequenceMatcher(
            None, normalized_name, _normalize_name(regatta.name)
        ).ratio(),
    )
    print(f"Using closest regatta match for '{regatta_name}': '{closest.name}'")
    return closest.link
