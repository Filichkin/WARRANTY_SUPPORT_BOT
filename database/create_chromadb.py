import time

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger

import torch


CHROMA_PATH = './warranty_chroma_db'
COLLECTION_NAME = 'warranty_data'
