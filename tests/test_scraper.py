from webscraper.scraper import parse_title_and_links

def test_parse_title_and_links():
    html = '<html><head><title>Test Page</title></head><body><a href="https://example.com"></a></body></html>'
    res = parse_title_and_links(html)
    assert res["title"] == "Test Page"
    assert "https://example.com" in res["links"]
