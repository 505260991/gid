from __future__ import annotations

import html
import re
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import unquote, urlparse

CODE_PATTERNS = [
    re.compile(r"(?:提取码|访问码|密码|code|passcode)\s*[:：]?\s*([A-Za-z0-9]{4,8})", re.IGNORECASE),
    re.compile(r"\b([A-Za-z0-9]{4})\b"),
]

PAN115_PATTERN = re.compile(
    r"https?://(?:115\.com|115cdn\.com)/(?:s|share)/([A-Za-z0-9]+)(?:\?password=([A-Za-z0-9]{4,8}))?",
    re.IGNORECASE,
)

HDHIVE_PATTERN = re.compile(r"https?://(?:www\.)?hdhive\.[\w.\-/?:=&%#]+", re.IGNORECASE)
HREF_PATTERN = re.compile(r"href=[\"']([^\"']+)[\"']", re.IGNORECASE)
SCRIPT_PATTERN = re.compile(r"<script[^>]*>(.*?)</script>", re.IGNORECASE | re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")


@dataclass
class UnlockResult:
    source: str
    source_type: str
    pan_url: str
    code: str | None

    @property
    def quick_text(self) -> str:
        return f"{self.pan_url} 提取码: {self.code}" if self.code else self.pan_url


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _extract_code_nearby(text: str, start: int, end: int) -> str | None:
    window_start = max(0, start - 80)
    window_end = min(len(text), end + 80)
    window = text[window_start:window_end]

    for pattern in CODE_PATTERNS:
        hit = pattern.search(window)
        if hit:
            return hit.group(1)
    return None


def _extract_text_from_html(html_text: str) -> str:
    scripts = "\n".join(SCRIPT_PATTERN.findall(html_text))
    hrefs = "\n".join(unquote(html.unescape(m.group(1))) for m in HREF_PATTERN.finditer(html_text))
    no_tag = TAG_PATTERN.sub(" ", html_text)
    decoded = html.unescape(no_tag)
    return "\n".join([decoded, scripts, hrefs])


def extract_hdhive_urls(text: str) -> list[str]:
    return sorted({match.group(0) for match in HDHIVE_PATTERN.finditer(text)})


def parse_unlock_items(text: str, source: str = "manual-input", source_type: str = "text") -> list[UnlockResult]:
    items: list[UnlockResult] = []
    seen: set[tuple[str, str | None]] = set()

    source_text = text
    if "<html" in text.lower() or "href=" in text.lower():
        source_text = _extract_text_from_html(text)

    for match in PAN115_PATTERN.finditer(source_text):
        share_id = match.group(1)
        inline_code = match.group(2)
        pan_url = f"https://115.com/s/{share_id}"
        code = inline_code or _extract_code_nearby(source_text, match.start(), match.end())
        key = (pan_url, code)
        if key in seen:
            continue
        seen.add(key)
        items.append(UnlockResult(source=source, source_type=source_type, pan_url=pan_url, code=code))

    return items


def to_dicts(items: Iterable[UnlockResult]) -> list[dict[str, str | None]]:
    return [
        {
            "source": item.source,
            "sourceType": item.source_type,
            "panUrl": item.pan_url,
            "code": item.code,
            "quickCopy": item.quick_text,
            "host": urlparse(item.pan_url).netloc,
        }
        for item in items
    ]
