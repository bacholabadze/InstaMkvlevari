# import sys
# sys.path.append('F:/Optimo/dashboard')
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()  # need chrome driver to execute
driver.maximize_window()


class InstaMkvlevari:
    def __init__(self):
        self.mutual = []
        self.they_dont_follow = []
        self.i_dont_follow = []
        self.followers = ['1', '2', '3', '4']
        self.followings = ['1', '2']

    def find_mutual(self):
        for f in self.followings:
            if f in self.followers:
                self.mutual.append(f)

    def find_they_dont_follow(self):
        for f in self.followings:
            if f not in self.followers:
                self.they_dont_follow.append(f)

    def find_i_dont_follow(self):
        for f in self.followers:
            if f not in self.followings:
                self.i_dont_follow.append(f)

    def __str__(self):
        self.find_mutual()
        print(f"Mutual".center(35, '-'))
        for ix, f in enumerate(self.mutual):
            print(f"{ix}) {f}")

        self.find_they_dont_follow()
        print(f"Who doesn't follow back".center(35, '-'))
        for ix, f in enumerate(self.they_dont_follow):
            print(f"{ix}) {f}")

        self.find_i_dont_follow()
        print(f"Who I don't follow back".center(35, '-'))
        for ix, f in enumerate(self.i_dont_follow):
            print(f"{ix}) {f}")

        return "END".center(35, '-')

    def get_data_from_insta(self):

        driver.get("https://instagram.com")
        # ans = input("Enter Credentials on the page and click Enter to confirm authentication: _")
        driver.implicitly_wait(10)
        username = driver.find_element(By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input")
        password = driver.find_element(By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input")

        username.send_keys("USERNAME")
        password.send_keys("PASSWORD")

        enter = driver.find_element(By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button/div")
        enter.click()

        profile_pic = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[1]/span/img"))).click()
        profile_view = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div/div[2]/div[1]/a/div/div[2]/div/div/div"))).click()

        driver.implicitly_wait(5)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Followings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        followings_quantity = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a/div/span").text
        print(followings_quantity)
        followings = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a/div"))).click()

        driver.implicitly_wait(10)
        scroll_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")

        driver.implicitly_wait(5)
        while True:
            ht = driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight; """, scroll_box)
            driver.implicitly_wait(3)
            links = scroll_box.find_elements(By.TAG_NAME, 'a')
            following_names = [name.text for name in links if name.text != '']
            print(f"{len(following_names)/int(followings_quantity)*100}%".center(35, "~"))
            if len(following_names) == int(followings_quantity):
                break
        print(following_names)
        self.followings = following_names

        exit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button"))).click()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Followers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        followers_quantity = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a/div/span").text
        print(followings_quantity)
        followers = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a/div"))).click()

        driver.implicitly_wait(10)
        scroll_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")

        driver.implicitly_wait(5)
        while True:
            ht = driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight; """, scroll_box)
            driver.implicitly_wait(3)
            links = scroll_box.find_elements(By.TAG_NAME, 'a')
            follower_names = [name.text for name in links if name.text != '']
            print(f"{len(follower_names)/int(followers_quantity)*100}%".center(35, "~"))
            if len(follower_names) == int(followers_quantity):
                break
        print(follower_names)
        self.followers = follower_names


my_acc = InstaMkvlevari()
my_acc.get_data_from_insta()
print(my_acc)
