from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Parse args
outputFilename = sys.argv[1]

# Set up output file
f = open(outputFilename, "w")

# Initialize Chrome driver
options = ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get("https://imsdb.com/all-scripts.html")

# Get all movie scripts
movies = driver.find_elements(By.CSS_SELECTOR, "p")

# Iterate over each movie to extract its title, writers, script link and write into CSV
for m in movies:
  a_tag = m.find_element(By.TAG_NAME, "a")
  title = a_tag.text

  # Get writers
  i_tag = p.find_element(By.TAG_NAME, "i")
  writers = i_tag.text  # This will include 'Written by'
  writers = writer_text.replace("Written by ", "") 

  f.write(title+","+writers+"\n")

  # Navigate to next page, download script
  movie_link = a_tag.get_attribute("href") 

  
   
f.close()
driver.quit()    