from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import os

class autoInsta:
    
    def __init__(self, path):
        
        with open(path, "r") as f:
            settings = f.readlines()
            settings = [setting.split("= ")[1].replace("\n", "") for setting in settings]
            
        self.username = str(settings[0])
        self.password = str(settings[1])
        self.maxwait = int(settings[2])
        self.restperiod = int(settings[3])
        self.restchance = int(settings[4])
        self.unfollowchance = int(settings[5])
        self.unfollowamount = int(settings[6])
        self.stalkchance = int(settings[7])
        self.stalkamount = int(settings[8])
        self.followchance = int(settings[9])
        self.hashtags = settings[10].split(", ")
        self.runamount = int(settings[11])


    def wait(self):
        self.driver.implicitly_wait(10)
        time.sleep(random.randint(0, self.maxwait))

    def login(self):

        userAgent = "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36"
        profile = webdriver.FirefoxProfile() #starts webbrowser emulating as a phone
        profile.set_preference("general.useragent.override", userAgent)
        self.driver = webdriver.Firefox(profile)
        self.driver.set_window_size(540,960)

        self.driver.get("https://www.instagram.com/accounts/login/")
        self.wait()
        
        usernameInput = self.driver.find_element_by_xpath(
            "//input[@name='username']")
        usernameInput.send_keys(self.username)
        self.wait()
        
        passwordInput = self.driver.find_element_by_xpath(
            "//input[@name='password']")
        passwordInput.send_keys(self.password)
        self.wait()
        
        loginButton = self.driver.find_element_by_xpath(
            "//button[@type='submit']")
        loginButton.click()
        self.wait()

    def popup(self):
        try:
            notNow = self.driver.find_element_by_xpath(
                "//button[contains(text(),'Not Now')]")
            notNow.click()
            self.wait()
        except Exception as e:
            print(e)

    def search(self, term):
        self.wait()
        button = self.driver.find_element_by_xpath(
            "//a[@href='/explore/']")
        button.click()
        self.wait()
        self.wait()

        bar = self.driver.find_element_by_xpath(
            "//input[@type='search']")
        bar.send_keys(term)
        self.wait()
        bar.send_keys(Keys.RETURN)
        self.wait()
        
        links = self.driver.find_elements_by_xpath('//a[@href]')
        link = links[random.randint(0,1)].find_element_by_xpath('.//*')
        link.click()

    def explore(self, cycles):
        run = True
        while cycles > 0:
            self.wait()
            for i in range(1, random.randint(4, 8)):
                height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("window.scrollTo(0," + str(height-random.randint(400, 1000)) + ")")
                self.wait()
            try:
                hrefs = self.driver.find_elements_by_tag_name("a")
                hrefs = [elem.get_attribute("href") for elem in hrefs]
                href = hrefs[len(hrefs)-random.randint(7, 20)]
                self.driver.get(href)
                self.wait()
                self.driver.find_element_by_xpath("//*[@aria-label='Like']").click()
                print("Liked")
                cycles -= 1
            except Exception as e:
                print(e)
                print("Explore error")
            self.wait()
            if random.randint(1, 100) <= self.followchance:
                try:
                    self.driver.find_element_by_xpath("//button[@type='button']").click()
                    print("Followed")
                    self.wait()
                    name = self.driver.find_elements_by_xpath("//a")
                except Exception as e:
                    print(e)
                    print("Follow button not found")
            self.driver.back()

    def unfollow(self, cycles):
        self.wait()
        self.driver.find_elements_by_xpath("//span[@role='link']")[-1].click()
        self.wait()
        self.driver.find_elements_by_xpath("//li")[2].click()
        height = 1500
        while cycles > 0:
            self.wait()
            followed = self.driver.find_elements_by_xpath("//button[@type='button']")
            self.driver.execute_script("window.scrollTo(0," + str(height) + ")")
            try:
                self.wait()
                followed[random.randint(int(1+(height/50)), int(5+(height/50)))].click()
                self.wait()
                self.driver.find_element_by_xpath("//button[text()='Unfollow']").click()
                print("Unfollowed")
                cycles -= 1
            except Exception as e:
                print(e)
                print("Unfollow button not found")
            height += random.randint(50, 100)
        self.wait()

    def likeProfile(self, cycles):
        self.wait()
        self.driver.find_elements_by_xpath("//span[@role='link']")[-1].click()
        self.wait()
        self.driver.find_elements_by_xpath("//li")[2].click()
        height = random.randint(1, 2000)
        while cycles > 0:
            try:
                self.wait()
                self.driver.execute_script("window.scrollTo(0," + str(height) + ")")
                self.wait()
                followed = self.driver.find_elements_by_xpath("//a[@class='FPmhX notranslate  _0imsa ']")
                followed[random.randint(int(1+(height/50)), int(5+(height/50)))].click()
                self.wait()
                for i in range(1, random.randint(2, 4)):
                    try:
                        images = self.driver.find_elements_by_xpath("//*[@class='_9AhH0']")
                        images[i].click()
                        self.wait()
                        self.driver.find_element_by_xpath("//*[@aria-label='Like']").click()
                        self.wait()
                        print("Liked")
                        self.driver.back()
                        self.wait()
                    except Exception as e:
                        self.driver.back()
                        print(e)
                        print("Like button not found")
                self.driver.back()
                cycles -= 1
            except Exception as e:
                print(e)
                print("Stalk error")
                height = 0
            height += random.randint(50, 100)

    def rest(self, length):
        print("Resting")
        self.wait()
        self.driver.quit()
        time.sleep(length)
        print("Resting done")
        self.login()
        self.popup()
        
files = os.listdir(".")
files = [file for file in files if ".txt" in file]
print(files)

bots = []
for file in files:
    
    bot = autoInsta(file)
    bots.append(bot)
while True:
    bot = bots[0]
    bot.login()
    bot.popup()
    for i in range(0, bot.runamount):
        print("EXPLORING")
        bot.search(random.choice(bot.hashtags))
        bot.explore(random.randint(4, 6))
        if random.randint(1, 100) <= bot.unfollowchance:
            print("UNFOLLOW")
            bot.unfollow(random.randint(int(bot.unfollowamount * 0.8), int(bot.unfollowamount * 1.2)))
        if random.randint(1, 100) <= bot.restchance:
            bot.rest(random.randint(int(bot.restperiod * 0.8), int(bot.restperiod * 1.2)))
        if random.randint(1, 100) <= bot.stalkchance:
            print("STALKING")
            bot.likeProfile(random.randint(int(bot.stalkamount * 0.8), int(bot.stalkamount * 1.2)))
    self.driver.quit()
