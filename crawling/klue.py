
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
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

login(driver, "dayoung20", "da3417!00")