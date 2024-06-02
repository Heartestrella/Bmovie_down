from requests.cookies import RequestsCookieJar
from requests.exceptions import RequestException
from tqdm import tqdm
import requests
from . import multithreading
import os
import sys
import time
class Downloader_movie:
    def __init__(self, config, cookie):
        self.config = config
        cookie_jar = RequestsCookieJar()
        cookie_jar.update(cookie)
        self.session = requests.Session()
        self.session.cookies = cookie_jar
        self.multithreading_ = multithreading.Multithreading(session=self.session)
    def get_epid_video(self, ep_id, name):
        url = f"https://api.bilibili.com/pgc/player/web/playurl?ep_id={ep_id}&qn={self.config['qn']}"
        print(url)
        response = self.session.get(url, headers=self.config["headers"],timeout=20)
        if response.status_code == 200:
            video_url = response.json()["result"]["durl"][0]["url"]
            if self.download_video(video_url, name):
                return True
        else:
            return False
    def download_video(self, url:str, name:str):
        print("开始下载 MP4，请耐心等待...")
        full_path = os.path.join(self.config["save_path"], f"{name}.mp4")
        if os.path.exists(full_path):
            print(f"电影 {name} 已经存在")
            return True
        
        if self.config['multithreading']:
            print(f"多线程下载：{name}")
            self.multithreading_.download(url,full_path)
            return True
        else:
            try:
                response = self.session.get(
                    url, headers=self.config["headers"], stream=True
                )
                if response.status_code == 200:
                    content_length = int(response.headers.get("Content-Length", 0))
                    with tqdm(
                        total=content_length,
                        unit="B",
                        unit_scale=True,
                        desc=name,
                        file=sys.stdout,
                    ) as pbar:

                        with open(full_path, "wb") as file:
                            for chunk in response.iter_content(
                                chunk_size=self.config["chunk_size"]
                            ):
                                file.write(chunk)
                                pbar.update(len(chunk))
                    print("\n下载完成")
                    return True
                else:
                    print(name, "下载失败")
                    return False
            except RequestException as e:
                print(f"出现错误 : {e} 1分钟后再次尝试!")
                os.remove(full_path)
                time.sleep(60)
                self.download_video(url, name)
