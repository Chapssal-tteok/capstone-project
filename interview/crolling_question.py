import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# WebDriver의 경로 설정 (크롬 드라이버의 위치 지정)
driver_path = "C:\\Users\\ShinJunghwa\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
service = Service(executable_path=driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# 출력할 CSV 파일 경로
output_file = "dataset_question.csv"

# CSV 파일이 이미 존재하는지 확인
# 파일이 존재하면 데이터가 추가되고, 없으면 새로 생성
file_exists = os.path.exists(output_file)

# CSV 파일 열기 (쓰기 또는 추가 모드)
# 파일이 없을 경우 'w' 모드, 파일이 있을 경우 'a' 모드
with open(output_file, mode="a" if file_exists else "w", newline="", encoding="utf-8") as file:
    # 데이터를 큰따옴표로 감싸도록 설정
    writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_ALL)
    
    # CSV 파일이 새로 생성된 경우에만 헤더 추가
    if not file_exists:
        writer.writerow(["기업명", "경력", "직무", "질문"])  # CSV 파일의 헤더 작성

    for page_number in range(1, 17):

        # 웹페이지 URL을 동적으로 생성하여 접속
        web_url = f"https://www.jobkorea.co.kr/starter/review/view?FavorCo_Stat=0&schTxt=%EC%82%BC%EC%84%B1&OrderBy=0&Page=1&C_Idx=1&Half_Year_Type_Code=0&Ctgr_Code=5&VPage={page_number}"
        driver.get(web_url) # 해당 URL로 이동

        # 회사명 크롤링
        company_name = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[1]/div/h2/strong/a').text

        # 각 질문 항목 크롤링
        item_index = 1
        while True:
            try:
                # 각 질문의 상세 정보 가져오기
                # 경력 정보 크롤링 (예: 신입, 경력 등)
                employment_type = driver.find_element(
                    By.XPATH, f'//*[@id="container"]/div[2]/div[3]/ul/li[{item_index}]/div/span[1]/span[2]'
                ).text
                # 직무 정보 크롤링 (예: 개발, 디자인 등)
                department = driver.find_element(
                    By.XPATH, f'//*[@id="container"]/div[2]/div[3]/ul/li[{item_index}]/div/span[2]'
                ).text
                # 질문 내용 크롤링
                question = driver.find_element(
                    By.XPATH, f'//*[@id="container"]/div[2]/div[3]/ul/li[{item_index}]/div/span[3]'
                ).text

                # 크롤링된 데이터를 CSV 파일에 작성
                writer.writerow([company_name, employment_type, department, question])
                print(f"{company_name},{employment_type},{department},{question}")
                
                # 다음 질문 항목으로 이동
                item_index += 1
            except NoSuchElementException:
                # 더 이상 항목이 없으면 반복문 종료
                break

# WebDriver 종료
driver.quit()

# 작업 완료 메시지 출력
print(f"크롤링 완료! 데이터가 '{output_file}'에 저장되었습니다.")