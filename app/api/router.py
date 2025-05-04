from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse

from app.api.schemas import AskResponse, AskWithAIResponse
from app.chroma_client.ai_store import ChatWithAI
from app.chroma_client.chroma_store import ChromaVectorStore, get_vectorstore
from app.users.dependencies import get_current_user


router = APIRouter(prefix='/ai_agent', tags=['AI_agent'])


@router.post('/ask')
async def ask(
    query: AskResponse,
    vectorstore: ChromaVectorStore = Depends(get_vectorstore),
    user_id: int = Depends(get_current_user),
):
    results = await vectorstore.asimilarity_search(
        query=query.response,
        with_score=True,
        k=10
    )
    formatted_results = []
    for doc, score in results:
        formatted_results.append({
            'text': doc.page_content,
            'metadata': doc.metadata,
            'similarity_score': score,
        })
    return {'results': formatted_results}
