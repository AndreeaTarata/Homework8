import time

from selenium import webdriver


chrome = webdriver.Chrome(executable_path=ChromeDriverManager().install()) #instantiere browser
# ca sa accespte si vers cu update
# am instantiat un ob al clasei Chrome din libraria Webdriver
time.sleep(0) # instruim sistemul sa astepte 3 sec inainte de orice comanda
# driver.get deschide site



