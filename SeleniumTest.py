from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class TestSeuBarriga(unittest.TestCase):

		def setUp(self):
				self.driver = webdriver.Chrome()
				self.driver.get("https://seubarriga.wcaquino.me/login")

		def tearDown(self):
				# Fechar o navegador após o teste
				self.driver.quit()

		# Gera um novo login aleatório para teste de cadastro
		def generate_new_user(self):
				now = datetime.now()
				data_hora_str = now.strftime("%Y%m%d_%H%M%S")
				new_login = f"teste{data_hora_str}@teste.com"
				return new_login

		# Testa o cadastro com novo login
		def test_register_and_login(self):
				login_new_user = self.generate_new_user()
				password_new_user = 'senhaestupida123'

				# Localizar página de cadastro
				cadastro = WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, '//*[@id="bs-example-navbar-collapse-1"]/ul/li[2]/a'))
				)
				cadastro.click()

				nome = self.driver.find_element(By.ID, "nome")
				nome.send_keys("Alexandre")
				time.sleep(1)

				email = self.driver.find_element(By.ID, "email")
				email.send_keys(login_new_user)
				time.sleep(1)

				senha = self.driver.find_element(By.ID, "senha")
				senha.send_keys(password_new_user)

				submit = self.driver.find_element(By.XPATH, '/html/body/div[2]/form/input')
				submit.click()
				time.sleep(1)

				try:
						message = self.driver.find_element(By.XPATH, '/html/body/div[1]')
						print(f"Usuário {login_new_user} cadastrado com sucesso: {message.text}")
						print('Passando para tela de login')
						self.login_user(login_new_user, password_new_user)
				except:
						print('Falha no cadastro do usuário')

		def login_user(self, user, password):
				email_field = self.driver.find_element(By.ID, "email")
				email_field.send_keys(user)

				password_field = self.driver.find_element(By.ID, "senha")
				password_field.send_keys(password)

				login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
				login_button.click()
				time.sleep(3)

				try:
						message = self.driver.find_element(By.XPATH, "//div[@class='alert alert-success']")
						print("Login bem-sucedido:", message.text)
				except:
						print("Falha no login.")

if __name__ == "__main__":
		unittest.main()
