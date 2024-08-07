from locust import task, run_single_user
from locust import FastHttpUser, between
import uuid
import logging


class input(FastHttpUser):
#    wait_time = between(0.5,2)

    def test(self):
        self.client.get("/user/login")
        for c in self.client.cookiejar:
            print(c)

    @task
    def t(self):
        username = uuid.uuid4().hex

        logging.debug("\n\n######################## get_user_login() #######################")
        self.get_user_login()
        logging.debug(f"\n\nuser={username}\nrequest.headers={self.response.request.headers}\nresponse.text={self.response.text}\nresponse.status_code={self.response.status_code}\n")

        logging.debug("\n\n######################## post_user_create() #######################")
        self.post_user_create(username)
        logging.debug(f"\n\nuser={username}\nrequest.headers={self.response.request.headers}\nresponse.text={self.response.text}\nresponse.status_code={self.response.status_code}\n")

        for i in range(4):
            logging.debug("\n\n######################## post_movies_add() #######################")
            self.post_movies_add(uuid.uuid4().hex)
            logging.debug(f"\n\nuser={username}\nrequest.headers={self.response.request.headers}\nresponse.text={self.response.text}\nresponse.status_code={self.response.status_code}\n")

        logging.debug("\n\n######################## get_user_logout() #######################")
        self.get_user_logout()
        logging.debug(f"\n\nuser={username}\nrequest.headers={self.response.request.headers}\nresponse.text={self.response.text}\nresponse.status_code={self.response.status_code}\n")



    def get_user_logout(self):
        with self.client.request(
            "GET",
            "/user/logout",
            catch_response=True,
        ) as resp:
            self.response = resp

    def get_user_login(self):
        with self.client.request(
            "GET",
            "/user/login",
            catch_response=True,
        ) as resp:
            self.response = resp

    def post_user_create(self, username):
        data=f"username={username}"
        logging.debug(data)
        with self.client.request(
            "POST",
            "/user/create",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
            catch_response=True,
        ) as resp:
            self.response = resp

    def get_movies_list(self):
        with self.client.request(
            "GET",
            "/movies/list",
            catch_response=True,
        ) as resp:
            self.response = resp

    def post_movies_add(self, title):
        with self.client.request(
            "POST",
            "/movies/add",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"title={title}",
            catch_response=True,
        ) as resp:
            self.response = resp

    def post_user_login(self, username):
        with self.client.request(
            "POST",
            "/user/login",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"username={username}",
            catch_response=True,
        ) as resp:
            self.response = resp

if __name__ == "__main__":
    run_single_user(input)
