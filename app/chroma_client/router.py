from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.chroma_client.schemas import AskResponse, AskWithAIResponse
from app.chroma_client.ai_store import ChatWithAI
from app.chroma_client.chroma_store import ChromaVectorStore, get_vectorstore
from app.constants import SEARCH_COUNT
from app.users.dependencies import get_current_user


router = APIRouter(prefix='/api', tags=['AI_agent'])


@router.post('/ask')
async def ask(
    query: AskResponse,
    vectorstore: ChromaVectorStore = Depends(get_vectorstore),
    user_id: int = Depends(get_current_user),
):
    results = await vectorstore.asimilarity_search(
        query=query.response,
        with_score=True,
        k=SEARCH_COUNT
    )
    formatted_results = []
    for doc, score in results:
        formatted_results.append({
            'text': doc.page_content,
            'metadata': doc.metadata,
            'similarity_score': score,
        })
    return {'results': formatted_results}


@router.post('/ask_with_ai')
async def ask_with_ai(
    query: AskWithAIResponse,
    vectorstore: ChromaVectorStore = Depends(get_vectorstore),
    user_id: int = Depends(get_current_user),
):
    results = await vectorstore.asimilarity_search(
        query=query.response, with_score=True, k=SEARCH_COUNT
    )

    if results:
        ai_context = '\n'.join([doc.page_content for doc, _ in results])
        ai_store = ChatWithAI(provider=query.provider)

        async def stream_response():
            async for chunk in ai_store.astream_response(
                ai_context,
                query.response
            ):
                yield chunk

        return StreamingResponse(
            stream_response(),
            media_type='text/plain',
            headers={
                'Content-Type': 'text/plain',
                'Transfer-Encoding': 'chunked',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
            },
        )
    else:
        return {'response': 'Ничего не найдено'}
