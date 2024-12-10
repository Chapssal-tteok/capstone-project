from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma

# 래핑된 SentenceTransformer 클래스 정의
class LangChainSentenceTransformer:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts):
        return [self.model.encode(text) for text in texts]
    
    def embed_query(self, text):
        return self.model.encode(text)

# Step 2: 사용자 입력 기반 검색
def search_db(query, persist_directory="./db"):
    print("[2] 사용자 입력 기반 검색")

    # 래핑된 SentenceTransformer 임베딩 함수 사용
    embedding_function = LangChainSentenceTransformer('all-MiniLM-L6-v2')

    # ChromaDB 로드
    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function
    )

    # 검색 실행
    results = db.similarity_search(query, k=3)
    print(f"검색 결과 ({len(results)}개 문서 반환):")
    for result in results:
        print(result)

if __name__ == "__main__":
    # 사용자 쿼리
    user_query = "현대모비스 면접에서 자주 나오는 질문이 무엇인가요??"
    
    # Step 2: 검색 테스트
    search_db(query=user_query, persist_directory="./db")