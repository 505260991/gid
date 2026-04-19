from app.parser import parse_unlock_items, extract_hdhive_urls


def test_parse_115_with_code():
    text = "资源：https://115.com/s/abcXYZ 提取码: d9x2"
    items = parse_unlock_items(text)
    assert len(items) == 1
    assert items[0].pan_url == "https://115.com/s/abcXYZ"
    assert items[0].code == "d9x2"


def test_parse_inline_password_query():
    text = "https://115.com/s/abc999?password=1q2w"
    items = parse_unlock_items(text)
    assert items[0].code == "1q2w"


def test_extract_hdhive_link():
    text = "文章: https://hdhive.example.com/posts/7"
    links = extract_hdhive_urls(text)
    assert links == ["https://hdhive.example.com/posts/7"]
