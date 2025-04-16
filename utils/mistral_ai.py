import os

from mistralai import Mistral


API_KEY = os.getenv('MISTRAL_TOKEN')

MODEL = 'mistral-small-latest'


def run_mistral(user_message):
    client = Mistral(api_key=API_KEY)

    uploaded_pdf = client.files.upload(
        file={
            'file_name': 're_test.pdf',
            'content': open('./re_test.pdf', 'rb'),
            },
        purpose='ocr'
    )
    signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)

    messages = [
        {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': 'Сделай небольшой тренинг из 20 предложений'
                },
                {
                    'type': 'document_url',
                    # "document_url": "https://arxiv.org/pdf/1805.04770"
                    'document_url': signed_url.url
                }
            ]
        }
    ]
    chat_response = client.chat.complete(
        model=MODEL,
        messages=messages
    )
    return chat_response.choices[0].message.content

