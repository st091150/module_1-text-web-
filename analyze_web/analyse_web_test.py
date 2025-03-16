import unittest
import requests
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock
from io import StringIO
from AnalyserWeb import  fetch_page_content, parse_page_content, extract_title, extract_links, extract_paragraphs, extract_images

class TestFetchPageContent(unittest.TestCase):
    
    @patch('requests.get')
    def test_fetch_page_content_success(self, mock_get):
        """Тест успешного получения контента страницы."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Test content</body></html>"
        mock_get.return_value = mock_response

        content = fetch_page_content("http://test_1.com")
        self.assertEqual(content, "<html><body>Test content</body></html>")
    
    @patch('sys.stdout', new_callable=StringIO)
    @patch('requests.get')
    def test_fetch_page_content_error(self, mock_get, mock_stdout):
        """Тест ошибки при получении контента страницы."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found")
        mock_get.return_value = mock_response

        content = fetch_page_content("http://test_2.com")
        self.assertIsNone(content)
        self.assertIn("Ошибка при получении страницы: Not Found", mock_stdout.getvalue())


    @patch('sys.stdout', new_callable=StringIO)
    @patch('requests.get')
    def test_fetch_page_content_connection_error(self, mock_get, mock_stdout):
        """Тест ошибки подключения."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")
        content = fetch_page_content("http://test_3.com")
        self.assertIsNone(content)
        self.assertIn(f"Ошибка при получении страницы: {mock_get.side_effect.args[0]}", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('requests.get')
    def test_fetch_page_content_error_message(self, mock_get, mock_stdout):
        """Проверка вывода сообщения об ошибке."""
        mock_get.side_effect = requests.exceptions.RequestException("Test error")
        fetch_page_content("http://example.com")
        self.assertIn(f"Ошибка при получении страницы: {mock_get.side_effect.args[0]}", mock_stdout.getvalue())


class TestParsePageContent(unittest.TestCase):
    def test_parse_page_content_with_empty_string(self):
        """Проверка на обработку пустой строки"""
        soup = parse_page_content("")
        self.assertIsNone(soup)

    def test_parse_page_content_with_none(self):
        """Проверка на обработку None"""
        soup = parse_page_content(None)
        self.assertIsNone(soup)
    
    def test_parse_page_content_with_valid_html(self):
        """Проверка обработки корректной веб-страницы"""
        html = "<html><body><h1>Заголовок</h1></body></html>"
        soup = parse_page_content(html)
        self.assertIsInstance(soup, BeautifulSoup)


class TestExtractTitle(unittest.TestCase):
    def setUp(self):
        self.soup_with_title = BeautifulSoup("<html><head><title>Мой заголовок</title></head><body></body></html>", 'html.parser')
        self.soup_without_title = BeautifulSoup("<html><head></head><body></body></html>", 'html.parser')
        self.soup_with_empty_title = BeautifulSoup("<html><head><title></title></head><body></body></html>", 'html.parser')
        return super().setUp()

    def test_extract_title_with_title(self):
        """Проверка корректной работы"""
        title = extract_title(self.soup_with_title)
        self.assertEqual(title, "Мой заголовок")

    def test_extract_title_without_title(self):
        """Проверка обработки веб-страницы без заголовка"""
        title = extract_title(self.soup_without_title)
        self.assertEqual(title, "Нет заголовка")

    def test_extract_title_with_empty_title(self):
        """Проверка обработки веб-страницы с пустым заголовком"""
        title = extract_title(self.soup_with_empty_title)
        self.assertEqual(title, "Нет заголовка")

    def test_extract_title_with_none_soup(self):
        """Проверка на некорректный аргумент"""
        with self.assertRaises(AttributeError):
            extract_title(None)


class TestExtractLinks(unittest.TestCase):
    def setUp(self):
        self.html_without_links = BeautifulSoup("<html><body></body></html>", 'html.parser')

        self.html_with_multiple_links = BeautifulSoup("""
                                            <html>
                                            <body>
                                                <a href="https://example.com">Ссылка на пример</a>
                                                <a href="https://google.com">Ссылка на Google</a>
                                                <a href="https://yandex.ru">Ссылка на Яндекс</a>
                                            </body>
                                            </html>
                                            """, 
                                            'html.parser')
        
        self.html_with_multiple_links_and_other_elements = BeautifulSoup("""
                                            <html>
                                            <body>
                                                <p>Параграф текста</p>
                                                <a href="https://example.com">Ссылка на пример</a>
                                                <div>Другой элемент</div>
                                                <a href="https://google.com">Ссылка на Google</a>
                                            </body>
                                            </html>
                                            """, 
                                            'html.parser')
        return super().setUp()
        

    def test_extract_links_without_links(self):
        """Проверка обработки веб-страницы без ссылок"""
        links = extract_links(self.html_without_links)
        self.assertEqual(len(links), 0)
        self.assertEqual(links, {})

    def test_extract_links_without_links(self):
        """Проверка обработки веб-страницы c множеством ссылок"""
        links = extract_links(self.html_with_multiple_links)
        self.assertEqual(len(links), 3)
        self.assertEqual(links[0], {'text': 'Ссылка на пример', 'href': 'https://example.com'})
        self.assertEqual(links[1], {'text': 'Ссылка на Google', 'href': 'https://google.com'})
        self.assertEqual(links[2], {'text': 'Ссылка на Яндекс', 'href': 'https://yandex.ru'})

    def test_extract_links_with_links_and_other_elements(self):
        """Проверка обработки веб-страницы c множеством ссылок и другими тегами"""
        links = extract_links(self.html_with_multiple_links_and_other_elements)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0], {'text': 'Ссылка на пример', 'href': 'https://example.com'})
        self.assertEqual(links[1], {'text': 'Ссылка на Google', 'href': 'https://google.com'})

    def test_extract_links_with_none_soup(self):
        """Проверка на некорректный аргумент"""
        with self.assertRaises(AttributeError):
            extract_title(None)


class TestExtractParagraphs(unittest.TestCase):
    def setUp(self):
        self.html_without_paragraphs = BeautifulSoup("<html><body></body></html>", 'html.parser')

        self.html_with_empty_paragraph = BeautifulSoup("<html><body><p></p></body></html>", 'html.parser')

        self.html_with_multiple_paragraphs = BeautifulSoup("""
                                            <html>
                                            <body>
                                                <p>Первый параграф.</p>
                                                <p>Второй параграф.</p>
                                                <p>Третий параграф.</p>
                                            </body>
                                            </html>
                                            """, 
                                            'html.parser')
        
        self.html_with_multiple_paragraphs_and_other_elements = BeautifulSoup("""
                                            <html>
                                            <body>
                                                <h1>Заголовок</h1>
                                                <p>Первый параграф.</p>
                                                <div>Другой элемент</div>
                                                <p>Второй параграф.</p>
                                            </body>
                                            </html>
                                            """, 
                                            'html.parser')
        return super().setUp()
        

    def test_extract_paragraphs_without_paragraphs(self):
        """Проверка обработки веб-страницы без параграфов"""
        paragraphs = extract_paragraphs(self.html_without_paragraphs)
        self.assertEqual(len(paragraphs), 0)
        self.assertEqual(paragraphs, [])

    def test_extract_paragraphs_with_empty_paragraph(self):
        """Проверка обработки веб-страницы c пустым параграфом"""
        paragraphs = extract_paragraphs(self.html_with_empty_paragraph)
        self.assertEqual(len(paragraphs), 1)
        self.assertEqual(paragraphs[0], "")

    def test_extract_paragraphs_with_empty_paragraph(self):
        """Проверка обработки веб-страницы c множеством параграфов"""
        paragraphs = extract_paragraphs(self.html_with_multiple_paragraphs)
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(paragraphs[0], "Первый параграф.")
        self.assertEqual(paragraphs[1], "Второй параграф.")
        self.assertEqual(paragraphs[2], "Третий параграф.")

    def test_extract_paragraphs_with_paragraphs_and_other_elements(self):
        """Проверка обработки веб-страницы c множеством параграфов и другими тегами"""
        paragraphs = extract_paragraphs(self.html_with_multiple_paragraphs_and_other_elements)
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0], "Первый параграф.")
        self.assertEqual(paragraphs[1], "Второй параграф.")

    def test_extract_paragraphs_with_none_soup(self):
        """Проверка на некорректный аргумент"""
        with self.assertRaises(AttributeError):
            extract_paragraphs(None)


class TestExtractImages(unittest.TestCase):
    def setUp(self):
        self.html_without_images = BeautifulSoup("<html><body></body></html>", 'html.parser')

        self.html_with_one_image = BeautifulSoup("<html><body><img src='image.png' alt='One image'></body></html>", 'html.parser')

        self.html_with_one_image_and_without_alt = BeautifulSoup("<html><body><img src='image.png'></body></html>", 'html.parser')

        self.html_with_one_image_and_without_src = BeautifulSoup("<html><body><img alt='No source'></body></html>", 'html.parser')

        self.html_with_multiple_images = BeautifulSoup("""
                                            <html>
                                            <body>
                                                    <img src="image1.png" alt="First image">
                                                    <img src="image2.jpg" alt="Second image">
                                                    <img src="image3.gif">
                                            </body>
                                            </html>
                                            """, 
                                            'html.parser')
        
        self.html_with_multiple_paragraphs_and_other_elements = BeautifulSoup("""
                                            <html>
                                            <body>
                                                <img src="image1.png" alt="First image">
                                                <p>Первый параграф.</p>
                                                <div>Другой элемент</div>
                                                <img src="image2.jpg" alt="Second image">
                                            </body>
                                            </html>
                                            """, 
                                            'html.parser')
        return super().setUp()
        
    def test_extract_images_without_images(self):
        """Проверка обработки веб-страницы без изображений"""
        images = extract_images(self.html_without_images)
        self.assertEqual(len(images), 0)
        self.assertEqual(images, [])

    def test_extract_images_with_one_image(self):
        """Проверка обработки веб-страницы с 1 изображением"""
        images = extract_images(self.html_with_one_image)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], {'src': 'image.png', 'alt': 'One image'})

    def test_extract_images_with_one_image_and_without_alt(self):
        """Проверка обработки веб-страницы с 1 изображением без описания"""
        images = extract_images(self.html_with_one_image_and_without_alt)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], {'src': 'image.png', 'alt': ''})

    def test_extract_images_with_one_image_and_without_src(self):
        """Проверка обработки веб-страницы с 1 изображением без URL"""
        images = extract_images(self.html_with_one_image_and_without_src)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], {'src': '', 'alt': 'No source'})

    def test_extract_images_with_multiple_images(self):
        """Проверка обработки веб-страницы c множеством изображений"""
        images = extract_images(self.html_with_multiple_images)
        expected = [
            {'src': 'image1.png', 'alt': 'First image'},
            {'src': 'image2.jpg', 'alt': 'Second image'},
            {'src': 'image3.gif', 'alt': ''}
        ]
        self.assertEqual(len(images), 3)
        self.assertEqual(images, expected)

    def test_extract_images_with_multiple_paragraphs_and_other_elements(self):
        """Проверка обработки веб-страницы c множеством изображений и другими тегами"""
        images = extract_images(self.html_with_multiple_paragraphs_and_other_elements)
        expected = [
            {'src': 'image1.png', 'alt': 'First image'},
            {'src': 'image2.jpg', 'alt': 'Second image'},
        ]
        self.assertEqual(len(images), 2)
        self.assertEqual(images, expected)

    def test_extract_images_with_none_soup(self):
        """Проверка на некорректный аргумент"""
        with self.assertRaises(AttributeError):
            extract_images(None)

if __name__ == '__main__':
    unittest.main()