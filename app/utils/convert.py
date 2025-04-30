import os

from docling.document_converter import DocumentConverter


DATABASE = os.listdir('./data')

converter = DocumentConverter()

processed_text = []
for file in DATABASE:
    result = converter.convert(f'./data/{file}')
    content = result.document.export_to_markdown()
    processed_text.append(content)

with open('re-example.md', 'wt') as file:
    file.write('\n'.join(processed_text))
