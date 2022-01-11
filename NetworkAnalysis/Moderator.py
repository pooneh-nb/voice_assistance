import asyncio

import NetworkAnalysis.Traffic_Capturer as Traffic
import NetworkAnalysis.SkillHandler as Installer
import NetworkAnalysis.Skill_Interactor as Interactor
import NetworkAnalysis.utilities as utilities

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
import time


class Moderator:
    def __init__(self, firefox_exe_path, gecko_path, data_dir, signin_page, profile, email, pasw, num_skills, persona):
        # driver/extensions path
        self.FIREFOX_EXE_PATH = firefox_exe_path
        self.GECKO_PATH = gecko_path
        self.DATA_DIR = data_dir
        self.EXTENSION_PATH = os.path.join(self.DATA_DIR, 'browser-extension.zip')

        # Persona name
        self.PERSONA = persona

        # list of skills
        SKILLS_ADDR = os.path.join(self.DATA_DIR, 'data/subgrouped_skills.json')
        self.all_skills = utilities.read_json(SKILLS_ADDR)[self.PERSONA]
        self.no_skills_to_install = num_skills

        # skill with no reviews  -- start page
        self.SIGNIN_PAGE = signin_page

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
    
    def main(self):
        driver = self.get_webdriver()
        print('WebDriver registered')

        # SIGNING IN
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
                traffic = Traffic.TrafficCapturer(skill)
                try:
                    eventloop = asyncio.get_event_loop()
                    eventloop.run_until_complete(traffic.dispatch_capture())
                except KeyboardInterrupt as e:
                    print("-- Exiting due to keyboard interrupt --")


                # %%% INSTALL
                installer = Installer.Skill_Handler(driver, skill_url, skill_perm)
                install_status = installer.install_skill()

                # Log successfully and partially installed skills
                if install_status[0]:
                    total_installed += 1

                if total_installed >= self.no_skills_to_install:
                    break

                # %%% INTERACT
                interaction = Interactor.Skill_Interaction(self.DATA_DIR, self.PERSONA, skill)
                interaction.skill_interactor()

                # %%% UNINSTALL
                uninstall_status = installer.uninstall_skill()

                # Log successfully and partially uninstalled skills
                if uninstall_status[0]:
                    total_uninstalled += 1

                if total_uninstalled >= self.no_skills_to_install:
                    break
                # %%% STOP TCPDUMP

                #traffic.kill_process()

        else:
            print('Could not sign in. Stopping the process')
            self.quit_driver(driver)

        self.quit_driver(driver)
        print(total_installed, len(self.all_skills))
        print('Installed %f skills.', (total_installed / self.no_skills_to_install) * 100.0)


if __name__ == '__main__':

    # initialization
    firefox_exe_path = '/usr/bin/firefox-trunk'
    gecko_path = '/home/c2/alexa/source/voice-assistant-central/geckodriver'
    data_dir = '/home/c2/alexa/source/voice-assistant-central/'

    signin_page = 'https://www.amazon.com/Sarim-Studios-CurrentBitcoin/dp/B01N9SS2LI/ref=sr_1_3641'
    profile = "/home/c2/.mozilla/firefox-trunk/qjr4taro.alexa"
    email = "alex.nik.echo@gmail.com"
    pasw = "change.me"
    num_skills = 2
    persona = 'Dating'

    moderator_obj = Moderator(firefox_exe_path, gecko_path, data_dir, signin_page, profile, email, pasw, num_skills, persona)
    moderator_obj.main()


