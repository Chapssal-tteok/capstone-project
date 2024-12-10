import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document

# SentenceTransformer를 LangChain과 호환되도록 확장한 클래스 (텍스트를 벡터로 변환하는 기능 제공)
class LangChainSentenceTransformer:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts):
        # 다중 텍스트를 임베딩(벡터) 형태로 변환
        return [self.model.encode(text) for text in texts]
    
    def embed_query(self, text):
        # 단일 쿼리를 임베딩(벡터) 형태로 변환
        return self.model.encode(text)

# ChromaDB 초기화 함수
# CSV 데이터를 로드하고 임베딩한 뒤, ChromaDB에 저장하거나 기존 DB를 불러옴
def init_db(csv_filename="dataset_question.csv", persist_directory="./db"):
    print("CSV 파일 로드 및 DB 초기화")

    # CSV 파일 존재 여부 확인
    if not os.path.exists(csv_filename):
        raise FileNotFoundError(f"CSV 파일이 존재하지 않습니다: {csv_filename}")
    
    # CSV 데이터를 DataFrame으로 로드
    data = pd.read_csv(csv_filename)
    print("CSV 데이터 로드 완료:")
    print(data.head())  # 데이터 일부를 출력하여 확인

    # 각 행의 데이터를 LangChain Document 형식으로 변환
    documents = [
        Document(page_content=row["질문"], metadata={"기업명": row["기업명"], "경력": row["경력"], "직무": row["직무"]})
        for _, row in data.iterrows()
    ]

    # SentenceTransformer 기반 임베딩 함수 생성
    embedding_function = LangChainSentenceTransformer('all-MiniLM-L6-v2')

    # 기존 ChromaDB가 존재하는지 확인
    if os.path.exists(persist_directory):
        print("기존 ChromaDB 로드 중...")
        # 기존 DB 로드
        db = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_function
        )
    else:
        print("새로운 ChromaDB 생성 중...")
        # 새로운 DB 생성 및 문서 추가
        db = Chroma.from_documents(
            documents,
            embedding_function,
            persist_directory=persist_directory
        )
    
    # DB에 저장된 문서 수 출력
    print(f"DB 저장 완료. 저장된 문서 개수: {len(documents)}")
    return db

# 메인 함수
if __name__ == "__main__":
    # CSV 파일 경로 설정
    csv_file_path = "dataset_question.csv"

    # ChromaDB 초기화 수행
    db = init_db(csv_filename=csv_file_path, persist_directory="./db")
