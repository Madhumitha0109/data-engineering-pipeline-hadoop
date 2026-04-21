from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import urllib.request
import os
import time
import json

# Create images and metadata directories
os.makedirs("./images", exist_ok=True)
os.makedirs("./metadata", exist_ok=True)

# to run Chrome in headless mode
options = Options()
# options.add_argument("--headless")

# initialize Chrome WebDriver
driver = webdriver.Chrome(
    service=ChromeService(),
    options=options
)

driver.maximize_window()

url = "https://unsplash.com/t/wallpapers"
driver.get(url)

# Scroll until at least 100 image elements are loaded
scroll_pause_time = 2
min_images = 100

while True:
    image_html_nodes = driver.find_elements(By.CLASS_NAME, "czQTa")
    if len(image_html_nodes) >= min_images:
        break
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

print(f"Found {len(image_html_nodes)} image elements.")

# select the image elements
image_html_nodes = driver.find_elements(By.CLASS_NAME, "czQTa")

# where to store scraped image metadata
image_metadata_list = []
image_name_counter = 1

for image_html_node in image_html_nodes:
    try:
        image_url = image_html_node.get_attribute("src")

        # get higher resolution URL
        srcset = image_html_node.get_attribute("srcset")
        if srcset is not None:
            srcset_last_element = srcset.split(", ")[-1]
            image_url = srcset_last_element.split(" ")[0]

        if not image_url or not image_url.startswith("http"):
            continue

# Extract metadata
        metadata = {
            "image_url": image_url,
        }
        # Click image to open detail page
        driver.execute_script("arguments[0].click();", image_html_node)
        # Wait for the views element to appear
        time.sleep(2)  # adjust if needed for slower internet

        # Description
        try:
            metadata["description"] = image_html_node.get_attribute("alt")
        except:
            metadata["description"] = None

        # Photographer
        try:
            photographer_element = driver.find_element(By.CSS_SELECTOR, "a.bimlc.Pc_c1.rkYpC.wQd_A")
            photographer_name = photographer_element.text.strip()
            metadata["photographer_name"] = photographer_name
        except Exception:
            metadata["photographer_name"] = None

        

        # Views & Downloads count
        try:
            # Find the container with both views and downloads info
            container = driver.find_element(By.CLASS_NAME, "T6zc2")

            # Find all child divs inside it
            info_blocks = container.find_elements(By.TAG_NAME, "div")

            views_text = None
            downloads_text = None

            for block in info_blocks:
                try:
                    label = block.find_element(By.TAG_NAME, "h3").text.strip()
                    value = block.find_element(By.CLASS_NAME, "sZ3iN").text.strip()

                    if label == "Views":
                        views_text = value
                    elif label == "Downloads":
                        downloads_text = value
                except:
                    continue

        except:
            views_text = None
            downloads_text = None

        metadata["views"] = views_text
        metadata["downloads"] = downloads_text  

       # Location, Published Time & License type
        location_text = None
        published_time = None
        license_type = None
        
        try:
            # Find the container
            metadata_container = driver.find_element(By.CLASS_NAME, "sS8aU")
    
            # Find all possible metadata spans
            info_blocks = metadata_container.find_elements(By.CLASS_NAME, "nJlr7")
    
            for block in info_blocks:
                try:
                    desc_tag = block.find_element(By.TAG_NAME, "desc").get_attribute("innerHTML").strip()
            
                    if "map marker" in desc_tag.lower():
                        # This is the location block
                        location_text = block.find_element(By.CLASS_NAME, "X5fE_").text.strip()
                    elif "calendar" in desc_tag.lower():
                        # This is the published time block
                        published_time = block.find_element(By.TAG_NAME, "time").get_attribute("datetime")

                    span_text = block.text.strip()
                    # License
                    if "Free to use" in span_text:
                        license_type = "Free"
                    elif "Unsplash+ License" in span_text:
                        license_type = "Premium"

                except Exception:
                    continue
        
        except Exception:
            pass

        metadata["location"] = location_text
        metadata["published_time"] = published_time
        metadata["license"] = license_type

        # Tags
        tags = []
        try:
            tags_container = driver.find_element(By.CLASS_NAME, "uN4_r")
            tag_links = tags_container.find_elements(By.TAG_NAME, "a")
    
            for tag in tag_links:
                tag_text = tag.text.strip()
                if tag_text:
                    tags.append(tag_text)
        except Exception:
            pass

        metadata["tags"] = tags

        # Close the detail view (Unsplash uses Escape)
        webdriver.ActionChains(driver).send_keys(u'\ue00c').perform()

        # Wait for modal to close
        time.sleep(1)

        # Append metadata
        image_metadata_list.append(metadata)

        # Download image
        print(f"Downloading image no. {image_name_counter} ...")
        file_name = f"./images/{image_name_counter}.jpg"
        urllib.request.urlretrieve(image_url, file_name)
        print(f"Image downloaded successfully to '{file_name}'\n")

        image_name_counter += 1

        if image_name_counter > 100:     # Stop after 100 images
            break

    except StaleElementReferenceException:
        continue

# Save metadata as JSON
metadata_file = "./metadata/images_metadata.json"
with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(image_metadata_list, f, ensure_ascii=False, indent=4)

print(f"Saved metadata to {metadata_file}")

# Close browser
driver.quit()
