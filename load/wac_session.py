from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.by import By
import uuid
import os

class ConfigurationException(Exception):
        """Raised when configuration is not complete"""

class WaCSession():
    """ a session of using watch and chill (wac) using Selenium driver """

    def __init__(self, driver, baseURL):
        # web driver must have already been initialized
        self._driver = driver
        self._baseURL = baseURL
        self._username = uuid.uuid4().hex

    def navigate_login(self):
        """ go to the login page using baseURL passed at class instantiation """
        self._driver.get(f"{self._baseURL}/user/login")
        assert self.at_login()

    def at_login(self):
        """ assertion that we are on the login page based on title """
        return self._driver.title == "Log In or Create User - Watch and Chill"

    def at_movielist(self):
        """ assertion that we are on the movie list page based on title """
        return self._driver.title == "Movie List - Watch and Chill"

    def logout(self):
        """ find the logout link that should be on every page and select """
        self._driver.find_element(by=By.ID, value="logout").click()

        assert self.at_login()
    
    def add_movie(self):
        """ adds a movie for the currently logged in user """
        assert self.at_movielist()
        moviename = uuid.uuid4().hex
        num_movies = len(self._driver.find_elements(by=By.TAG_NAME, value="article"))

        self._driver.find_element(by=By.ID, value="title").send_keys(moviename)
        self._driver.find_element(by=By.ID, value="addmovie").click()

        movies = self._driver.find_elements(by=By.TAG_NAME, value="article")
        assert len(movies) == num_movies + 1
        assert moviename in movies[num_movies].text


    def add_movies(self, num):
        """ add num movies """
        for i in range(num):
            self.add_movie()

    def login(self, intended_fail = False):
        self.navigate_login()
        self.login_create("login", intended_fail)

    def create_user(self, intended_fail = False):
        self.navigate_login()
        self.login_create("create", intended_fail)

    def login_create(self, button_value, intended_fail):
        """ login or create user """
        self._driver.find_element(by=By.ID, value="username").send_keys(self._username)
        self._driver.find_element(by=By.ID, value=button_value).click()

        if intended_fail:
            assert self.at_login()
        else:
            assert self.at_movielist()

class WaCSessionLoadTest(WaCSession):

    def run_load_script(self):
        self.login(intended_fail=True)  # user has not been created
        self.create_user()
        self.add_movies(4)
        self.logout()
        for i in range(9):
            self.login()
            self.add_movies(4)
            self.logout()
        self.create_user(intended_fail=True) # user already created, duplicate
   
    def run_short_script(self):
        self.create_user()
        self.add_movies(4)
        self.logout()
    
class SeleniumSession():
    """ a session using Selinum using standard config 
        should use as follows:

        with SeleniumSession() as sess:
            # do stuff with sess instance object
    """
    def __init__(self):
        self.setup()

    def setup(self, remoteURL = None):
        self._method = "http"
        self._cfg = self.get_config(["CHILLER_HOST", "CHILLER_PORT"])
        options = webdriver.ChromeOptions()
        if remoteURL is None:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.binary_location = '/usr/bin/chromium'
            #options.binary_location = '/usr/bin/chromium-browser'
            self._driver = webdriver.Chrome(options=options)
        else:
            print(remoteURL)
            self._driver = RemoteWebDriver(command_executor=remoteURL,options=options)

        self._driver.implicitly_wait(0.5)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._driver.quit()

    def get_config(self, keys):
        d = { }
        for key in keys:
            if key in os.environ:
                d[key] = os.environ[key]
            else:
                raise ConfigurationException(
                    f"environment variable {key} must be set")
        return d

    @property
    def baseURL(self):
        host = self._cfg['CHILLER_HOST']
        port = self._cfg['CHILLER_PORT']
        return f"{self._method}://{host}:{port}"

    @property
    def driver(self):
        return self._driver
    
class RemoteSeleniumSession(SeleniumSession):
    def __init__(self, remoteURL):
        print(remoteURL)
        self.setup(remoteURL)
