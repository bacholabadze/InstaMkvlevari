import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()  # need chrome driver to execute
driver.maximize_window()


class InstaMkvlevari:
    def __init__(self):
        self.username = "ENTER YOUR USERNAME HERE"
        self.password = "ENTER YOUR PASSWORD HERE"
        self.mutual = []
        self.they_dont_follow = []
        self.i_dont_follow = []
        self.followers = ['1', '2', '3', '4']
        self.followings = ['1', '2']
        self.hunt = ""

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

    def start_analyze(self):
        self.find_mutual()
        self.find_they_dont_follow()
        self.find_i_dont_follow()

    def save_data_log(self):
        now = datetime.datetime.now()
        now = str(now).split(" ")
        now[1] = now[1][:8]
        # print(f"{now} - now")

        file_name = f"{self.username}_{self.hunt}_{now[1]}_{now[0]}"
        file_name = file_name.replace(":", "-")

        print(f"{file_name}.txt")

        with open(f"{file_name}.txt", "w") as file:
            file.write("followers\n")
            for f in self.followers:
                if "Verified" in f:
                    f = f.replace("\nVerified", "")
                file.write(f"{f}, ")

            file.write("\nfollowing\n")
            for f in self.followings:
                if "Verified" in f:
                    f = f.replace("\nVerified", "")
                file.write(f"{f}, ")

    def __str__(self):

        print(f"Mutual".center(35, '-'))
        for ix, f in enumerate(self.mutual):
            print(f"{ix}) {f}")

        print(f"Who doesn't follow back".center(35, '-'))
        for ix, f in enumerate(self.they_dont_follow):
            print(f"{ix}) {f}")

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

        username.send_keys(f"{self.username}")
        password.send_keys(f"{self.password}")

        enter = driver.find_element(By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button/div")
        enter.click()

        if self.hunt == "":
            profile_pic = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[1]/span/img"))).click()
            profile_view = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div/div[2]/div[1]/a/div/div[2]/div/div/div"))).click()
        else:
            search_bar = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[2]/input")
            search_bar.send_keys(self.hunt)

            first_result = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/div/a/div")
            first_result.click()
        driver.implicitly_wait(5)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Followings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        followings_quantity = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a/div/span").text
        print(followings_quantity)

        # click followings button
        followings = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a/div"))).click()

        driver.implicitly_wait(10)

        # followings list
        scroll_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")

        driver.implicitly_wait(5)

        # scroll till end of followings list
        quit_loop_index = 0
        last_follower_name = ""
        new_follower_name = ""
        while True:
            quit_loop_index += 1
            print(quit_loop_index)
            print(quit_loop_index)
            last_follower_name = new_follower_name

            ht = driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight; """, scroll_box)
            driver.implicitly_wait(3)
            links = scroll_box.find_elements(By.TAG_NAME, 'a')
            following_names = [name.text for name in links if name.text != '']
            print(f"{len(following_names)/int(followings_quantity)*100}% [{len(following_names)}/{followings_quantity}]".center(35, "~"))
            print(following_names[len(following_names)-1])

            new_follower_name = following_names[len(following_names)-1]
            if new_follower_name != last_follower_name:
                quit_loop_index = 0
            # End Logic
            if len(following_names) == int(followings_quantity) or quit_loop_index > 5:
                break
        print(following_names)
        for f in following_names:
            if f == "Verified":
                following_names.remove(f)

        self.followings = following_names

        exit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button"))).click()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Followers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        followers_quantity = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a/div/span").text
        print(followings_quantity)
        followers = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a/div"))).click()

        driver.implicitly_wait(10)
        scroll_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")

        driver.implicitly_wait(5)

        quit_loop_index = 0
        last_follower_name = ""
        new_follower_name = ""
        while True:
            quit_loop_index += 1
            print(quit_loop_index)
            last_follower_name = new_follower_name

            ht = driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight; """, scroll_box)
            driver.implicitly_wait(3)
            links = scroll_box.find_elements(By.TAG_NAME, 'a')
            follower_names = [name.text for name in links if name.text != '']
            print(f"{len(follower_names)/int(followers_quantity)*100}% [{len(follower_names)}/{followers_quantity}]".center(35, "~"))
            print(follower_names)
            print(len(follower_names))
            new_follower_name = str(follower_names[len(follower_names)-1])

            if new_follower_name != last_follower_name:
                quit_loop_index = 0

            # End Logic
            if len(follower_names) == int(followers_quantity) or quit_loop_index > 5:
                break

        print(follower_names)
        for f in follower_names:
            if f == "Verified":
                following_names.remove(f)
        self.followers = follower_names


try:
    my_acc = InstaMkvlevari()
    my_acc.get_data_from_insta()
    my_acc.start_analyze()
    print(my_acc)
    my_acc.save_data_log()
    print("data_log")
except:
    print("iaghlishi")
finally:
    driver.quit()


