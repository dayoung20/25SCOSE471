
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import openpyxl
import time

def login(driver, email, password):
    driver.get("https://klue.kr/")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/header/div/div/div[2]/a[1]'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/section/div/div/div/div/input[1]'))
    ).send_keys(email)

    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/div/div/div/div/input[2]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/div/div/div/div/button').click()

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=options)


def scrape_lecture(driver, lecture_id, worksheet):
    url = f"https://klue.kr/lectures/{lecture_id}"
    driver.get(url)
    time.sleep(1)
    title = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section[1]/div/div[1]/div[1]/div[2]/p[1]').text
    semester = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section[1]/div/div[1]/div[1]/div[1]/p[1]').text
    # 없는 값 Null 들어가도록 -> TODO : 독립적으로
    try:
        score = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[1]/div[1]/span').text
        attd_rate = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[2]/div/div[1]/span').text
        avg_study = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[3]/div[1]/div[1]/div[1]/span[2]').text
        avg_diff = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[3]/div[1]/div[2]/div[1]/span[2]').text
        avg_performance = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[3]/div[2]/div[1]/div[1]/span[2]').text
        avg_satisfaction = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[3]/div[2]/div[2]/div[1]/span[2]').text
        worksheet.append([lecture_id, title, semester, score, attd_rate, avg_study, avg_diff, avg_performance, avg_satisfaction])
        print(f"[{lecture_id}] {title} {semester} {score} {attd_rate} {avg_study} {avg_diff} {avg_performance} {avg_satisfaction}")
    
    except NoSuchElementException:
        score = "N/A"
        attd_rate = "N/A"
        avg_study = "N/A"
        avg_diff = "N/A"
        avg_performance = "N/A"
        avg_satisfaction = "N/A"
        print(f"[{lecture_id}] 강의 없음 또는 비공개")

    except Exception as e:
        print(f"[{lecture_id}] 오류 발생: {e}")

def run_scraper(email, password, start_id=1, end_id=1000, output_file="klue_lectures.xlsx"):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=options)

    login(driver, email, password)
    time.sleep(2)

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.append(["Lecture ID", "Title", "Semester", "Average Score", "Attd_rate", "avg_study", "avg_diff", "avg_performance", "avg_satisfaction"])

    for lecture_id in range(start_id, end_id + 1):
        scrape_lecture(driver, lecture_id, worksheet)

    workbook.save(output_file)
    driver.quit()

# 실행
run_scraper("id", "pwd", start_id=1, end_id=10)
