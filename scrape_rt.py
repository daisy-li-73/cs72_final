from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Parse args
inputFilename = sys.argv[1]
outputFilename = sys.argv[2]

# Set up output file
f = open(outputFilename, "w")
f.write("IMSDB_Title,RT_Title,CriticScore,AudienceScore\n")

options = ChromeOptions()
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)

driver.get("https://www.rottentomatoes.com/")

# Read input file
with open(inputFilename, "r") as file:
  for line in file:
    found = False

    # Parse input
    parsed_input = line.split(",")
    imsdb_title = parsed_input[0]
    imsdb_writers = parsed_input[1:]
    imsdb_writers_set = set(imsdb_writers)

    # Write IMSDB title to output file
    f.write(imsdb_title+",")

    # Search for movie
    search_string = imsdb_title
    for writer in imsdb_writers:
      search_string += " "+writer
    search_bar = driver.find_element(By.CLASS_NAME, "search-text")
    search_bar.click()
    search_bar.send_keys(search_string)
    search_bar.send_keys(Keys.RETURN)

    # Locate the search results component
    search_results = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "ul[slot='list']"))
    )
    result_items = search_results.find_elements(By.CSS_SELECTOR, "search-page-media-row")  # Adjust the selector as necessary
    result_urls = [result.find_element(By.CSS_SELECTOR, "a[data-qa='info-name']").get_attribute("href") for result in result_items]

    # Iterate through the results
    for result in result_urls:
      driver.get(result)
      # Get list of writers from the movie's page
      movie_info = driver.find_element(By.ID, "info")
      li_elements = movie_info.find_elements(By.TAG_NAME, "li")
      writers_element = li_elements[5]
      span_element = writers_element.find_element(By.CSS_SELECTOR, "span[data-qa='movie-info-item-value']")
      writer_links = span_element.find_elements(By.TAG_NAME, "a")
      rt_writers = [link.text for link in writer_links]

      # Check if the writers match      
      rt_writers_set = set(rt_writers)
      common_writers = imsdb_writers_set.intersection(rt_writers_set)
      # threshold = min(len(imsdb_writers_set), len(rt_writers_set)) / 2
      # If match found, get audience and critic scores and write to output file
      if common_writers == imsdb_writers_set:
        rt_title = driver.find_element(By.CLASS_NAME, "title").text

        try:
          scoreboard = WebDriverWait(driver, 10).until(
              EC.presence_of_element_located((By.ID, "scoreboard"))
          )
          critic_score = scoreboard.get_attribute("tomatometerscore")
          audience_score = scoreboard.get_attribute("audiencescore")

        except TimeoutException:
          f.write(",,,")
          continue
        except NoSuchElementException:
          f.write(",,,")
          continue

        f.write(f"{rt_title},{critic_score},{audience_score}\n")
        found = True
        break
    
    if found == False:
      f.write(",,,")

f.close()
driver.quit()

    


