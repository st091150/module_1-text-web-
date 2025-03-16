import argparse
import subprocess
from pdfminer.high_level import extract_text as pdfminer_extract_text
from pdf2image import convert_from_path
import pytesseract
from docx import Document

def extract_text_from_pdf(pdf_path):
    """
    Извлекает текст из файла PDF.
    Если текст недоступен (например, в сканированных PDF), используется OCR (распознавание текста).
    """
    try:
        # Попытка извлечь текст напрямую
        text = pdfminer_extract_text(pdf_path)
        if text.strip():  # Если текст не пустой
            return text
        else:
            # Если текст пустой, используем OCR
            images = convert_from_path(pdf_path)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image, lang='rus')  # Язык: русский
            return text
    except Exception as e:
        print(f"Ошибка при извлечении текста из PDF: {e}")
        return ""
    
def extract_text_from_docx(docx_path):
    """
    Извлекает текст из файла DOCX.
    """
    try:
        doc = Document(docx_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Ошибка при извлечении текста из DOCX: {e}")
        return ""
    
def extract_text_from_djvu(djvu_path):
    """
    Извлекает текст из файла DJVU с использованием внешнего инструмента djvutxt.
    """
    try:
        # Используем djvutxt для извлечения текста
        result = subprocess.run(['djvutxt', djvu_path], capture_output=True, text=True, encoding='utf-8')
        return result.stdout
    except Exception as e:
        print(f"Ошибка при извлечении текста из DJVU: {e}")
        return ""
    
def extract_text_from_doc(doc_path):
    """
    Извлекает текст из файла DOC (старый формат Word) с использованием внешнего инструмента antiword.
    """
    try:
        # Используем antiword для извлечения текста
        result = subprocess.run(['antiword', doc_path], capture_output=True, text=True, encoding='utf-8')
        return result.stdout
    except Exception as e:
        print(f"Ошибка при извлечении текста из DOC: {e}")
        return ""
    
def extract_text(file_path):
    """
    Извлекает текст из файла в зависимости от его расширения.
    Поддерживаемые форматы: PDF, DOC, DOCX, DJVU.
    """
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.djvu'):
        return extract_text_from_djvu(file_path)
    elif file_path.endswith('.doc'):
        return extract_text_from_doc(file_path)
    else:
        print(f"Формат файла не поддерживается: {file_path}")
        return ""
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Извлечение текста из файла (.djvu, .docx, .pdf, .doc')
    parser.add_argument('file_path', type=str, help='Путь к файлу')

    args = parser.parse_args()
    
    file_path = args.file_path

    text = extract_text(file_path)

    print(text)