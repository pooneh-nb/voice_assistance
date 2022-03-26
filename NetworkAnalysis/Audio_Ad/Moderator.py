import threading

from NetworkAnalysis.Traffic_capturing import Traffic_Capturer as Traffic
from NetworkAnalysis.Traffic_capturing import SkillHandler as Installer


from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By


from gtts import gTTS
import utilities
import os
import time
from NetworkAnalysis.Audio_Ad import audio_recorder as Recorder
from playsound import playsound


class Moderator:
    def __init__(self, firefox_exe_path, gecko_path, data_dir, signin_page, profile, email, pasw, persona,
                 output_traffic_dir, output_audio_dir):
        # driver/extensions path
        self.FIREFOX_EXE_PATH = firefox_exe_path
        self.GECKO_PATH = gecko_path
        self.DATA_DIR = data_dir
        self.EXTENSION_PATH = os.path.join(self.DATA_DIR, 'tools/browser-extension.zip')

        # Persona name
        self.PERSONA = persona

        # list of skills
        SKILLS_ADDR = os.path.join(self.DATA_DIR, 'skills_data/music_skills.json')
        self.all_skills = utilities.read_json(SKILLS_ADDR)

        # skill with no reviews  -- start page
        self.SIGNIN_PAGE = signin_page

        # credentials
        self.Email = email
        self.Password = pasw
        self.Profile = profile

        # output directory
        self.output_traffic_dir = output_traffic_dir
        self.output_audio_dir = output_audio_dir

    def get_webdriver(self):
        options = FirefoxOptions()
        options.add_argument('-profile')
        options.add_argument(self.Profile)

        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True

        firefox_profile = webdriver.FirefoxProfile()
        firefox_bin = FirefoxBinary(firefox_path=self.FIREFOX_EXE_PATH)
        driver = webdriver.Firefox(firefox_binary=firefox_bin,
                                   capabilities=firefox_capabilities,
                                   options=options,
                                   executable_path=self.GECKO_PATH,
                                   service_args=["--marionette-port", "2828"])

        driver.install_addon(self.EXTENSION_PATH, temporary=True)

        return driver

    def quit_driver(self, driver):
        try:
            driver.quit()
        except BaseException as ex:
            print('Something went wrong: ', str(ex))

    def signin(self, driver):
        try:
            driver.get(self.SIGNIN_PAGE)
            time.sleep(3)

            # signin_button = driver.find_element_by_id('a-autoid-0-announce')
            # signin_button.click()
            # time.sleep(3)

            try:
                signin_pop_up_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Sign In')]")
                signin_pop_up_button.click()
                time.sleep(3)
                email_input = driver.find_element_by_id('ap_email')

            except Exception as ex:
                # Assume that the user is already signed in
                print('Already signed in. Returning.')
                return True

            email_input.send_keys(self.Email)
            time.sleep(3)

            # continue_button = driver.find_element_by_id('continue')
            # continue_button.click()
            # time.sleep(3)

            password_input = driver.find_element_by_id('ap_password')
            password_input.send_keys(self.Password)
            time.sleep(3)

            signin_button = driver.find_element_by_id('signInSubmit')
            signin_button.click()
            time.sleep(3)

        except BaseException as ex:
            print('Something went wrong: ', str(ex))
            return False

        return True

    def main(self):
        driver = self.get_webdriver()
        print('WebDriver registered')
        # SIGNING IN
        signin_status = self.signin(driver)
        #signin_status =True

        if signin_status:
            print('Signed in.')
            for music_name, link in self.all_skills.items():
                # %%% START TCPDUMP
                traffic = Traffic.TrafficCapturer(music_name, self.PERSONA, self.output_traffic_dir)
                t = threading.Thread(target=traffic.capture_process(), daemon=True)
                t.start()

                # %%% INSTALL
                installer = Installer.Skill_Handler(driver, link, "")
                install_status = installer.install_skill()
                # Spotify


                # %%% INTERACT
                utterance = "Alexa, play top hits on" + music_name
                utterance_wav = gTTS(text=utterance, lang='en', slow=False)
                utterance_wav.save(os.path.join(self.DATA_DIR, "sound", 'current-utterance' + '.wav'))
                file_name = os.path.join(self.DATA_DIR, "sound", 'current-utterance' + '.wav')
                print(file_name)
                playsound(file_name)

                # Record
                f_name_directory = os.path.join(self.output_audio_dir, music_name)
                if not os.path.exists(f_name_directory):
                    os.mkdir(f_name_directory)
                raw_string = r"{}".format(f_name_directory)
                record = Recorder.Recorder(raw_string)
                record.listen()

                # wait
                time.sleep(3)

                utterance = "Alexa, Stop"
                utterance_wav = gTTS(text=utterance, lang='en', slow=False)
                utterance_wav.save(os.path.join(self.DATA_DIR, "sound", 'current-utterance' + '.wav'))
                file_name = os.path.join(self.DATA_DIR, "sound", 'current-utterance' + '.wav')
                print(file_name)
                playsound(file_name)

               # UNINSTALL
                uninstall_status = installer.uninstall_skill()

                # STOP TCPDUMP
                print("tcpdump is terminated \n")
                t.join(timeout=1)
                traffic.terminate_process()

        else:
            print('Could not sign in. Stopping the process')
            self.quit_driver(driver)

        self.quit_driver(driver)


if __name__ == '__main__':

    data_dir = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data"
    music_skills = os.path.join(data_dir, "skills_data/music_skills.json")
    selected_categories = ["Fashion-Style", "ConnectedCar", "Plain"]
    for persona in selected_categories:
        output_traffic_dir = os.path.join(data_dir, "Audio_ads_test", "Traffic", persona)
        if not os.path.exists(output_traffic_dir):
            os.makedirs(output_traffic_dir)
        output_audio_dir = os.path.join(data_dir, "Audio_ads_test", "Audio_Records", persona)
        if not os.path.exists(output_audio_dir):
            os.makedirs(output_audio_dir)

        # initialization
        firefox_exe_path = '/usr/bin/firefox-trunk'
        gecko_path = os.path.join(data_dir, 'tools/geckodriver')
        signin_page = 'https://www.amazon.com/Sarim-Studios-CurrentBitcoin/dp/B01N9SS2LI/ref=sr_1_3641'
        profile = "/home/c2/.cache/mozilla/firefox-trunk/zptiqr5g.echo-profile"
        email = "hari.echodot@gmail.com"
        pasw = "change.me"
        #num_skills = 50
        moderator_obj = Moderator(firefox_exe_path, gecko_path, data_dir, signin_page, profile, email, pasw,
                                  persona, output_traffic_dir, output_audio_dir)
        moderator_obj.main()
