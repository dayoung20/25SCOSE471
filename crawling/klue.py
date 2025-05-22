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


def safe_get_text(driver, xpath):
    try:
        return driver.find_element(By.XPATH, xpath).text
    except NoSuchElementException:
        return "N/A"


def scrape_lecture(driver, idx, worksheet):
    url = f"https://klue.kr/lectures/{idx}"
    driver.get(url)
    time.sleep(1)

    try:
        title = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section[1]/div/div[1]/div[1]/div[2]/p[1]').text
        semester_and_name = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section[1]/div/div[1]/div[1]/div[1]/p[1]').text
        year = semester_and_name[0:4]
        semester_start_idx = semester_and_name.find('년')
        semester_last_idx = semester_and_name.find('-')
        semester = semester_and_name[semester_start_idx + 2:semester_last_idx]
        lecture_id = semester_and_name[semester_last_idx + 2:semester_last_idx + 9]
        lecture_class_id = semester_and_name[semester_last_idx + 11:semester_last_idx + 13]

    except NoSuchElementException:
        print(f"[{idx}] 강의 제목 또는 학기 없음")
        return

    score = safe_get_text(driver, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[1]/div[1]/span')
    attd_rate = safe_get_text(driver, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[2]/div/div[1]/span')
    avg_study = safe_get_text(driver, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[3]/div[1]/div[1]/div[1]/span[2]')
    avg_diff = safe_get_text(driver, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[3]/div[1]/div[2]/div[1]/span[2]')
    avg_performance = safe_get_text(driver, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[3]/div[2]/div[1]/div[1]/span[2]')
    avg_satisfaction = safe_get_text(driver, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[1]/div[3]/div[2]/div[2]/div[1]/span[2]')
    recc_rate = safe_get_text(driver, '//*[@id="root"]/div/div/section/section[1]/div/div[3]/div/div[2]/span')

    worksheet.append([
        idx, lecture_id, lecture_class_id, title, year, semester,
        score, attd_rate, avg_study, avg_diff, avg_performance, avg_satisfaction, recc_rate
    ])

    print(f"[{idx}] {lecture_id} {lecture_class_id} {title} {year} {semester} {score} {attd_rate} {avg_study} {avg_diff} {avg_performance} {avg_satisfaction} {recc_rate}")


def run_scraper(email, password, start_idx, end_idx, output_file):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=options)

    login(driver, email, password)
    time.sleep(2)

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.append(["Idx", "ID", "Class", "Title", "Year", "Semester", "Average Score", "Attd_rate", "avg_study", "avg_diff", "avg_performance", "avg_satisfaction", "recc_rate"])

    # 순서에 따라 반복 범위 설정
    if start_idx > end_idx:
        index_range = range(start_idx, end_idx - 1, -1)
    else:
        index_range = range(start_idx, end_idx + 1)

    for idx in index_range:
        scrape_lecture(driver, idx, worksheet)

    workbook.save(output_file)
    driver.quit()


# 실행 설정
total_start = 140000
total_end = 150000
chunk_size = 10000

# 내림차순으로 파일 분할 실행
for i in range(total_end, total_start - 1, -chunk_size):
    chunk_end = i
    chunk_start = max(i - chunk_size + 1, total_start)
    file_index = (total_end - chunk_end) // chunk_size 
    output_filename = f"klue_lectures_desc_{file_index}.xlsx" 

    print(f"Scraping from {chunk_end} down to {chunk_start} -> {output_filename}")
    run_scraper("dayoung20", "da3417!00", start_idx=chunk_end, end_idx=chunk_start, output_file=output_filename)
