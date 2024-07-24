from wac_session import WaCSessionLoadTest, SeleniumSession, RemoteSeleniumSession

#with RemoteSeleniumSession("http://localhost:4444") as sess:
with SeleniumSession() as sess:
    print(sess.baseURL)
    ws = WaCSessionLoadTest(sess.driver, sess.baseURL)
    #ws.run_short_script()
    ws.run_load_script()
