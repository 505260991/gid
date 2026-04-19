from app.parser import extract_hdhive_urls, parse_unlock_items


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


def test_parse_from_html_source_without_api():
    html = '''
    <html><body>
      <a href="https://115.com/s/hello99?password=ab12">download</a>
      <script>var note = "提取码: ab12"</script>
    </body></html>
    '''
    items = parse_unlock_items(html)
    assert len(items) == 1
    assert items[0].pan_url == "https://115.com/s/hello99"
    assert items[0].code == "ab12"
