import os

import requests
from tqdm import tqdm


class Download:
    def __init__(self) -> None:
        self.driver_url = "https://github.com/Heartestrella/Bmovie_down/releases/download/Chrome_Driver_V_99/chromedriver"
        self.chrome_apt = "https://github.com/Heartestrella/Bmovie_down/releases/download/Chrome_Driver_V_99/google-chrome-stable_current_amd64.deb"
        self.chrome_yum = "https://github.com/Heartestrella/Bmovie_down/releases/download/Chrome_Driver_V_99/google-chrome-stable_current_x86_64.rpm"

    def download_file(self, url: str, file_path: str):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))

        with open(file_path, mode="wb") as f:
            with tqdm(
                total=total_size, unit="B", unit_scale=True, unit_divisor=1024
            ) as pbar:
                for data in response.iter_content(chunk_size=1024):
                    f.write(data)
                    pbar.update(len(data))

    def start(self, manager: str):
        print("开始下载Google Drvier Version 99")
        os.makedirs("driver", exist_ok=True)
        self.download_file(
            self.driver_url, os.path.join(os.getcwd(), "driver", "chromedriver")
        )
        if manager == "apt":
            url = self.chrome_apt
        elif manager == "yum":
            url = self.chrome_yum
        print("开始下载Google Chrome")
        self.download_file(url, os.path.join(os.getcwd(), "driver", "chrome"))
        print("下载完成")
