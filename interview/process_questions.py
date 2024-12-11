import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain_chroma import Chroma
from langchain.docstore.document import Document

# SentenceTransformer를 LangChain과 호환되도록 확장한 클래스
# 텍스트를 벡터로 변환하여 검색 및 유사도 계산에 사용됨
class LangChainSentenceTransformer:
    def __init__(self, model_name):
        # SentenceTransformer 모델 로드
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts):
        # 다중 텍스트를 임베딩(벡터) 형태로 변환
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()  # 리스트 형태로 변환하여 반환
    
    def embed_query(self, text):
        # 단일 텍스트(쿼리)를 임베딩(벡터) 형태로 변환
        return self.model.encode([text])[0]

# ChromaDB 초기화 함수
# CSV 데이터를 불러와 ChromaDB로 저장하거나 기존 DB를 갱신
def init_db(csv_filename="dataset_question.csv", persist_directory="./db"):
    print("CSV 파일 로드 및 DB 초기화")

    # CSV 파일 존재 여부 확인
    if not os.path.exists(csv_filename):
        raise FileNotFoundError(f"CSV 파일이 존재하지 않습니다: {csv_filename}")
    
    # CSV 데이터를 DataFrame으로 로드
    data = pd.read_csv(csv_filename)
    print("CSV 데이터 로드 완료:")
    print(data.head())

    # Document 객체 생성 (각 행을 Document 형식으로 변환)
    documents = [
        Document(
            page_content=f"{row['질문']} [기업명: {row['기업명']}, 경력: {row['경력']}, 직무: {row['직무']}]",
            metadata={"기업명": row["기업명"], "경력": row["경력"], "직무": row["직무"]}
        )
        for _, row in data.iterrows() if pd.notna(row["질문"]) and row["질문"].strip() != ""
    ]

    # SentenceTransformer 임베딩 함수 생성
    embedding_function = LangChainSentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    # 기존 ChromaDB 삭제 후 새로 생성
    if os.path.exists(persist_directory):
        import shutil
        shutil.rmtree(persist_directory)
        print("기존 ChromaDB를 삭제했습니다.")

    print("새로운 ChromaDB 생성 중...")
    db = Chroma.from_documents(
        documents,
        embedding_function,
        persist_directory=persist_directory
    )
    
    # 저장된 문서 수 출력
    print(f"DB 저장 완료. 저장된 문서 개수: {len(documents)}")
    return db

# 검색 함수
# 사용자 입력 쿼리를 기반으로 유사도가 높은 문서를 검색하여 출력
def search_db(query, persist_directory="./db"):
    print("사용자 입력 기반 검색 시작")

    # SentenceTransformer 임베딩 함수 생성
    embedding_function = LangChainSentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    # 기존 ChromaDB 로드
    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function
    )

    # 유사도 검색 실행 (가장 유사한 3개의 문서 반환)
    results = db.similarity_search(query, k=3)

    # 검색 결과 출력
    print(f"검색 결과 ({len(results)}개 문서 반환):")
    for result in results:
        print(f"질문: {result.page_content}")
        print(f"메타데이터: {result.metadata}")
        print("---")

# 메인 실행 코드
if __name__ == "__main__":
    # CSV 파일 경로 설정
    csv_file_path = "dataset_question.csv"

    # 데이터베이스 초기화 실행
    db = init_db(csv_filename=csv_file_path, persist_directory="./db")

    # 사용자 입력 쿼리 설정
    user_query = "반도체 관련 기술 질문을 알려주세요."

    # 검색 실행
    search_db(query=user_query, persist_directory="./db")
