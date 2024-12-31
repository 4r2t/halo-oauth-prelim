from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def automate_xsts_oauth_login(client_id, username, password):
    redirect_uri = "http://localhost"
    scope = "XboxLive.signin XboxLive.offline_access"
    oauth_url = f"https://login.live.com/oauth20_authorize.srf?client_id={client_id}&response_type=code&approval_prompt=auto&scope={scope}&redirect_uri={redirect_uri}"

    # Set up Selenium WebDriver in headless mode
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver: WebDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the OAuth URL in headless browser
    driver.get(oauth_url)

    wait = WebDriverWait(driver, 30)  # Set up an explicit wait of up to 10 seconds

    # Wait for the email/username field and enter the username
    email_field = wait.until(EC.presence_of_element_located((By.ID, "i0116")))
    email_field.send_keys(username)
    driver.find_element(By.ID, "idSIButton9").click()  # Click "Next"
    
    # Wait for the password field and enter the password
    password_field = wait.until(EC.presence_of_element_located((By.ID, "i0118")))
    password_field.send_keys(password)
    driver.find_element(By.ID, "idSIButton9").click()  # Click "Sign in"
    
    try:
        print("Waiting for 'Stay signed in?' prompt...")
        stay_signed_in_button = wait.until(EC.element_to_be_clickable((By.ID, "acceptButton")))
        stay_signed_in_button.click()
        print("Clicked 'Stay signed in?' button.")
    except Exception as e:
        print(f"Error: 'Stay signed in?' button not found: {str(e)}")
            
    # Wait for the redirect to finish
    wait.until(lambda d: "code=" in d.current_url)

    # Capture the authorization code from the URL
    current_url = driver.current_url
    print(f"Redirected URL: {current_url}")

    if "code=" in current_url:
        xsts_auth_code = current_url.split("code=")[1].split("&")[0]
        print(f"Authorization Code: {xsts_auth_code}")

    # Close the browser
    driver.quit()

    return xsts_auth_code
