from chromadb.config import Settings
from chromadb import Client
from sentence_transformers import SentenceTransformer

def search_in_chromadb(user_input, collection, model_name='all-MiniLM-L6-v2'):
    print("[4] 사용자 입력 기반 질문 검색")
    model = SentenceTransformer(model_name)
    query_embedding = model.encode(user_input).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    print("검색 결과:")
    for doc, meta in zip(results["documents"], results["metadatas"]):
        print(f"질문: {doc}")
        print(f"메타데이터: {meta}")

if __name__ == "__main__":
    # ChromaDB 초기화
    db_directory = "./db"
    client = Client(Settings(persist_directory=db_directory))
    collection = client.get_collection(name="interview_questions")

    # 사용자 입력 기반 테스트 실행
    user_query = "현대모비스에서 근무하고 싶은 이유에 대해 질문할 수 있는 예문"
    search_in_chromadb(user_query, collection)
