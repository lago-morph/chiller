from wac_session import WaCSessionLoadTest, SeleniumSession, RemoteSeleniumSession
import time
import random

#with RemoteSeleniumSession("http://localhost:4444") as sess:
with SeleniumSession() as sess:
    time.sleep(random.random() * 30)
    while True:
        ws = WaCSessionLoadTest(sess.driver, sess.baseURL)
        #ws.run_short_script()
        ws.run_load_script()
