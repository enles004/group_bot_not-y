import osssss
import pickle

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from .exceptions import *
from .imagehelper import *


class Pinterest():
    def __init__(self, login, pw):
        self.domains = [".pinterest.com", ".www.pinterest.com", "www.pinterest.com", ".www.pinterest.co.kr",
                        "www.pinterest.co.kr"]
        self.piclist = []
        self.currentdir = os.getcwd()
        self.user_agent = ""
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=options)
        self.user_agent = self.driver.execute_script("return navigator.userAgent;")
        if os.path.exists("cookies.pkl"):
            print("Loading cookies...")
            self.driver.get("https://pinterest.com")
            self.driver.implicitly_wait(3)
            sleep(2)
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                # print(cookie)
                for domain in self.domains:
                    try:
                        self.driver.add_cookie({
                            "domain": domain,
                            "name": cookie["name"],
                            "value": cookie["value"],
                            "path": '/'
                            # "expiry": None
                        })
                    except:
                        pass
            self.driver.get("https://pinterest.com")
            self.driver.implicitly_wait(3)
            try:
                self.driver.find_element(By.XPATH, '//*[@id="HeaderContent"]')
                return
            except:
                print("Failed to login from cookies.. login manually")
                # input()
                # pass
        try:
            self.driver.get("https://pinterest.com/login")
            self.driver.implicitly_wait(3)
            for i in range(3):
                try:
                    self.driver.find_element(By.ID, "email")
                    break
                except:
                    sleep(1)
            emailelem = self.driver.find_element(By.ID, "email")
            passelem = self.driver.find_element(By.ID, "password")
            emailelem.send_keys(login)
            passelem.send_keys(pw)
            sleep(1)
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        except Exception as e:
            raise e

        while True:
            try:
                self.driver.find_element(By.XPATH, '//*[@id="HeaderContent"]')
                break
            except:
                sleep(1)
                try:
                    self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
                except:
                    pass
        self.dump()
        return

    def dump(self):
        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open("cookies.pkl", "wb"))

    def crawl(self, dir):
        timeout = 0
        height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            now_height = self.driver.execute_script("return document.body.scrollHeight")

            # If height changed
            if now_height != height:
                self.download_image(dir)
                break
            else:
                timeout += 1
                if timeout >= 5:
                    print("It seems we find the end of current page, stop crawling.")
                    raise EndPageException
        sleep(2)
        return

    def single_download(self, n=-1, url="https://pinterest.com/", dir="./download"):
        global loop
        fail_image = 0
        if n == -1:
            n = 999999999
        loop = asyncio.get_event_loop()

        # Create directory
        if dir[0] == "/":
            dir = dir[1:]
        directory = os.path.join(self.currentdir, dir)
        if not os.path.exists(directory):
            os.mkdir(directory)

        self.driver.get(url)
        self.driver.implicitly_wait(3)
        for i in range(n):
            try:
                self.crawl(dir)
            except EndPageException as e:
                break
            download_pic_count = len(self.piclist)
            print(f"Scroll down {i} Page, downloaded {download_pic_count} images.")
        download_pic_count = len(self.piclist)
        print(f"Totally downloaded {download_pic_count} images.")
        loop.close()
        return fail_image

    def download_image(self, dir="./download"):
        page_pic_list = []
        req = self.driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        pics = soup.find_all("img")
        if pics is None:
            return 0
        for pic in pics:
            src = pic.get("src")

            # Profile image, skip
            if "75x75_RS" in src:
                continue

            if src not in self.piclist:
                self.piclist.append(src)
                page_pic_list.append(src)

        fail_image = sum(loop.run_until_complete(download_image_host(page_pic_list, dir)))
        return fail_image

    def getdriver(self):
        return self.driver
