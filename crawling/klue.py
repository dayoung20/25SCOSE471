
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

def safe_get_text(driver,xpath):
    try:
        return driver.find_element(By.XPATH, xpath).text
    except NoSuchElementException:
        return "N/A"



def scrape_lecture(driver, lecture_id, worksheet):
    url = f"https://klue.kr/lectures/{lecture_id}"
    driver.get(url)
    time.sleep(1)

    try:
        title = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section[1]/div/div[1]/div[1]/div[2]/p[1]').text
        semester = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section[1]/div/div[1]/div[1]/div[1]/p[1]').text
    except NoSuchElementException:
        print(f"[{lecture_id}] 강의 제목 또는 학기 없음")
        return

    score = safe_get_text(driver, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[1]/div[1]/span')
    attd_rate = safe_get_text(driver, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[2]/div/div[1]/span')
    avg_study = safe_get_text(driver, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[3]/div[1]/div[1]/div[1]/span[2]')
    avg_diff = safe_get_text(driver, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[3]/div[1]/div[2]/div[1]/span[2]')
    avg_performance = safe_get_text(driver, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[3]/div[2]/div[1]/div[1]/span[2]')
    avg_satisfaction = safe_get_text(driver, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[3]/div[2]/div[2]/div[1]/span[2]')

    worksheet.append([
        lecture_id, title, semester,
        score, attd_rate, avg_study,
        avg_diff, avg_performance, avg_satisfaction
    ])

    print(f"[{lecture_id}] {title} {semester} {score} {attd_rate} {avg_study} {avg_diff} {avg_performance} {avg_satisfaction}")


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
