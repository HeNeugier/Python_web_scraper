import unittest
import crawl


class TestCrawl(unittest.TestCase):
    def test_normalize_url_1(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = crawl.normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_2(self):
        input_url = "www.boot.dev"
        actual = crawl.normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)



    def test_get_heading_from_html(self):
        test_html = """
            <html>
              <body>
                <h1>Welcome to Boot.dev</h1>
                <main>
                  <p>Learn to code by building real projects.</p>
                  <p>This is the second paragraph.</p>
                </main>
              </body>
            </html>
        """
        returned_header = crawl.get_heading_from_html(test_html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(returned_header, expected)

    def test_get_heading_from_html_h2(self):
        test_html = """
            <html>
              <body>
                <h2>Welcome to Boot.dev</h2>
                <main>
                  <p>Learn to code by building real projects.</p>
                  <p>This is the second paragraph.</p>
                </main>
              </body>
            </html>
        """
        returned_header = crawl.get_heading_from_html(test_html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(returned_header, expected)

    def test_get_heading_from_html_empty(self):
        test_html = """
            <html>
              <body>
                <main>
                  <p>Learn to code by building real projects.</p>
                  <p>This is the second paragraph.</p>
                </main>
              </body>
            </html>
        """
        returned_header = crawl.get_heading_from_html(test_html)
        expected = ""
        self.assertEqual(returned_header, expected)



    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = '''<html><body>
             <p>Outside paragraph.</p>
             <main>
                 <p>Main paragraph.</p>
             </main>
        </body></html>'''
        actual = crawl.get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main(self):
        input_body = '''<html><body>
            <p>Normal paragraph.</p>
        </body></html>'''
        actual = crawl.get_first_paragraph_from_html(input_body)
        expected = "Normal paragraph."
        self.assertEqual(actual, expected)



    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = crawl.get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_missing_href(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a><span>Boot.dev</span></a></body></html>'
        actual = crawl.get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_three_links_and_relative(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <a href="https://crawler-test.com">
            <a href="//crawler-test.com/testy.xml">
            <a href="/the_boot/launcher.sh">
            <span>Boot.dev</span></a></body></html>"""
        actual = crawl.get_urls_from_html(input_body, input_url)
        expected = [
                "https://crawler-test.com", 
                "https://crawler-test.com/testy.xml",
                "https://crawler-test.com/the_boot/launcher.sh"
            ]
        self.assertEqual(actual, expected)



    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = crawl.get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <img src="/logo.png" alt="Logo">
            <img src="/pogo.png">
            </body></html>"""
        actual = crawl.get_images_from_html(input_body, input_url)
        expected = [
                "https://crawler-test.com/logo.png",
                "https://crawler-test.com/pogo.png"
            ]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <img src="https://crawler-test.com/logo.png" alt="Logo">
            </body></html>"""
        actual = crawl.get_images_from_html(input_body, input_url)
        expected = [
                "https://crawler-test.com/logo.png"
            ]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_none(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <img>
            </body></html>"""
        actual = crawl.get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = crawl.extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_blank(self):
        input_url = "https://crawler-test.com"
        input_body = ""
        actual = crawl.extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_mash(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <h2>Test Title2</h2>
            <p>This is the first paragraph.</p>
            <main>
                <p>no me.</p>
            </main>
            <a href="/link1">Link 1</a>
            <img src="/bongo/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = crawl.extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title2",
            "first_paragraph": "no me.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/bongo/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_empty(self):
        input_url = ""
        input_body = ""
        actual = crawl.extract_page_data(input_body, input_url)
        expected = {
            "url": "",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_farting(self):
        input_url = "https://crawler-test.com"
        input_body = """
            <p>This is the first paragraph.</p>
            <p>This is the second paragraph.</p>
            <p>This is the third paragraph.</p>
        """
        actual = crawl.extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_shitting(self):
        input_url = ""
        input_body = """
            <p>This is the first paragraph.</p>
            <img src="/bingo.png">
        """
        actual = crawl.extract_page_data(input_body, input_url)
        expected = {
            "url": "",
            "heading": "",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [],
            "image_urls": ["/bingo.png"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_final(self):
        input_url = "https://sourcey.net"
        input_body = """
            <p>This is the first paragraph.</p>
            <img src="/bingo.png">
        """
        actual = crawl.extract_page_data(input_body, input_url)
        expected = {
            "url": "https://sourcey.net",
            "heading": "",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [],
            "image_urls": ["https://sourcey.net/bingo.png"]
        }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
