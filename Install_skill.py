from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import utilities
import os
import skill_interaction

from subprocess import Popen, PIPE
import subprocess


class AlexaNetworkTraffic:
    def __init__(self, firefox_exe_path, gecko_path, data_dir, persona, signin_page, email, pasw, profile, num_skills):
        # driver/extensions path
        self.FIREFOX_EXE_PATH = firefox_exe_path
        self.GECKO_PATH = gecko_path
        self.DATA_DIR = data_dir
        self.EXTENSION_PATH = os.path.join(self.DATA_DIR, 'browser-extension.zip')

        # Persona name
        self.PERSONA = persona

        # skill with no reviews  -- start page
        self.SIGNIN_PAGE = signin_page

        # list of skills
        SKILLS_ADDR = os.path.join(self.DATA_DIR, 'data/subgrouped_skills.json')
        self.all_skills = utilities.read_json(SKILLS_ADDR)[self.PERSONA]
        self.no_skills_to_install = num_skills

        # credentials
        self.Email = email
        self.Password = pasw
        self.Profile = profile

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

            signin_button = driver.find_element_by_id('a-autoid-0-announce')
            signin_button.click()
            time.sleep(3)

            try:
                email_input = driver.find_element_by_id('ap_email')

            except Exception:
                # Assume that the user is already signed in
                print('Already signed in. Returning.')
                return True

            email_input.send_keys(self.Email)
            time.sleep(3)

            continue_button = driver.find_element_by_id('continue')
            continue_button.click()
            time.sleep(3)

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

    def install_skill(self, driver, url, perm=False):
        try:
            driver.get(url)
            time.sleep(3)

            skill_enable_button = driver.find_element_by_id("a2s-skill-enable-button")
            skill_enable_button.click()
            time.sleep(3)

            if perm:
                try:
                    permission_button = driver.find_element_by_xpath(
                        "//input[@type='submit'][@class='a-button-input'][not(@aria-labelledby)]")
                    permission_button.click()
                    time.sleep(3)

                except Exception:
                    print('Something went wrong when enabling permissions')
                    return False, 'perm'

        except BaseException as ex:
            print('Something went wrong when installing: ', str(ex))
            return False, 'sim'

        return True, 'sim'

    def uninstall_skill(self, driver, url, perm=False):
        try:
            driver.get(url)
            time.sleep(3)

            skill_disable_button = driver.find_element_by_id("a2s-skill-disable-button")
            skill_disable_button.click()
            time.sleep(3)

            pop_up = driver.find_element_by_id("a-popover-1")
            pop_up_skill_disable_button = pop_up.find_element_by_xpath("//span[contains(@data-a2s_skill_action, 'disable')]")
            pop_up_skill_disable_button.click()
            time.sleep()
            """if perm:
                try:
                    permission_button = driver.find_element_by_xpath(
                        "//input[@type='submit'][@class='a-button-input'][not(@aria-labelledby)]")
                    permission_button.click()
                    time.sleep(3)

                except Exception:
                    print('Something went wrong when enabling permissions')
                    return False, 'perm'"""

        except BaseException as ex:
            print('Something went wrong in Uninstall: ', str(ex))
            return False, 'sim'

        return True, 'sim'

    def train_persona(self):

        driver = self.get_webdriver()
        print('WebDriver registered')

        signin_status = self.signin(driver)

        total_installed = 0
        total_uninstalled = 0
        if signin_status:
            print('Signed in.')
            for skill in self.all_skills:
                print(self.all_skills[skill]["Name"])

                skill_perm = self.all_skills[skill]['Skill_permission']
                skill_url = self.all_skills[skill]['Skill_link']

                if len(skill_perm) > 0:
                    skill_perm = True
                else:
                    skill_perm = False

                # %%% START TCPDUMP
                print("START TCPDUMP")
                sudo_password = '1234'
                file_id = skill+'.pcap'
                command = 'tcpdump -i wlo1 src 10.42.0.11 -w '+file_id
                command = command.split()
                p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
                sudo_prompt = p.communicate(sudo_password + '\n')[1]


                # %%% INSTALL
                print("INSTALL")
                install_status = self.install_skill(driver, skill_url, skill_perm)

                # Log succesfully and partially installed skills
                if install_status[0]:
                    total_installed += 1

                if total_installed >= self.no_skills_to_install:
                    break

                # %%% INTERACT
                interaction = skill_interaction.SkillInteraction(self.DATA_DIR, self.PERSONA)
                skills_utterances = interaction.get_utterances(skill)
                interaction.play_utterances(skills_utterances)

                # %%% UNINSTALL
                print("Uninstall")
                uninstall_status = self.uninstall_skill(driver, skill_url, skill_perm)

                # Log successfully and partially uninstalled skills
                if uninstall_status[0]:
                    total_uninstalled += 1

                if total_uninstalled >= self.no_skills_to_install:
                    break
                # %%% STOP TCPDUMP
                p.send_signal(subprocess.signal.SIGTERM)

        else:
            print('Could not sign in. Stopping the process')
            self.quit_driver(driver)

        self.quit_driver(driver)
        print(total_installed, len(self.all_skills))
        print('Installed %f skills.', (total_installed / self.no_skills_to_install) * 100.0)


firefox_exe_path = '/usr/bin/firefox-trunk'
gecko_path = '/home/c2/alexa/source/voice-assistant-central/geckodriver'
data_dir = '/home/c2/alexa/source/voice-assistant-central/'
persona = 'Dating'
signin_page = 'https://www.amazon.com/Sarim-Studios-CurrentBitcoin/dp/B01N9SS2LI/ref=sr_1_3641'
email = "alex.nik.echo@gmail.com"
pasw = "change.me"
profile = "/home/c2/.mozilla/firefox-trunk/qjr4taro.alexa"
num_skills = 2

Alex = AlexaNetworkTraffic(firefox_exe_path, gecko_path, data_dir, persona, signin_page, email, pasw, profile, num_skills)
Alex.train_persona()

