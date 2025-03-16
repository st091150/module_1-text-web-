import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from TextExtraction import extract_text_from_pdf, extract_text_from_docx, extract_text_from_djvu, extract_text_from_doc

class TestExtractTextFromPDF(unittest.TestCase):
    def setUp(self):
        self.dummy_pdf_path = "dummy_path.pdf"
        return super().setUp()

    @patch('TextExtraction.pdfminer_extract_text')
    def test_extract_text_success(self, mock_pdfminer):
        """Проверка корректной работы извлечения текста напрямую из pdf файла"""
        mock_pdfminer.return_value = "Это текст из PDF."
        result = extract_text_from_pdf(self.dummy_pdf_path)
        self.assertEqual(result, "Это текст из PDF.")
    

    @patch('TextExtraction.pdfminer_extract_text')
    @patch('TextExtraction.convert_from_path')
    @patch('pytesseract.image_to_string')
    def test_extract_text_with_ocr(self, mock_tesseract, mock_convert, mock_pdfminer):
        """Проверка корректной работы извлечения текста через ocr"""
        mock_pdfminer.return_value = ""
        mock_convert.return_value = [MagicMock(), MagicMock()]
        mock_tesseract.side_effect = ["Текст из первой страницы", "Текст из второй страницы"]
        result = extract_text_from_pdf(self.dummy_pdf_path)

        self.assertEqual(result, "Текст из первой страницыТекст из второй страницы")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('TextExtraction.pdfminer_extract_text')
    def test_extract_text_exception(self, mock_pdfminer, mock_stdout):
        """Проверка обработки исключений"""
        mock_pdfminer.side_effect = Exception("Ошибка извлечения текста")
        
        extract_text_from_pdf(self.dummy_pdf_path)
        self.assertIn("Ошибка извлечения текста", mock_stdout.getvalue())


class TestExtractTextFromDocx(unittest.TestCase):
    def setUp(self):
        self.dummy_docx_path = "dummy_path.docx"
        return super().setUp()

    @patch('TextExtraction.Document')
    def test_extract_text_success(self, mock_document):
        """Проверка корректной обработки docx файла"""
        mock_paragraph_1 = MagicMock()
        mock_paragraph_1.text = "Первый параграф."

        mock_paragraph_2 = MagicMock()
        mock_paragraph_2.text = "Второй параграф."

        mock_document.return_value.paragraphs = [mock_paragraph_1, mock_paragraph_2]

        result = extract_text_from_docx(self.dummy_docx_path)

        expected_result = "Первый параграф.\nВторой параграф."
        self.assertEqual(result, expected_result)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('TextExtraction.Document')
    def test_extract_text_failure(self, mock_document, mock_stdout):
        """Проверка обработки исключений"""
        mock_document.side_effect = Exception("Вызов исключения из unittest")
        
        extract_text_from_docx(self.dummy_docx_path)
        self.assertIn("Вызов исключения из unittest", mock_stdout.getvalue())


class TestExtractTextFromDjvu(unittest.TestCase):
    def setUp(self):
        self.dummy_djvu_path = "dummy_path.djvu"
        return super().setUp()
    
    @patch('TextExtraction.subprocess.run')
    def test_extract_text_success(self, mock_run):
        mock_run.return_value = MagicMock(stdout="Извлеченный текст из DJVU.")
        
        result = extract_text_from_djvu(self.dummy_djvu_path)
        self.assertEqual(result, "Извлеченный текст из DJVU.")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('TextExtraction.subprocess.run')
    def test_extract_text_failure(self, mock_run, mock_stdout):
        mock_run.side_effect = Exception("Вызов исключения из unittest")
        
        extract_text_from_djvu(self.dummy_djvu_path)
        self.assertIn("Вызов исключения из unittest", mock_stdout.getvalue())


class TestExtractTextFromDoc(unittest.TestCase):
    def setUp(self):
        self.dummy_doc_path = "dummy_path.doc"
        return super().setUp()
    
    @patch('TextExtraction.subprocess.run')
    def test_extract_text_success(self, mock_run):
        mock_run.return_value = MagicMock(stdout="Извлеченный текст из DOC.")
        
        result = extract_text_from_doc(self.dummy_doc_path)
        self.assertEqual(result, "Извлеченный текст из DOC.")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('TextExtraction.subprocess.run')
    def test_extract_text_failure(self, mock_run, mock_stdout):
        mock_run.side_effect = Exception("Вызов исключения из unittest")
        
        extract_text_from_doc(self.dummy_doc_path)
        self.assertIn("Вызов исключения из unittest", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()