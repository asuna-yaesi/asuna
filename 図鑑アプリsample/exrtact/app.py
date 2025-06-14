from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = ""
driver.get(url)

file_path = '抽出テキスト.txt'

all_data = []

try:
    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="search_table"]/div//img'))
            )
            images = driver.find_elements(By.XPATH, '//*[@id="search_table"]/div//img')

            for i in range(len(images)):
                try:
                    data_src = images[i].get_attribute('data-src')
                    image_url = data_src if data_src else images[i].get_attribute('src')

                    if "blank.gif" in image_url:
                        print("プレースホルダー画像をスキップしました")
                        continue

                    driver.execute_script("arguments[0].scrollIntoView(true);", images[i])
                    images[i].click()

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="maincontents"]/div[1]/h2'))
                    )
                    product_name = driver.find_element(By.XPATH, '//*[@id="maincontents"]/div[1]/h2').text

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="maincontents"]/div[3]/dl'))
                    )
                    text = driver.find_element(By.XPATH, '//*[@id="maincontents"]/div[3]/dl').text

                    content = f"リンク先: {driver.current_url}\n画像: {image_url}\n商品名: {product_name}\n{text}\n\n"
                    all_data.append(content)

                    driver.back()

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="search_table"]/div//img'))
                    )
                    images = driver.find_elements(By.XPATH, '//*[@id="search_table"]/div//img')

                except Exception as e:
                    print("エラーが発生しました:", e)
                    driver.back()

            try:
                next_link = driver.find_element(By.CSS_SELECTOR, "div.send_next > a")
                next_page_url = next_link.get_attribute('href')
    
                driver.get(next_page_url) 
                time.sleep(3)

            except Exception as e:
                print("最終ページに到達しました。")
                break

        except Exception as e:
            print("ページの読み込み中にエラーが発生しました:", e)
            break

finally:
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(all_data)

    print("取得したデータをファイルに保存しました。")
    driver.quit()
