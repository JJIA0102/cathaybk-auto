import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import re

def capture_screenshot(driver, filename):
    """截圖並儲存至指定檔案名稱"""
    driver.save_screenshot(filename)

def test_cathaybk_navigation():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1440,900")
    driver = webdriver.Chrome(service=Service(log_path="chromedriver.log"), options=chrome_options)

    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    #開啟首頁
    driver.get("https://www.cathaybk.com.tw/cathaybk")
    capture_screenshot(driver, f"{screenshot_dir}/{time.strftime('%Y%m%d_%H%M%S')}.png")

    #點擊開戶連結
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='開戶']"))
        )
        ActionChains(driver).move_to_element(element).click().perform()
    except Exception as e:
        driver.quit()
        assert False, f"找不到開戶連結或無法點擊：{e}"

    #等新分頁開啟並切換
    WebDriverWait(driver, 10).until(EC.new_window_is_opened)
    driver.switch_to.window(driver.window_handles[-1])

    try:
        WebDriverWait(driver, 10).until(EC.url_contains("open-account"))
        assert "open-account" in driver.current_url
    except Exception as e:
        driver.quit()
        assert False, f"頁面跳轉失敗：{e}"

    # 點擊他行驗證
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-anchor-btn='blockName02']"))
        )
        ActionChains(driver).move_to_element(element).click().perform()
    except Exception as e:
        driver.quit()
        assert False, f"找不到‘他行驗證’按鈕或無法點擊：{e}"

    #點擊「下載CUBE App」
    try:
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.presence_of_element_located((
            By.XPATH, "//a[@id='lnk_MajorButtonLink'][.//p[contains(text(), '下載CUBE App')]]"
        )))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
        time.sleep(1)
        try:
            wait.until(EC.element_to_be_clickable((
                By.XPATH, "//a[@id='lnk_MajorButtonLink'][.//p[contains(text(), '下載CUBE App')]]"
            )))
            button.click()
        except:
            driver.execute_script("arguments[0].click();", button)

        capture_screenshot(driver, f"{screenshot_dir}/{time.strftime('%Y%m%d_%H%M%S')}.png")
    except Exception as e:
        driver.quit()
        assert False, f"下載按鈕點擊失敗：{e}"

    #切換到下載分頁
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
    else:
        driver.quit()
        assert False, "新分頁未正確開啟"

    #驗證下載頁URL
    try:
        expected_url = "https://www.cathaybk.com.tw/cathaybk/promo/event/ebanking/product/appdownload/index.html?openExternalBrowser=1"
        assert driver.current_url.startswith(expected_url), f"頁面URL不符：{driver.current_url}"
        capture_screenshot(driver, f"{screenshot_dir}/{time.strftime('%Y%m%d_%H%M%S')}.png")
    except Exception as e:
        driver.quit()
        assert False, str(e)

    #驗證版本號是否一致
    try:
        android_text = driver.find_element(By.ID, "android").text.strip()
        ios_text = driver.find_element(By.ID, "ios").text.strip()
        android_ver = re.search(r"\d+(\.\d+)+", android_text).group()
        ios_ver = re.search(r"\d+(\.\d+)+", ios_text).group()
        assert android_ver == ios_ver, f"Android版本號：{android_ver}, iOS版本號：{ios_ver}"
    except Exception as e:
        driver.quit()
        assert False, f"版本號不一致或找不到元素：{e}"

    #驗證QRcode
    try:
        qrcode = driver.find_element(By.XPATH, "//img[contains(@src, 'qrcode')]")
        width = qrcode.get_attribute("width")
        height = qrcode.get_attribute("height")
        assert width == "160" and height == "160", f"QRcode尺寸不符：{width}x{height}"
    except Exception as e:
        driver.quit()
        assert False, f"QRcode尺寸驗證失敗：{e}"

    driver.quit()

    #開啟手機版
    mobile_driver = None
    try:
        mobile_emulation = { "deviceName": "iPhone X" }
        mobile_opts = Options()
        mobile_opts.add_experimental_option("mobileEmulation", mobile_emulation)
        mobile_opts.add_argument("--no-sandbox")
        mobile_opts.add_argument("--disable-dev-shm-usage")
        mobile_opts.add_argument("--disable-gpu")
        mobile_opts.add_argument("--disable-extensions")
        mobile_opts.add_argument("--disable-background-timer-throttling")
        mobile_opts.add_argument("--disable-renderer-backgrounding")
        mobile_opts.add_argument("--disable-backgrounding-occluded-windows")
        mobile_opts.add_argument("--renderer-process-limit=1")
        mobile_opts.add_argument("--js-flags=--max-old-space-size=4096")

        mobile_driver = webdriver.Chrome(service=Service(log_path="chromedriver.log"), options=mobile_opts)
        mobile_driver.set_page_load_timeout(180)

        for attempt in range(2):
            try:
                mobile_driver.get(expected_url)
                WebDriverWait(mobile_driver, 45).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(3)
                capture_screenshot(mobile_driver, f"{screenshot_dir}/{time.strftime('%Y%m%d_%H%M%S')}.png")
                break
            except Exception as e:
                if attempt == 1:
                    raise AssertionError(f"行動版截圖失敗（多次重試）：{e}")
                time.sleep(3)
    except Exception as e:
        if mobile_driver:
            capture_screenshot(mobile_driver, f"{screenshot_dir}/{time.strftime('%Y%m%d_%H%M%S')}.png")
        assert False, f"行動版截圖失敗：{e}"
    finally:
        if mobile_driver:
            mobile_driver.quit()