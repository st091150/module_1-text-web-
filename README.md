# Парсеры

Этот проект содержит два парсера: analyze_web и text_extract. 

## Описание программ

### 1. analyze_web

Эта программа принимает URL-адрес веб-страницы из консоли и парсит следующие элементы:
- Заголовок страницы (<title>)
- Ссылки (<a>)
- Параграфы (<p>)
- Изображения (<img>)

#### Использование

Запустите программу с помощью команды: python analyze_web.py <URL>

Замените <URL> на адрес веб-страницы, которую вы хотите проанализировать.

### 2. text_extract

Эта программа принимает файл с расширением .pdf, .doc, .docx или .djvu и извлекает текст из него. Также она может распарсить изображения с такими же расширениями.

#### Использование

Запустите программу с помощью команды: python textextract.py <путь_к_файлу>

Замените <путь_к_файлу> на путь к файлу, из которого вы хотите извлечь текст.

## Тестирование

В проекте также имеются тесты, написанные с использованием библиотеки unittest. Для запуска тестов выполните следующую команду: python <test_file>.py [-v](для подробной информации)

## Установка зависимостей

Не забудьте установить все необходимые зависимости. Вы можете сделать это, выполнив команду: pip install -r requirements.txt
