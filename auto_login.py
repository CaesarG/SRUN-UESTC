import os
import config
import time
import logging
import requests
from logging.handlers import RotatingFileHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


class AutoLogin(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_gateway = "http://10.253.0.235/srun_portal_pc?ac_id=3&theme=yd"

        if config.log:  # 记录log
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(level=logging.INFO)
            handler = RotatingFileHandler(
                os.path.join(config.log_path, "log.txt"),
                maxBytes=5 * 1024 * 1024,
                backupCount=5,
            )
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            if config.debug:  # debug 在控制台输出
                console = logging.StreamHandler()
                console.setLevel(logging.INFO)
                self.logger.addHandler(console)

        # 使用webdriver_manager自动下载和安装ChromeDriver
        self.service = Service("/usr/local/bin/chromedriver")
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")  # 如果你希望在无头模式下运行（没有UI）
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

    def _check_network(self):
        """
        检查网络是否畅通
        :return: Ture为畅通，False为不畅通。
        """
        try:
            req = requests.get("http://www.baidu.com", timeout=5)
            if "baidu" in req.text:
                return True
            else:
                return False
        except:
            return False

    def _login_srun(self):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)  # 超时
        try:
            driver.get(self.login_gateway)
        except:
            self.logger.warning("Get gateway out of time....try again soon")
            return
        time.sleep(2)
        username_box = driver.find_element(By.XPATH, '//*[@id="username"]')
        password_box = driver.find_element(By.XPATH, '//*[@id="password"]')
        username_box.send_keys(self.username)
        password_box.send_keys(self.password)
        driver.find_element(By.XPATH, '//*[@id="school-login"]').click()  # 移动登录
        # driver.find_element(By.XPATH, '//*[@id="ctcc-login"]').click()  # 电信登录
        time.sleep(3)
        driver.quit()
        return

    def _login(self):
        """
        登录网络
        :return: 成功返回True 失败返回 False
        """
        i = 1
        while i <= config.retry:
            self.logger.info("Start trying times: {}".format(i))
            self._login_srun()
            time.sleep(5)
            status = self._check_network()
            if status:
                self.logger.info("Login success")
                return True
            else:
                i += 1
                time.sleep(10)  # 等10秒再尝试
        if i > config.retry:
            self.logger.warning("Out of trying times")
            raise Exception("Out of trying times")

    def start(self):
        self.logger.info("Start watching network status")
        while True:
            # check是否掉线
            self.logger.info("Checking network")
            if self._check_network():
                self.logger.info("Network is good")
            else:
                self.logger.info("Network is disconnected. Try login now.")
                self._login()  # 重新登录
            time.sleep(config.check_time)


if __name__ == "__main__":
    login = AutoLogin(config.username, config.passowrd)
    login.start()
