from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


PATH = 'data/warranty_policy.pdf'
CHUNK_SIZE = 512
CHUNK_OVERLAP = 10

loader = PyPDFLoader(PATH)
pages = loader.load_and_split()
print(f'Loaded {len(pages)} pages from the PDF')

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
    add_start_index=True,
)

texts = text_splitter.split_documents(pages)

print(f'Split the pages in {len(texts)} chunks')
print(texts[10])
print(texts[11])
