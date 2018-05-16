from speech import Speech
from selenium import webdriver

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

class Recaptcha():
    """
        This class solves the Google's reCAPTCHA by receiving the <iframe> located on a page.
    """

    def __init__(self):
        pass

    def solve_recaptcha(self, driver):
        driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
        # time.sleep(4)

        # click on the "i'm not a robot checkbox"
        checkbox = driver.find_element_by_class_name("recaptcha-checkbox-checkmark")
        checkbox.click()
        print("Clicked on the checkbox. Verifying captcha.")
        time.sleep(3)

        is_checked = driver.find_element_by_id("recaptcha-anchor").get_attribute("aria-checked")
        print("reCAPTCHA was clicked. Validated? {}".format(is_checked))
        if is_checked == "false":
            driver.switch_to_default_content()
            frames = driver.find_elements_by_tag_name("iframe")
            driver.switch_to_frame(frames[-1]) # select the last frame, that's the image frame

            print("Diving into the image frame.")
            time.sleep(2)
            audio_button = driver.find_element_by_id("recaptcha-audio-button")
            audio_button.click()
            print("Clicked on the audio button.")

            time.sleep(3)
            audio_download_link = driver.find_element_by_class_name("rc-audiochallenge-tdownload-link").get_attribute('href')
            speech = Speech()
            audio_result = speech.speech_to_text(audio_download_link)

            audio_result_input = driver.find_element_by_id("audio-response")
            audio_result_input.send_keys(audio_result)
            time.sleep(3)

            verify_button = driver.find_element_by_id("recaptcha-verify-button")
            verify_button.click()

            while not EC.invisibility_of_element_located((By.CLASS_NAME, "rc-audiochallenge-error-message")):
                audio_download_link = driver.find_element_by_class_name("rc-audiochallenge-tdownload-link").get_attribute('href')
                speech = Speech()
                audio_result = speech.speech_to_text(audio_download_link)

                audio_result_input = driver.find_element_by_id("audio-response")
                audio_result_input.send_keys(audio_result)
                time.sleep(3)

                verify_button = driver.find_element_by_id("recaptcha-verify-button")
                verify_button.click()

            time.sleep(2)

        driver.switch_to_default_content()
        return driver
