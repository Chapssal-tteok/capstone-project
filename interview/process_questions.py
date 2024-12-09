import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document

# 래핑된 SentenceTransformer 클래스 정의
class LangChainSentenceTransformer:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts):
        return [self.model.encode(text) for text in texts]
    
    def embed_query(self, text):
        return self.model.encode(text)

# Step 1: CSV 파일 로드 및 초기화
def init_db(csv_filename="dataset_question.csv", persist_directory="./db"):
    print("[1] CSV 파일 로드 및 DB 초기화")

    # CSV 데이터 확인 및 로드
    if not os.path.exists(csv_filename):
        raise FileNotFoundError(f"CSV 파일이 존재하지 않습니다: {csv_filename}")
    data = pd.read_csv(csv_filename)
    print("CSV 데이터 로드 완료:")
    print(data.head())

    # Document 객체로 변환
    documents = [
        Document(page_content=row["질문"], metadata={"기업명": row["기업명"], "경력": row["경력"], "직무": row["직무"]})
        for _, row in data.iterrows()
    ]

    # 래핑된 SentenceTransformer 임베딩 함수 사용
    embedding_function = LangChainSentenceTransformer('all-MiniLM-L6-v2')

    # ChromaDB가 이미 존재하는지 확인
    if os.path.exists(persist_directory):
        print("기존 ChromaDB 로드 중...")
        db = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_function
        )
    else:
        print("새로운 ChromaDB 생성 중...")
        # 문서를 DB에 추가하고 저장
        db = Chroma.from_documents(
            documents,
            embedding_function,
            persist_directory=persist_directory
        )
    
    # 저장된 문서 수 확인
    print(f"DB 저장 완료. 저장된 문서 개수: {len(documents)}")
    return db

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

# 메인 함수
if __name__ == "__main__":
    # CSV 파일 경로
    csv_file_path = "dataset_question.csv"

    # Step 1: ChromaDB 초기화
    db = init_db(csv_filename=csv_file_path, persist_directory="./db")

    # Step 2: 검색 테스트
    user_query = "현대자동차에 지원하는 이유는 무엇인가요?"
    search_db(query=user_query, persist_directory="./db")
