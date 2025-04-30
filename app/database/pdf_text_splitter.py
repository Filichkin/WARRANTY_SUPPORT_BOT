from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


PATH = 'data/warranty_policy.pdf'
CHUNK_SIZE = 512
CHUNK_OVERLAP = 100


def load_documents(path):

    loader = PyPDFLoader(PATH)
    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True,
    )

    texts = text_splitter.split_documents(pages)

    return texts
