from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma

# SentenceTransformer를 LangChain과 호환되도록 확장한 클래스
class LangChainSentenceTransformer:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts):
        # 다중 텍스트를 임베딩(벡터) 형태로 변환
        return [self.model.encode(text) for text in texts]
    
    def embed_query(self, text):
        # 단일 쿼리를 임베딩(벡터) 형태로 변환
        return self.model.encode(text)

# ChromaDB에서 사용자 입력(쿼리)을 기반으로 검색 수행
def search_db(query, persist_directory="./db"):
    print("사용자 입력 기반 검색 시작")

    # SentenceTransformer 기반 임베딩 함수 생성
    embedding_function = LangChainSentenceTransformer('all-MiniLM-L6-v2')

    # ChromaDB 로드 (기존 데이터베이스에서 검색 수행)
    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function
    )

    # 유사도 검색 실행 (가장 유사한 k개의 문서 반환)
    results = db.similarity_search(query, k=3)

    # 검색 결과 출력
    print(f"검색 결과 ({len(results)}개 문서 반환):")
    for result in results:
        print(result)

if __name__ == "__main__":
    # 사용자 쿼리 입력 (검색할 키워드 또는 문장)
    user_query = "현대모비스 기계엔지니어 면접에서 기술적인 질문은 어떤 것이 있나요?"
    
    # ChromaDB에서 쿼리 검색 실행
    search_db(query=user_query, persist_directory="./db")