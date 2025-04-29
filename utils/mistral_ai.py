import os

from mistralai import Mistral


DATABASE = os.listdir('./data')

API_KEY = os.getenv('MISTRAL_TOKEN')

MODEL = 'mistral-small-latest'

PATH = './data/dealer_agreement.pdf'

messages = []
user_message_content = [{"type": "text", "text": user_message}]


def run_mistral(user_message):
    client = Mistral(api_key=API_KEY)
    
    uploaded_pdf = client.files.upload(
        file={
            'file_name': 'dealer_agreement.pdf',
            'content': open(PATH, 'rb'),
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
                    'text': user_message
                },
                {
                    'type': 'document_url',
                    # "document_url": "https://arxiv.org/pdf/1805.04770"
                    'document_url': signed_url.url
                },
                {
                    'type': 'document_url',
                    # "document_url": "https://arxiv.org/pdf/1805.04770"
                    'document_url': signed_url.url
                },
            ]
        }
    ]
    chat_response = client.chat.complete(
        model=MODEL,
        messages=messages
    )
    return chat_response.choices[0].message.content


if __name__ == '__main__':
    print(run_mistral('Опиши основные термины дилерского договора'))
