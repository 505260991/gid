from __future__ import annotations

from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, render_template, request

from app.parser import extract_hdhive_urls, parse_unlock_items, to_dicts

app = Flask(__name__, template_folder="../templates", static_folder="../static")


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/unlock")
def unlock():
    payload = request.get_json(silent=True) or {}
    text = str(payload.get("text", ""))
    fetch_url = str(payload.get("url", "")).strip()

    if not text and not fetch_url:
        return jsonify({"error": "请提供文本内容或链接"}), 400

    source = "manual-input"
    source_type = "text"
    merged_text = text

    if fetch_url:
        parsed = urlparse(fetch_url)
        if not parsed.scheme or not parsed.netloc:
            return jsonify({"error": "URL 格式不正确"}), 400
        try:
            resp = requests.get(fetch_url, timeout=12)
            resp.raise_for_status()
        except requests.RequestException as exc:
            return jsonify({"error": f"抓取失败: {exc}"}), 400

        merged_text = f"{merged_text}\n{resp.text}"
        source = fetch_url
        source_type = "url"

    items = parse_unlock_items(merged_text, source=source, source_type=source_type)
    hdhive_links = extract_hdhive_urls(merged_text)

    return jsonify(
        {
            "count": len(items),
            "items": to_dicts(items),
            "hdhiveLinks": hdhive_links,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
