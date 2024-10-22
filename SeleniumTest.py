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
				self.driver.quit()

		# Gera um novo login aleatório para teste de cadastro
		def generate_new_user(self):
				now = datetime.now()
				data_hora_str = now.strftime("%Y%m%d_%H%M%S")
				new_login = f"teste{data_hora_str}@teste.com"
				return new_login

		# Gera uma nova fatura aleatoria
		def generate_new_invoice(self):
				now = datetime.now()
				data_hora_str = now.strftime("%Y%m%d_%H%M%S")
				new_invoice_name = f"Fatura do Aluguel - Vencimento {data_hora_str}"
				return new_invoice_name

		# Testa o cadastro com novo login
		def test_register_and_login(self):
				login_new_user = self.generate_new_user()
				password_new_user = 'senhaestupida123'

				cadastro = WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, '//*[@id="bs-example-navbar-collapse-1"]/ul/li[2]/a'))
				)
				cadastro.click()

				nome = WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.ID, "nome"))
				)
				nome.send_keys("Alexandre")
				time.sleep(1)
				email = self.driver.find_element(By.ID, "email")
				email.send_keys(login_new_user)
				time.sleep(1)
				senha = self.driver.find_element(By.ID, "senha")
				senha.send_keys(password_new_user)
				time.sleep(1)
				submit = self.driver.find_element(By.XPATH, '/html/body/div[2]/form/input')
				submit.click()

				try:
						message = WebDriverWait(self.driver, 10).until(
								EC.presence_of_element_located((By.XPATH, '/html/body/div[1]'))
						)
						print(f"Usuário {login_new_user} cadastrado com sucesso: {message.text}")
						print('Passando para tela de login')
						self.login_user(login_new_user, password_new_user)
						time.sleep(2)
						self.add_invoice()
				except Exception as e:
						print('Falha no cadastro do usuário:', str(e))

		# Loga o usuário recém-criado
		def login_user(self, user, password):
				email_field = self.driver.find_element(By.ID, "email")
				email_field.send_keys(user)
				time.sleep(1)
				password_field = self.driver.find_element(By.ID, "senha")
				password_field.send_keys(password)
				time.sleep(1)
				login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
				login_button.click()

				try:
						message = WebDriverWait(self.driver, 10).until(
								EC.presence_of_element_located((By.XPATH, "//div[@class='alert alert-success']"))
						)
						print("Login bem-sucedido:", message.text)
				except Exception as e:
						print("Falha no login:", str(e))

		# Adiciona nova fatura
		def add_invoice(self):
				new_invoice = self.generate_new_invoice()
				nav_bar = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[2]/a')
				nav_bar.click()
				add = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[2]/ul/li[1]/a')
				add.click()

				invoice_name = self.driver.find_element(By.ID,"nome")
				invoice_name.send_keys(new_invoice)
				time.sleep(1)
				save = self.driver.find_element(By.XPATH, '/html/body/div[2]/form/div[2]/button')
				save.click()

				try:
						message = WebDriverWait(self.driver, 10).until(
								EC.presence_of_element_located((By.XPATH, "//div[@class='alert alert-success']"))
						)
						print(f'Conta adicionada com sucesso! {message.text}')
						self.list_and_edit_invoice()
				except Exception as e:
						print('Erro ao adicionar nova conta:', str(e))

		# Lista e edita fatura
		def list_and_edit_invoice(self):
				nav_bar = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[2]/a')
				nav_bar.click()
				list_invoices = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[2]/ul/li[2]/a')
				list_invoices.click()
				edit_invoice = self.driver.find_element(By.XPATH, '//*[@id="tabelaContas"]/tbody/tr/td[2]/a[1]/span')
				edit_invoice.click()
				new_invoice = self.generate_new_invoice()
				invoice_name = self.driver.find_element(By.ID,"nome")
				invoice_name.clear()
				invoice_name.send_keys(new_invoice)
				time.sleep(1)
				save = self.driver.find_element(By.XPATH, '/html/body/div[2]/form/div[2]/button')
				save.click()
				try:
						message = WebDriverWait(self.driver, 10).until(
								EC.presence_of_element_located((By.XPATH, "//div[@class='alert alert-success']"))
						)
						print(f'Conta alterada com sucesso! {message.text}')
						self.delete_invoice()
				except Exception as e:
						print('Erro ao alterar conta:', str(e))

		# Deleta fatura
		def delete_invoice(self):
				delete_invoice = self.driver.find_element(By.XPATH, '//*[@id="tabelaContas"]/tbody/tr/td[2]/a[2]/span')
				delete_invoice.click()
				time.sleep(2)
				print('Fatura deletada com sucesso.')



if __name__ == "__main__":
		unittest.main()
