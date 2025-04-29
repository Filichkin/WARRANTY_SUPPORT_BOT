import os

from pypdf import PdfReader


DATABASE = os.listdir('./data')


def process_pdf(database):
    # Process PDF file
    processed_text = []
    for file in database:
        pdf_reader = PdfReader(f'./data/{file}')
        text = ''.join(page.extract_text() for page in pdf_reader.pages)
        processed_text.append(text)
    return processed_text


print(process_pdf(DATABASE))
