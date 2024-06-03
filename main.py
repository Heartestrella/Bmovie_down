import json
import os
import re
import sys
import time

from tools import Movies, login, login163, scrape


def load_config():
    data = {
        "sleep_time": 10,
        "html_path": "",
        "sorce": 9.5,
        "save_path": "",
        "qn": 120,
        "chunk_size": 1024,
        "headers": {
            "authority": "api.vc.bilibili.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://message.bilibili.com",
            "referer": "https://message.bilibili.com/",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81",
        },
        "cookies": {},
        "163_coolies": {},
        "use_webdriver": True,
        "multithreading": False,
        "pages": 20,
    }
    config_file = "config.json"

    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            data = json.load(f)
            return data
    else:
        with open(config_file, "w") as f:
            json.dump(data, f, indent=4)
            print("配置文件初始化完毕，请手动修改某些数值")
            sys.exit()


if __name__ == "__main__":
    config = load_config()
    if not config["cookies"]:
        cookies = login.Login()
        cookies = cookies.get_cookies()
        config["cookies"] = cookies
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

    # if not config["163_coolies"]:
    #     cookies = login163.CloudMusicLogin(config)
    #     session = cookies.login()
    #     cookies.islogin(session)

    movies = scrape.BilibiliMovieScraper("https://www.bilibili.com/movie/", config)
    movies = movies.get_moive()
    Downloader_ = Movies.Downloader_movie(config, config["cookies"])
    sleep_time = config["sleep_time"]
    for movie in movies:
        for name, values in movie.items():
            match = re.search(r"/ep(\d+)", values[0])
            if match:
                target = match.group(1)
                if Downloader_.get_epid_video(target, name):
                    print(
                        f"电影 {name} 下载完成! 休眠：{sleep_time} 后继续下载下一部电影"
                    )
                    time.sleep(sleep_time)
                else:
                    print(f"电影")
            else:
                print("没匹配到id")
