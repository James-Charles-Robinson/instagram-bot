from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import os

# main class
class autoInsta:
    
    def __init__(self, path):
        
        # Opens settings file and assigns values
        with open(path, "r") as f:
            settings = f.readlines()
            settings = [setting.split("= ")[1].replace("\n", "") for setting in settings]
            
        self.username = str(settings[0])
        self.password = str(settings[1])
        self.maxwait = int(settings[2])
        if self.maxwait < 3:
            self.maxwait = 3
        self.restperiod = int(settings[3])
        self.restchance = int(settings[4])
        self.unfollowchance = int(settings[5])
        self.unfollowamount = int(settings[6])
        self.stalkchance = int(settings[7])
        self.stalkamount = int(settings[8])
        self.followchance = int(settings[9])
        self.followspecificamount = int(settings[10])
        self.followspecificchance = int(settings[11])
        self.hashtags = settings[12].split(", ")
        self.runamount = int(settings[13])

    # waits with random time
    def wait(self):
        self.driver.implicitly_wait(10)
        time.sleep(random.randint(0, self.maxwait))
    
    # logs in and starts the browser
    def login(self):

        userAgent = "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36"
        profile = webdriver.FirefoxProfile() #starts webbrowser emulating as a phone
        profile.set_preference("general.useragent.override", userAgent)
        self.driver = webdriver.Firefox(profile)
        self.driver.set_window_size(540,960)

        self.driver.get("https://www.instagram.com/accounts/login/")
        self.wait()
        
        # enters all the needed info
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

    # clicks the Not Now button of the pop up
    def popup(self):
        try:
            notNow = self.driver.find_element_by_xpath(
                "//button[contains(text(),'Not Now')]")
            notNow.click()
            self.wait()
        except Exception as e:
            print(e)

    # searches for the givin hastag
    def search(self, term, reach):
        self.wait()
        # clicks the button on the bottom row
        button = self.driver.find_element_by_xpath(
            "//a[@href='/explore/']")
        button.click()
        self.wait()
        self.wait()
        
        # clicks on the search bar and types
        bar = self.driver.find_element_by_xpath(
            "//input[@type='search']")
        bar.send_keys(term)
        self.wait()
        bar.send_keys(Keys.RETURN)
        self.wait()
        
        # clicks one of the top results
        links = self.driver.find_elements_by_xpath('//a[@href]')
        link = links[random.randint(0, reach)].find_element_by_xpath('.//*')
        link.click()

    # scrolls down the results,pics random posts and likes or follows them
    def explore(self, cycles):
        run = True
        while cycles > 0:
            self.wait()
            for i in range(1, random.randint(4, 8)):
                # scrolls down the page a little randomly
                height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("window.scrollTo(0," + str(height-random.randint(400, 1000)) + ")")
                self.wait()
            try:
                # clicks on one of the pictures and likes it
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
                    # follows them
                    self.driver.find_element_by_xpath("//button[@type='button']").click()
                    print("Followed")
                    self.wait()
                    name = self.driver.find_elements_by_xpath("//a")
                except Exception as e:
                    print(e)
                    print("Follow button not found")
            self.driver.back()

    # goes back to profile and unfollows some users
    def unfollow(self, cycles):
        self.wait()
        self.driver.find_elements_by_xpath("//span[@role='link']")[-1].click()
        self.wait()
        self.driver.find_elements_by_xpath("//li")[2].click()
        height = 1500
        # starts 1500 pixels down to unfollow people followed a few days/hours ago
        while cycles > 0:
            self.wait()
            # scrolls
            followed = self.driver.find_elements_by_xpath("//button[@type='button']")
            self.driver.execute_script("window.scrollTo(0," + str(height) + ")")
            try:
                # picks a random person and unfollows
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

    # goes onto someones account and likes some of thier posts, also known as stalking
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
                # picks random follower
                self.wait()
                for i in range(1, random.randint(2, 4)):
                    try:
                        # clicks on thier posts and likes them
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

    # logs out the user and closes the browser to emulate the user doing another task
    def rest(self, length):
        print("Resting")
        self.wait()
        self.driver.quit()
        time.sleep(length)
        print("Resting done")
        self.login()
        self.popup()

    def followSpecificUser(self, amount):
        with open("AccountsToFollow.txt", "r") as f:
            users = f.readlines()
        users = [user.replace("\n", "") for user in users]
        if len(users) > 0:
            for i in range(amount):
                try:
                    user = users[random.randint(0, len(users)-1)]
                    users.remove(user)
                    self.search(user, 0)
                    self.wait()
                    self.driver.find_element_by_xpath("//button[contains(text(),'Follow')]").click()
                    self.wait()
                except:
                    pass
            with open("AccountsToFollow.txt", "w") as f:
                for user in users:
                    f.write(user + "\n")

# main section of the program
files = os.listdir(".")
files = [file for file in files if ".txt" in file and "User" in file]
print(files)

# creates a list of users accounts and details so multiple accounts can be done at a time
bots = []
for file in files:
    bot = autoInsta(file)
    bots.append(bot)
    
while True:
    for bot in bots:
        bot.login()
        bot.popup()
        for i in range(0, bot.runamount):
            print("EXPLORING")
            bot.search(random.choice(bot.hashtags), 2)
            bot.explore(random.randint(4, 6))
            if random.randint(1, 100) <= bot.unfollowchance:
                print("UNFOLLOW")
                bot.unfollow(random.randint(int(bot.unfollowamount * 0.8), int(bot.unfollowamount * 1.2)))
            if random.randint(1, 100) <= bot.restchance:
                bot.rest(random.randint(int(bot.restperiod * 0.8), int(bot.restperiod * 1.2)))
            if random.randint(1, 100) <= bot.stalkchance:
                print("STALKING")
                bot.likeProfile(random.randint(int(bot.stalkamount * 0.8), int(bot.stalkamount * 1.2)))
            if random.randint(1, 100) <= bot.followspecificchance:
                print("FOLLOWING SPECIFIC USERS")
                bot.followSpecificUser(bot.followspecificamount)
        self.driver.quit()
