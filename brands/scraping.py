from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options

brands = [
	'mxuvW8VSR4aT4e3e8',
	'hzxWpA7HdpVC7w7XA',
	'3VQFFWqLNyg4sGf97',
]

short_url_maps = 'https://goo.gl/maps/:brand'

def scroll_element(driver, element):
	last_height = driver.execute_script("return arguments[0].scrollHeight", element)

	while True:
		driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
		time.sleep(2)
		new_height = driver.execute_script("return arguments[0].scrollHeight", element)

		if new_height == last_height:
			print("Não é mais possível rolar para baixo.")
			break
		
		last_height = new_height

def get_reviews(driver, url):
	driver.get(url)

	elemento = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.XPATH, "//div[text()='Avaliações']"))
	)
	
	elemento.click()

	WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.CSS_SELECTOR, '.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde'))
	)

def extract_data(div):
	aria_label = div.get('aria-label')
	img_src = ''
	span_aria_label = ''
	content = ''
	comment = ''
	
	img = div.find('img', class_='NBa7we')
	if img:
		img_src = img.get('src')

	span_img = div.find('span', class_='kvMYJc', role='img')
	if span_img:
		span_aria_label = span_img.get('aria-label')

	span_content = div.find('span', class_='rsqaWe')
	if span_content:
		content = span_content.get_text(strip=True) 

	span_comment = div.find('span', class_='wiI7pd')
	if span_comment:
		comment = span_comment.get_text(strip=True)

	img_comment = div.find_all('button', class_='Tya61d')
	background_images = []
					
	for button in img_comment:
		style = button.get('style')
		
		if style and 'background-image' in style:
			url_start = style.find('url(') + 4
			url_end = style.find(')', url_start)
			background_image_url = style[url_start:url_end].strip('"')
			background_images.append(background_image_url)
	
	return {
		'createdAt': content,
		'avatar': img_src,
		'rating': span_aria_label,
		'name': aria_label,
		'comment': comment,
		'comment_imgs': background_images,
	}

def scraping(brands):
	options = Options()
	options.add_argument("--headless")

	driver = webdriver.Chrome(options=options)

	data = []

	try:
		for brand in brands:
			uri = brand.get('uri', '')

			url = short_url_maps.replace(':brand', uri)

			get_reviews(driver, url)

			scrollable_element = driver.find_element(By.CSS_SELECTOR, '.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde')

			time.sleep(3)

			scroll_element(driver, scrollable_element)

			div_html = scrollable_element.get_attribute('outerHTML')

			formatted_html = BeautifulSoup(div_html, 'html.parser')

			target_divs = formatted_html.find_all('div', class_='jftiEf fontBodyMedium')
			
			reviews = []

			for _, div in enumerate(target_divs, start=1):
				reviews.append(extract_data(div))		

			data.append({
				'brand': brand.get('name', ''),
				'reviews': reviews,
			})
						
	except Exception as e:
		print(f"Ocorreu um erro: {e}")

	finally:
		driver.quit()

		return data
