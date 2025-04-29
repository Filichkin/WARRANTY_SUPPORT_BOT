import os

from mistralai import Mistral

MODEL = 'mistral-small-latest'
DATABASE = os.listdir('./data')
PATH = './data/'
API_KEY = os.getenv('MISTRAL_TOKEN')

client = Mistral(api_key=API_KEY)

messages = []
user_message_content = [
    {
        'type': 'text',
        'text': 'Кто принимает решение по гарантийному ремонту'
    }
]

for file in DATABASE:
    uploaded_pdf = client.files.upload(
        file={
            'file_name': 'dealer_agreement.pdf',
            'content': open(f'./data/{file}', 'rb')
            },
        purpose='ocr'
    )
    signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)
    user_message_content.append(
        {
            'type': 'document_url',
            'document_url': signed_url.url
        }
    )
messages.append({'role': 'user', 'content': user_message_content})

chat_response = client.chat.complete(
        model=MODEL,
        messages=messages
    )
print(chat_response.choices[0].message.content)
