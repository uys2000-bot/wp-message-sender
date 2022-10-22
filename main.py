
from cmath import nan
from xml.etree.ElementTree import tostring
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import re


class cssRemoved(object):
    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = self.locator  # Finding the referenced element
        if self.css_class in element.get_attribute("class"):
            return False
        else:
            return element


def toastRemover(driver):
    driver.execute_script("""
    var element = document.querySelector("#toasts");
    if (element)
        element.parentNode.removeChild(element);
    """)


def waitLocateWithClass(wait, name):
    print("wait locating", name)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, name)))
        return True
    except TimeoutException:
        return False


def waitLocatedWithId(wait, name):
    print("wait locating", name)
    try:
        wait.until(EC.presence_of_element_located((By.ID, name)))
        return True
    except TimeoutException:
        return False


def waitLocatedWithPath(wait, name):
    print("wait locating", name)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, name)))
        print("wait locating ended", name)
        return True
    except TimeoutException:
        return False


def waitCssRemoved(wait, item, name):
    print("wait remove tag", name)
    try:
        wait.until(cssRemoved(item, name))
        return True
    except TimeoutException:
        return False
    except:
        time.sleep(1)


def cFinderM(driver, name):
    return driver.find_elements(By.CLASS_NAME, name)


def iFinderM(driver, name):
    return driver.find_elements(By.ID, name)


def cFinder(driver, name):
    return driver.find_element(By.CLASS_NAME, name)


def iFinder(driver, name):
    return driver.find_element(By.ID, name)


def xFinder(driver, name):
    return driver.find_element(By.XPATH, name)


def waitFind(driver, wait, waiter, finder, name):
    waiter(wait, name)
    return finder(driver, name)


def scroll(driver, item):
    x = item.location['x']
    y = item.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (x, y)
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    driver.execute_script(scroll_by_coord)
    driver.execute_script(scroll_nav_out_of_way)


def scroller(driver, item):
    try:
        scroll(driver, item)
        actions = ActionChains(driver)
        actions.move_to_element(item)
        actions.click()
        return True
    except:
        return False


def clicker(driver, item):
    try:
        if (scroller(driver, item)):
            item.click()
            return True
        else:
            False
    except:
        return False


def getPage(i):
    if str(i)[0] == "0":
        print(
            f"https://web.whatsapp.com/send/?phone=+9{str(i)}&text&type=phone_number&app_absent=0")
        driver.get(
            f"https://web.whatsapp.com/send/?phone=+9{str(i)}&text&type=phone_number&app_absent=0")
        return True
    elif str(i)[0] == "N":
        print("elif pass")
        return False
    else:
        print(
            f"https://web.whatsapp.com/send/?phone=+90{str(i)}&text&type=phone_number&app_absent=0")
        driver.get(
            f"https://web.whatsapp.com/send/?phone=+90{str(i)}&text&type=phone_number&app_absent=0")
        return True


def sendMessage():
    waitLocatedWithPath(wait, '//*[@title="Type a message"]')
    text = xFinder(driver, '//*[@title="Type a message"]')
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@title="Type a message"]')))
    for t in "\nhttps://chat.whatsapp.com/Kp9HE6AwRotBW10HTiRJUG\nİstinye Oyun Geliştiricileri Kulübü WhatsApp duyuru grubuna katılmanızı bekliyoruz. Bu gurupta yapacağımız etkinlikler hakkında sizleri bilgilendiriyor olacağız.\nWe are waiting for you to join the İstinye Game Developers Club WhatsApp announcement group. We will inform you about the activities we will do in this group.\Gizlilik Uyarısı: Bu  mesajı ve ekinde bulunabilecek dosyalar yalnız mesajın alıcı hanesinde kayıtlı kullanıcı/kullanıcılar içindir. Mesajın alıcısı değilseniz, lütfen hemen göndericiyi uyarınız. Mesajı dağıtmayınız, kopyalamayınız, içeriğini açıklamayınız ve çıktı almaksızın siliniz.\nPrivacy Notice: This message and the files that may be found in its attachment are only for the user(s) registered in the recipient section of the message. If you are not the recipient of the message, please alert the sender immediately. Do not distribute the message, do not copy it, do not explain its content and delete it without printing.":
        text.send_keys(t)
    text.send_keys(Keys.ENTER)
    waitLocatedWithPath(wait, '//*[@data-icon="msg-time"]')
    WebDriverWait(driver, 100).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@data-icon="msg-time"]')))
    wait.until(EC.invisibility_of_element_located(
        (By.XPATH, '//*[@data-icon="msg-time"]')))


def runBot(i):
    if getPage(i):
        try:
            sendMessage()
        except:
            runBot(i)


driver = webdriver.Firefox()
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 1000)
waitLocateWithClass(wait, "selectable-text")

dataframe1 = pd.read_excel('liste.xlsx')
datas = dataframe1["Cep Telefonu"]
datas = ["5435930151", "05516393619"]

file = open("n.txt", "r")


pattern = r'<td>([^<]*)<\/td>'
text = file.read()
results = re.findall(pattern, text)
print(results)
for i in results:
    if len(i) > 2:
        if (i[0] == "0" or i[0] == "5"):
            print(i.replace(" ", ""))
            if (i[0] != "0"):
                i = "0"+i
            runBot(i)
# for i in datas:
#    runBot(i)
