'''
Intrati pe site-ul https://www.elefant.ro/ si efectuati urmatoarele teste:

- Test 1: Identificati butonul "accept cookies" si dai click pe el
- Test 2: cautati un produs la alegere (iphone 14) si verificati ca s-au returnat cel putin 10 rezultate ([class="product-title"])
- Test 3: Extrageti din lista produsul cu pretul cel mai mic [class="current-price "] -> //img[@class="product-image"]
- Test 4: Extrageti titlul paginii si verificati ca este corect
- Test 5: Intrati pe site, accesati butonul cont si click pe conectare.Identificati elementele de tip user si parola si inserati valori incorecte (valori incorecte inseamna oricare valori care nu sunt recunscute drept cont valid)
- Dati click pe butonul "conectare" si verificati urmatoarele:
            1. Faptul ca nu s-a facut logarea in cont
            2. Faptul ca se returneaza eroarea corecta
- Test 6: Stergeti valoarea de pe campul email si introduceti o valoare invalida (adica fara caracterul "@") si verificati faptul ca butonul "conectare" este dezactivat
'''
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class TestLogin(unittest.TestCase):
    cookies = (By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
    search = (By.NAME, 'SearchTerm')
    searchbtn = (By.NAME, 'search')
    cont = (By.XPATH, '//*[@id="HeaderRow"]/div[4]/div/ul/li[1]/a[1]/div/span[2]')
    conectare = (By.XPATH, '//*[@id="account-layer"]/a[1]')
    user = (By.XPATH, '//*[@id="ShopLoginForm_Login"]')
    psw = (By.ID, 'ShopLoginForm_Password')
    text_user_invalid = 'Te rugăm să introduci o adresă de e-mail validă.'
    user_invalid = (By.CLASS_NAME, 'help-block')
    text_invalid_login = 'Adresa dumneavoastră de email / Parola este incorectă. Vă rugăm să încercați din nou.'
    invalid_login = (By.CLASS_NAME, 'alert alert-danger')
    conectare_btn = (By.XPATH, '/html/body/div[2]/div/div[9]/div[1]/div/div[1]/div/form/div[4]/div/button')

    def setUp(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get('https://elefant.ro')
        self.driver.maximize_window()
        time.sleep(2)

    def test1_accept_cookies(self):
        self.driver.find_element(*self.cookies).click()

    def test2_seach_item(self):
        self.driver.find_element(*self.cookies).click()
        time.sleep(3)
        self.driver.find_element(*self.search).send_keys('iphone 14')
        self.driver.find_element(*self.searchbtn).click()
        time.sleep(3)
        rezultate = self.driver.find_elements(By.CLASS_NAME, "product-title")
        if len(rezultate) > 10:
            print(f'Sunt mai mult ede 10 rezultate, respectiv sunt {rezultate}')
        else:
            print(f'Cautarea a esuat. Sunt doar {rezultate}')

    def test3_pret_mic(self):
        self.driver.find_element(*self.cookies).click()
        self.driver.find_element(*self.search).send_keys('iphone 14')
        self.driver.find_element(*self.searchbtn).click()
        time.sleep(4)
        # self.driver.find_element(By.ID, "SortingAttribute").click()
        # self.driver.find_element(*self.cel_mai_mic_pret).click()
        # time.sleep(5)
        sorteaza = Select(self.driver.find_element(By.ID, 'SortingAttribute'))
        time.sleep(3)
        sorteaza.select_by_visible_text("Pret crescator")
        time.sleep(7)

        elemet_prices = self.driver.find_elements(By.CLASS_NAME, 'current-price')
        dict_elemente = {}
        return_elements = self.driver.find_elements(By.CLASS_NAME, 'product-title')
        for i in range(len(return_elements)):
            dict_elemente[return_elements[i].text] = elemet_prices[i].text.replace(".", "").replace(",", "").replace(
                " lei", "")[:-3]
        min_price = 99999999999999
        prod_min = ""
        for key, value in dict_elemente.items():
            min_price = value
            prod_min = key
        print(f'Produsul cu cel mai mic pret este: {prod_min} si valoarea de {min_price} lei')

    def test4_titlul_paginii(self):
        titlu = self.driver.title
        print(titlu)
        actual_url = "elefant.ro - mallul online al familiei tale! • Branduri de top, preturi excelente • Peste 500.000 de produse pentru tine!"
        self.assertTrue(actual_url, titlu)

    def test5_date_incorecte(self):
        self.driver.find_element(*self.cookies).click()
        time.sleep(3)
        self.driver.find_element(*self.cont).click()
        time.sleep(3)
        self.driver.find_element(*self.conectare).click()
        self.driver.find_element(*self.user).send_keys('aaa@gmail.com')
        time.sleep(3)
        self.driver.find_element(*self.psw).send_keys('bbb')

        valid_user = True
        if self.text_invalid_login == self.invalid_login:
            valid_user = False
        assert valid_user, 'Invalid user'
        self.assertTrue(self.text_invalid_login, self.invalid_login)

    def test6_invalid_email(self):
        self.driver.find_element(*self.cookies).click()
        time.sleep(3)
        self.driver.find_element(*self.cont).click()
        time.sleep(3)
        self.driver.find_element(*self.conectare).click()
        valoare_user = self.driver.find_element(*self.user)
        time.sleep(3)
        valoare_user.send_keys('aaa@gmail.com')
        valoare_user.clear()
        self.driver.find_element(*self.user).send_keys('aaagmail.com')
        valid_user = True
        if self.text_user_invalid == self.user_invalid:
            valid_user = False
        assert valid_user, 'Invalid user'
        self.assertTrue(self.text_user_invalid, self.user_invalid)
        buton_activ = self.driver.find_element(*self.conectare_btn).is_enabled()

        self.assertFalse(buton_activ)



    def tearDown(self) -> None:
        self.driver.close()
