import os
import platform
import subprocess
import time

import requests
from bs4 import BeautifulSoup


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
            # downlaod = Downloader(self.config)
            # for data in self.wait_download_moives:
            #     for name, values in data.items():
            #         match = re.search(r"/ep(\d+)", values[0])
            #         if match:
            #             target = match.group(1)
            #             id = f"ep{target}"
            #             if downlaod.get_epid_video(id, name):
            #                 print(f"已经完成 {name}的下载 30s后自动下载")
            #             # time.sleep(3)
            #         else:
            #             print("没匹配到id")


class get_full_page:
    def __init__(self, url) -> None:
        self.url = url

    def get_package_manager(self):
        try:
            subprocess.run(
                ["apt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            return "apt"
        except FileNotFoundError:
            pass
        try:
            subprocess.run(
                ["yum"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            return "yum"
        except FileNotFoundError:
            pass

        return "Unknown package manager"

    def get_page(self, driver: str):
        from selenium import webdriver

        if driver == "Edge":
            self.driver = webdriver.Edge()
        elif driver == "Chrome":
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=options)
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

        if platform.system() == "Linux":
            if config["use_webdriver"]:
                print("将在Linux上使用Webdriver模拟请求")
                #try:
                output  = subprocess.run("chromedriver --version", shell=True, capture_output=True, text=True).stdout
                print(output)
                if "command not found" not in output:
                    return self.get_page("Chrome")
                else:
                    print(
                        "尝试自动安装，若安装失败，请参考：https://github.com/Heartestrella/Downlaod-movie 安装方法"
                    )
                    package_manager = self.get_package_manager()
                    full_path_driver = os.path.join(
                        os.getcwd(), "driver", "google-chrome-stable_current_amd64.deb"
                    )
                    if package_manager == "apt":
                        os.system("sudo apt install {}".format(full_path_driver))
                    elif package_manager == "yum":
                        os.system("rpm -ivh {}".format(full_path_driver))
                    print("安装完成,请重新启动")
                #except FileNotFoundError:
               #     if "command not found" in output:
                        

                    
            else:
                resp = requests.get(url=self.url, headers=config["headers"])
                if resp.status_code == 200:
                    page_content = resp.text
                    return page_content
                else:
                    raise RuntimeError("无法获取到页面，请检查网络")
