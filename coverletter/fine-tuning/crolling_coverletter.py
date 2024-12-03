from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import jsonlines

# WebDriver의 경로 설정
driver_path = "C:\\Users\\ShinJunghwa\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
service = Service(executable_path=driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# 로그인 페이지 열기
driver.get("https://www.jobkorea.co.kr/Login")

# 로그인 정보 입력
username = "jungh150"  # 잡코리아 아이디 입력
password = "jungh051248!"  # 잡코리아 비밀번호 입력

# 아이디 입력 필드 찾기 및 입력
id_field = driver.find_element(By.ID, "M_ID")
id_field.send_keys(username)

# 비밀번호 입력 필드 찾기 및 입력
pw_field = driver.find_element(By.ID, "M_PWD")
pw_field.send_keys(password)

# 로그인 버튼 클릭
login_button = driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/section[3]/button')
login_button.click()

# 로그인 완료 대기 (필요에 따라 조정)
time.sleep(3)

# 웹페이지 열기
driver.get("https://www.jobkorea.co.kr/starter/PassAssay/View/241981?Page=1&OrderBy=0&FavorCo_Stat=0&schPart=1000229%2C1000230%2C1000231%2C1000232&Pass_An_Stat=0")

# 버튼 클릭 (답변들이 전부 보이게)
idx = 3
while True:
    try:
        btn = driver.find_element(By.XPATH, f'//*[@id="container"]/div[2]/div[2]/dl/dt[{idx}]/button')
        btn.click()
        idx += 1
    except NoSuchElementException:
        break

# 웹페이지에서 요소 찾기
company = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[1]/div[1]/h2/strong/a').text
part = driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[1]/div[1]/h2/em').text
print(company)
print(part)

idx = 1
while True:
    try:
        question = driver.find_element(By.XPATH, f'//*[@id="container"]/div[2]/div[2]/dl/dt[{idx}]/button/span[2]').text
        answer = driver.find_element(By.XPATH, f'//*[@id="container"]/div[2]/div[2]/dl/dd[{idx}]/div').text
        print(f'Q{idx}.')
        print(question)
        print(f'A{idx}.')
        print(answer)
        idx += 1

        new_message = {
            "messages": [
                {
                    "role": "system",
                    "content": f"당신은 {company}의 {part} 파트에 지원한 지원자의 자기소개서를 첨삭하고 피드백하는 일을 해야 합니다."
                },
                {
                    "role": "user",
                    "content": f"질문: [{question}] 답변: [지원자의 답변]"
                },
                {
                    "role": "assistant",
                    "content": f"모범 답변: [{answer}]"
                }
            ]
        }
        # 'dataset.jsonl' 파일에 새로운 메시지 추가
        with jsonlines.open('dataset_coverletter.jsonl', mode='a') as writer:
            writer.write(new_message)
    except NoSuchElementException:
        break

# 웹페이지 닫기
driver.quit()