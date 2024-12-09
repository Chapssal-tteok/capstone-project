import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
from chromadb import Client
from ast import literal_eval

# Step 1: CSV 파일 로드
def load_csv(file_path):
    print("[1] CSV 파일 로드")
    data = pd.read_csv(file_path)
    print(data.head())
    return data

# Step 2: 질문 데이터 벡터화
def vectorize_questions(data, model_name='all-MiniLM-L6-v2'):
    print("[2] 질문 데이터 벡터화")
    model = SentenceTransformer(model_name)
    data["embedding"] = data["질문"].apply(lambda x: model.encode(x).tolist())
    data.to_csv("vectorized_questions.csv", index=False)
    print("벡터화 완료! vectorized_questions.csv에 저장되었습니다.")
    return data

# Step 3: 벡터 DB에 데이터 저장
def store_in_chromadb(data, db_directory="C:/testtemp/db"):
    print("[3] 벡터 DB에 데이터 저장")

    if not os.path.exists(db_directory):
        os.makedirs(db_directory)
        print(f"디렉토리 생성: {db_directory}")

    # ChromaDB 클라이언트 초기화
    settings = Settings(persist_directory=db_directory)
    client = Client(settings)

    # 디버깅: Settings 정보 출력
    print("ChromaDB Settings:")
    print(f"persist_directory: {settings.persist_directory}")

    collection = client.get_or_create_collection(name="interview_questions")

    # 데이터를 벡터 DB에 추가
    for idx, row in data.iterrows():
        # embedding 데이터를 안전하게 변환
        embedding = row["embedding"]
        if isinstance(embedding, str):  # 문자열일 경우만 변환
            embedding = literal_eval(embedding)
        
        # 고유 ID 생성 (여기서는 인덱스를 사용)
        unique_id = f"question_{idx}"
        
        collection.add(
            ids=[unique_id],  # 고유 ID 추가
            documents=[row["질문"]],
            metadatas={"기업명": row["기업명"], "경력": row["경력"], "직무": row["직무"]},
            embeddings=[embedding]
        )

    print(f"디렉토리 내용: {os.listdir(db_directory)}")
    print(f"컬렉션 이름: {collection.name}")
    print(f"저장된 문서 개수: {collection.count()}")
    print("데이터가 ChromaDB에 저장되었습니다!")
    return collection

# 메인 함수
if __name__ == "__main__":
    # CSV 파일 경로
    csv_file_path = "dataset_question.csv"

    # Step 1: 데이터 로드
    data = load_csv(csv_file_path)

    # Step 2: 벡터화
    data = vectorize_questions(data)

    # Step 3: 벡터 DB에 저장
    collection = store_in_chromadb(data)
