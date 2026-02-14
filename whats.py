from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time


# ---------------- SETTINGS ----------------
FILE_PATH = "Make Your Phone Numbers CSV File"
MESSAGE = "Type Message To Send "
FILE_TO_SEND = r"Give File Path To Send File "

# ---------------- READ CSV ----------------
df = pd.read_csv(FILE_PATH)
numbers = df["phone"].astype(str).tolist()

# ---------------- DRIVER ----------------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 120)
driver.get("https://web.whatsapp.com")

print("📱 Scan QR Code...")
wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Chat list']")))
print("✅ Logged In")

# ---------------- FUNCTION ----------------
def send_message_and_video(phone):
    try:
        # -------- NEW CHAT --------
        wait.until(EC.element_to_be_clickable((
            By.XPATH, "//span[@data-icon='new-chat-outline']"
        ))).click()
        time.sleep(2)

        # -------- SEARCH NUMBER --------
        search_box = wait.until(EC.presence_of_element_located((
            By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"
        )))
        search_box.clear()
        search_box.send_keys(phone)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)
        time.sleep(4)

        # -------- SEND TEXT MESSAGE --------
        msg_box = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "/html/body/div[1]/div/div/div/div/div[3]/div/div[5]/div/footer/div[1]/div/span/div/div/div/div[3]/div[1]/p"
        )))
        msg_box.send_keys(MESSAGE)
        msg_box.send_keys(Keys.ENTER)
        time.sleep(2)

        # -------- CLICK ATTACH BUTTON --------
        attach_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "/html/body/div[1]/div/div/div/div/div[3]/div/div[5]/div/footer/div[1]/div/span/div/div/div/div[1]/div/span/button/div/div/div[1]/span"
        )))
        attach_btn.click()
        time.sleep(2)

        # -------- SELECT FILE --------
        file_input = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@type='file']"
        )))
        file_input.send_keys(FILE_TO_SEND)

        

        send_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//*[@id='app']/div/div/div[3]/div/div[3]/div[2]/div/span/div/div/div/div[2]/div/div[2]/div[2]/span/div/div"
        )))
        send_btn.click()

        # -------- OPTIONAL: FOCUS MESSAGE FIELD --------
        final_msg_box = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "/html/body/div[1]/div/div/div/div/div[3]/div/div[5]/div/footer/div[1]/div/span/div/div/div/div[3]/div[1]/p"
        )))
        final_msg_box.send_keys("")  # keeps flow stable

        print(f"✅ Video sent to {phone}")
        time.sleep(10)

    except Exception as e:
        print(f"❌ Failed for {phone} | {e}")

# ---------------- LOOP ----------------
for num in numbers:
    send_message_and_video(num)

print("🎉 All videos sent successfully")


