import time
from selenium.webdriver.common.by import By

class Skill_Handler:
    def __init__(self, driver, url, perm):
        self.DRIVER = driver
        self.URL = url
        self.PERM = perm

    def install_skill(self):
        print("INSTALL")
        try:
            self.DRIVER.get(self.URL)
            time.sleep(3)

            # skill_enable_button = self.DRIVER.find_element_by_id("a2s-skill-enable-button")
            skill_enable = self.DRIVER.find_element(By.XPATH, "//button[contains(text(), 'Enable')]")
            skill_enable.click()
            # skill_enable_button.click()
            time.sleep(3)

            if self.PERM:
                try:
                    permission_button = self.DRIVER.find_element_by_xpath(
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

    def uninstall_skill(self):
        print("Uninstall")
        try:
            self.DRIVER.get(self.URL)
            time.sleep(3)

            skill_disable_button = self.DRIVER.find_element(By.XPATH, "//button[contains(text(), 'Disable Skill')]")
            skill_disable_button.click()
            time.sleep(3)

            pop_up = self.DRIVER.find_element(By.CLASS_NAME, "sc-iWRGeL")
            pop_up_skill_disable_button = pop_up.find_element(By.XPATH, "//button[contains(text(), 'Disable Skill')]")
            pop_up_skill_disable_button.click()
            time.sleep(3)

            # skill_disable_button = self.DRIVER.find_element_by_id("a2s-skill-disable-button")
            # skill_disable_button.click()
            # time.sleep(3)
            #
            # pop_up = self.DRIVER.find_element_by_id("a-popover-1")
            # pop_up_skill_disable_button = pop_up.find_element_by_xpath(
            #     "//span[contains(@data-a2s_skill_action, 'disable')]")
            # pop_up_skill_disable_button.click()
            # time.sleep(3)
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
