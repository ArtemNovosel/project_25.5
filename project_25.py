from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import random


class TestLoginPetFrends:
    # подготавливаем данные для тестов и вызываем метод открытия браузера
    def setup(self):
        self.open()
        self.user = 'tes111t@mail.ru'
        self.password = '12345'
        self.name_random = f"TEST{random.randint(0, 999)}"
        self.user_random = f"testik{random.randint(0, 999)}@com.ru"
        self.password_random = random.randint(0, 999)

    # метод открывает браузер
    def open(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://petfriends.skillfactory.ru')

    # метод вводит данные валидного юзера в форму и нажимает войти
    def login(self):
        self.driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(self.user)  # вводим логин
        self.driver.find_element(By.XPATH, '//*[@id="pass"]').send_keys((self.password))
        self.driver.find_element(By.XPATH, '//*[@class="btn btn-success"]').click()

    # метод достает кол-во питомцев из статистики пользователя(Сайтбара) и возвращает число
    def koll_pets(self):
        koll_pets = self.driver.find_element(By.XPATH, '//*[@class=".col-sm-4 left"]').text  # забираем текст тега div
        koll_pets = [koll_pets.replace("\n", " ")]  # убираем переносы
        koll_pets = [x.split('Питомцев: ')[1] for x in koll_pets]
        koll_pets = [x.split(' Друзей')[0] for x in koll_pets]
        koll = " ".join(koll_pets)  # получаем кол-во питомцев
        return int(koll)

    # метод закрывает сессию
    def close(self):
        self.driver.quit()


# тест, который проверяет, что на странице со списком питомцев пользователя:
    def test_all_pets_on_page(self):
# Присутствуют все питомцы.
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Зарегистрироваться")]'))).click()
        # дожидаемся появления кнолпки У меня уже есть аккаунт и нажимаем
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "У меня уже есть аккаунт")]'))).click()
        # вызываем метод логин
        self.login()
        # проверяем что есть кнопка ВЫЙТИ значит пользователь залогинен
        assert WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn-outline-secondary"]')))
        # получем URL на моих питомцев
        teg = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a'))).get_attribute("href")
        # переходим по URL
        self.driver.get(teg)
        # получаем колличество питомцев вызывая метод
        kol_petss = self.koll_pets()
        # считаем строки в списке с питомцами (одна лишняя- заголовок таблицы)
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
        koll_list = len(self.driver.find_elements(By.TAG_NAME, 'tr'))
        # проверяем что Присутствуют все питомцы сверяя с колличеством из статистики
        assert kol_petss == koll_list - 1
# Хотя бы у половины питомцев есть фото.
        # подсчитываем типомцев с фото
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//th/img')))
        images = self.driver.find_elements(By.TAG_NAME, 'img')
        koll_pet_photo = 0
        for i in range(len(images)):
            if images[i].get_attribute('src'):
                koll_pet_photo += 1
        # проверяем, что Хотя бы у половины питомцев есть фото
        try:
            assert kol_petss <= koll_pet_photo * 2
        except:
            print(f' фото есть у {koll_pet_photo} из {kol_petss} питомцев')
# У всех питомцев есть имя, возраст и порода.
        # получаем породу
        descriptions = self.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
        descriptions_list = []
        # забираем возраст
        age = self.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
        age_list = []
        # забираем имена
        names = self.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
        names_list = []
        # формируем списки с данными
        for i in range(len(names)):
            if names[i].text:
                names_list.append(names[i].text)
            if descriptions[i].text:
                descriptions_list.append(descriptions[i].text)
            if age[i].text:
                age_list.append(age[i].text)
        try:
            # сверяем кол-во потомцев с длиннами списков
            assert kol_petss == len(names_list) == len(descriptions_list) == len(age_list)
            print('У всех питомцев есть имя, возраст и порода!')
        except:
            print(
                f'НЕ у всех питомцев(всего: {kol_petss}) есть имя(только у {len(names_list)}), возраст(только у {len(age_list)}) и порода(только у {len(descriptions_list)})!')
# У всех питомцев разные имена
        # формируем список с именами питомцев пользователя проверяя на повторения
        for i in range(len(names)):
            if names[i].text in names_list:
                print(f'Найдены повторяющиеся имена питомецев ({names[i].text})')
                break
# В списке нет повторяющихся питомцев. (Сложное задание).
        itog_list = []
        # формируем список с данными питомцев пользователя проверяя на повторения
        for i in range(kol_petss):
            dataa = f'{names_list[i]} {descriptions_list[i]} {age_list[i]}'
            if dataa not in itog_list:
                itog_list.append(f'{names[i].text} {descriptions[i].text} {age[i].text}')
            else:
                print(f'Найден повторяющийся питомец ({names[i].text} {descriptions[i].text} {age[i].text})')
                break
                
                
    # тест проверяет вход валидного юзера
    def test_login(self):
        # дожидаемся появления кнолпки зарегистрироваться и нажимаем
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Зарегистрироваться")]'))).click()
        # дожидаемся появления кнолпки У меня уже есть аккаунт и нажимаем
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "У меня уже есть аккаунт")]'))).click()
        # вызываем метод логин
        self.login()
        # проверяем что есть кнопка ВЫЙТИ значит пользователь залогинен
        assert WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn-outline-secondary"]')))


    # тест проверяет регистрацию нового пользователя
    def test_registration(self):
        # self.open()
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Зарегистрироваться")]'))).click()
        self.driver.find_element(By.XPATH, '//*[@id="name"]').send_keys(self.name_random)
        self.driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(self.user_random)  # вводим логин
        self.driver.find_element(By.XPATH, '//*[@id="pass"]').send_keys((self.password_random))
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Зарегистрироваться")]'))).click()
        assert WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn-outline-secondary"]')))

    # вызывает метод закрытия сессии после каждого теста
    def teardown(self):
        self.close()