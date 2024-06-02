import os
import platform
import shutil
import subprocess
import time

import requests
from bs4 import BeautifulSoup

from .download import Download


class BilibiliMovieScraper:
    def __init__(self, url, config):
        """{
            "240P 极速": 6,
            "360P 流畅": 16,
            "480P 清晰": 32,
            "720P 高清": 64,
            "720P60 高帧率": 74,
            "1080P 高清": 80,
            "1080P+ 高码率": 112,
            "1080P60 高帧率": 116,
            "4K 超清": 120
        }
        """
        self.config = config
        #  self.headers = headers
        self.movie_info = []
        full_page = get_full_page(url)
        if self.config["html_path"]:
            print("使用手动指定的HTML路径解析...")
            with open(self.config["html_path"], encoding="utf-8") as f:
                self.page_content = f.read()
        else:
            self.page_content = full_page.main(config)
            open("full_page.html", encoding="utf-8", mode="a").write(self.page_content)
        self.scrape_movie_info()

    def scrape_movie_info(self):
        # response = httpx.get(self.url, headers=self.headers)

        # soup = BeautifulSoup(response.text, "html.parser")
        soup = BeautifulSoup(self.page_content, "html.parser")

        target_divs = soup.find_all("div", class_="module inner-c web_feed_v2")

        for div in target_divs:
            hover_c_divs = div.find_all("div", class_="hover-c")

            for hover_c_div in hover_c_divs:
                title_div = hover_c_div.find("div", class_="title")
                if title_div:
                    movie_name = title_div.get_text(strip=True)

                    a_tag = hover_c_div.find("a", {"target": "_blank"})

                    if a_tag:
                        a_href = a_tag["href"]
                    else:
                        a_href = "N/A"

                    img_tags = hover_c_div.find_all("img")
                    if img_tags:
                        img_src = img_tags[0]["src"]
                    else:
                        img_src = "N/A"

                    score_tags = hover_c_div.find_all("div", class_="score")
                    if score_tags:
                        for score_tag in score_tags:
                            score = score_tag.get_text(strip=True)
                    else:
                        score = "N/A"

                    self.movie_info.append(
                        {
                            movie_name: [a_href, img_src, score]
                        },  # 电影名 : 电影播放地址 图片地址 分数
                    )

    def get_moive(self):
        print("所有电影:\n")
        self.wait_download_moives = []
        for info in self.movie_info:
            sorce = list(info.values())[-1][-1]
            if sorce == "N/A":
                print(f"电影{list(info.keys())[0]},无法获取到分数")
            elif float(sorce) >= float(self.config["sorce"]):  # 只下载高分电影
                self.wait_download_moives.append(info)
        print("将要下载的电影:\n")
        for movie_info in self.wait_download_moives:
            movie_name = list(movie_info.keys())[0]
            print(f"{movie_name}\n")
        result = input(f"确定下载吗？ Y/YES : ").upper()
        print(f"{self.config['save_path']} 电影将保存到此")
        if result == "Y" or result == "YES":
            print(f"分辨率: {self.config['qn']} 即将开始下载")
            return self.wait_download_moives

class get_full_page:
    def __init__(self, url) -> None:
        self.url = url
        self.download = Download()

    def get_package_manager(self):
        package_managers = ["apt", "yum"]

        for package_manager in package_managers:
            try:
                # 尝试执行命令并捕获标准输出
                result = subprocess.run(
                    [package_manager, "--version"], capture_output=True, text=True
                )

                if result.returncode == 0:
                    return package_manager
            except FileNotFoundError:
                pass
        return "Unknown package manager"

    def whereis(self, program) -> str:
        path = shutil.which(program)
        if path:
            return path
        else:
            return f"{program} not found"

    def get_page(self, driver: str):
        from selenium import webdriver

        if driver == "requests":
            resp = requests.get(url=self.url, headers=self.config["headers"])
            if resp.status_code == 200:
                page_content = resp.text
                return page_content
            else:
                raise ConnectionError("无法获取到页面，请检查网络")
        else:
            if driver == "Edge":
                self.driver = webdriver.Edge()
            elif driver == "Chrome":
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.chrome.service import Service

                options = Options()
                options.add_argument("--headless")
                options.binary_location = self.google_chrome
                self.chromedriver = os.path.join(os.getcwd(), "driver", "chromedriver")
                os.system("sudo chmod +x {}".format(self.chromedriver))
                self.driver = webdriver.Chrome(
                    options=options, service=Service(self.chromedriver)
                )
            else:
                RuntimeError("未知的浏览器")
            self.driver.get(self.url)
            for i in range(10):
                self.driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(3)

            page_content = self.driver.page_source
            self.driver.quit()

            return page_content

    def main(self, config) -> str:
        if platform.system() == "Windows":
            return self.get_page("Edge")
        self.config = config
        if platform.system() == "Linux":
            if config["use_webdriver"]:
                machine = platform.machine()
                if machine == "x86_64":
                    print("将在Linux上使用Webdriver模拟请求")
                    full_path_driver = os.path.join(
                            os.getcwd(),
                            "driver",
                            "chrome",
                        )
                    full_path = os.path.join(os.getcwd(),"driver")
                    package_manager = self.get_package_manager()
                    if not (os.path.exists(full_path) and os.path.isdir(full_path)):
                        suffix = self.download.start(package_manager)
                    self.google_chrome = self.whereis("google-chrome")
                    if "not found" not in self.google_chrome:
                        return self.get_page("Chrome")
                    else:
                        print(
                            "尝试自动安装，若安装失败，请参考：https://github.com/Heartestrella/Downlaod-movie 安装方法"
                        )
                        
                        if package_manager == "apt":
                            os.system(
                                "sudo apt install {}.{} -y  --allow-downgrades".format(
                                    full_path_driver,suffix
                                )
                            )
                        elif package_manager == "yum":
                            os.system("sudo rpm -i  {}.{} -y ".format(full_path_driver,suffix))
                        print("安装完成,请重新启动")
                        exit()
                else:
                    print("非X86架构不支持Webdriver模拟请求")
                    print("继续使用requests请求,获取的页面受限")
                    return self.get_page("requests")
            else:
                return self.get_page("requests")