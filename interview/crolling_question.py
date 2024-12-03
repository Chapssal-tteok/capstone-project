import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# WebDriver의 경로 설정
driver_path = "C:\\Users\\ShinJunghwa\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
service = Service(executable_path=driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# CSV 파일 경로
output_file = "dataset_question.csv"

# 파일 존재 여부 확인
file_exists = os.path.exists(output_file)

# CSV 파일 열기 (쓰기 또는 추가 모드)
with open(output_file, mode="a" if file_exists else "w", newline="", encoding="utf-8") as file:
    # 모든 데이터를 큰따옴표로 감싸도록 설정
    writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_ALL)
    
    # 파일이 없을 때만 헤더 추가
    if not file_exists:
        writer.writerow(["기업명", "경력", "직무", "질문"])  # CSV 헤더 작성

    for page_number in range(1, 17):

        # 웹페이지 열기
        web_url = f"https://www.jobkorea.co.kr/starter/review/view?FavorCo_Stat=0&schTxt=%EC%82%BC%EC%84%B1&OrderBy=0&Page=1&C_Idx=1&Half_Year_Type_Code=0&Ctgr_Code=5&VPage={page_number}"
        driver.get(web_url)

        # 회사명 크롤링
        company_name = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[1]/div/h2/strong/a').text

        # 각 질문 항목 크롤링
        item_index = 1
        while True:
            try:
                # 각 질문의 상세 정보 가져오기
                employment_type = driver.find_element(
                    By.XPATH, f'//*[@id="container"]/div[2]/div[3]/ul/li[{item_index}]/div/span[1]/span[2]'
                ).text
                department = driver.find_element(
                    By.XPATH, f'//*[@id="container"]/div[2]/div[3]/ul/li[{item_index}]/div/span[2]'
                ).text
                question = driver.find_element(
                    By.XPATH, f'//*[@id="container"]/div[2]/div[3]/ul/li[{item_index}]/div/span[3]'
                ).text

                # 데이터를 CSV 파일에 작성
                writer.writerow([company_name, employment_type, department, question])
                print(f"{company_name},{employment_type},{department},{question}")
                item_index += 1
            except NoSuchElementException:
                # 더 이상 항목이 없으면 반복 종료
                break

# 웹페이지 닫기
driver.quit()

print(f"크롤링 완료! 데이터가 '{output_file}'에 저장되었습니다.")