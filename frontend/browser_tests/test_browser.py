from selenium import webdriver
from selenium.webdriver.common.by import By
import uuid
import os


class ConfigurationException(Exception):
        """Raised when configuration is not complete"""

def get_config(keys):

    d = { }
    for key in keys:
        if key in os.environ:
            d[key] = os.environ[key]
        else:
            raise ConfigurationException(
                    f"environment variable {key} must be set")
    return d

    
def add_and_check_movie(driver, moviename):
    num_movies = len(driver.find_elements(by=By.TAG_NAME, value="article"))

    text_box = driver.find_element(by=By.ID, value="title")
    submit_button = driver.find_element(by=By.ID, value="addmovie")
    text_box.send_keys(moviename)
    submit_button.click()

    movies = driver.find_elements(by=By.TAG_NAME, value="article")
    assert len(movies) == num_movies + 1
    assert moviename in movies[num_movies].text

def test_login_add_movie():
    cfg = get_config(["CHILLER_HOST", "CHILLER_PORT"])
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.binary_location = '/usr/bin/chromium-browser'
    driver = webdriver.Chrome(options=options)

# go to login page
    driver.get(f"http://{cfg["CHILLER_HOST"]}:{cfg["CHILLER_PORT"]}/user/login")

# verify title of login page
    title = driver.title
    assert title == "Log In or Create User - Watch and Chill"

    driver.implicitly_wait(0.5)

# create a user
    username = uuid.uuid4().hex
    text_box = driver.find_element(by=By.ID, value="username")
    submit_button = driver.find_element(by=By.ID, value="create")

    text_box.send_keys(username)
    submit_button.click()

# verify title of movie list page
    title = driver.title
    assert title == "Movie List - Watch and Chill"

# verify no movies in list (no <article> tagged items)
    assert len(driver.find_elements(by=By.TAG_NAME, value="article")) == 0

# add 3 movies including a duplicate and verify it is added ecah time

    m1 = uuid.uuid4().hex
    m2 = uuid.uuid4().hex
    add_and_check_movie(driver, m1)
    add_and_check_movie(driver, m2)
    add_and_check_movie(driver, m1)

# logout
    driver.find_element(by=By.ID, value="logout").click()

# assert on login page again
    title = driver.title
    assert title == "Log In or Create User - Watch and Chill"

    driver.quit()
