import os

from docling.document_converter import DocumentConverter


DATABASE = os.listdir('/Users/alexeyfilichkin/MainDev/WARRANTY_SUPPORT_BOT/app/database/data/PDF')

converter = DocumentConverter()

processed_text = []
for file in DATABASE:
    result = converter.convert(f'/Users/alexeyfilichkin/MainDev/WARRANTY_SUPPORT_BOT/app/database/data/PDF/{file}')
    content = result.document.export_to_markdown()
    processed_text.append(content)
    with open(f'{file}.md', 'wt') as file:
        file.write('\n'.join(processed_text))


