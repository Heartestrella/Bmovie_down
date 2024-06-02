import os
import requests
import threading

class Multithreading:
    def __init__(self,session:requests.Session ,num_threads: int = 0,) -> None:
        """
        初始化多线程下载器
        :param num_threads: 多线程下载的线程数，不输入时为 CPU 核心数的两倍
        """
        if num_threads == 0:
            cpu_count = os.cpu_count()
            self.num_threads = cpu_count * 2
        else:
            self.num_threads = num_threads
            
        self.session = session
    def single_thread_download(self, url: str, file_name: str) -> None:
        """
        单线程下载文件
        :param url: 文件下载 URL
        :param file_name: 保存文件名
        """
        response = self.session.get(url, stream=True)
        file_size = int(response.headers.get("content-length", 0))
        chunk_size = 1024
        
        with open(file_name, "wb") as file:
            downloaded = 0
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                downloaded += len(data)
                percentage = (downloaded / file_size) * 100
                print(f"\rDownloading: {percentage:.2f}%", end="")
        print("\nDownload complete!")

    def download_part(self, url: str, start: int, end: int, file_name: str, part_num: int, hidden_folder: str, chunk_size=1024) -> None:
        """
        下载文件的一部分
        :param url: 文件下载 URL
        :param start: 分块开始位置
        :param end: 分块结束位置
        :param file_name: 保存文件名
        :param part_num: 分块编号
        :param hidden_folder: 存储分块文件的隐藏文件夹
        :param chunk_size: 分块大小
        """
        headers = {"Range": f"bytes={start}-{end}"}
        response = self.session.get(url, headers=headers, stream=True)
        part_file_name = os.path.join(hidden_folder, f"{file_name}.part{part_num}")
        file_size = end - start + 1
        downloaded = 0

        with open(part_file_name, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                downloaded += len(data)
                percentage = (downloaded / file_size) * 100
                print(f"\rPart {part_num}: {percentage:.2f}%", end="")
        print(f"\nPart {part_num} download complete!")

    def merge_files(self, file_name: str, hidden_folder: str, num_parts: int) -> None:
        """
        合并分块文件
        :param file_name: 合并后的文件名
        :param hidden_folder: 存储分块文件的隐藏文件夹
        :param num_parts: 分块数量
        """
        with open(file_name, "wb") as merged_file:
            for i in range(num_parts):
                part_file_name = os.path.join(hidden_folder, f"{file_name}.part{i}")
                with open(part_file_name, "rb") as part_file:
                    merged_file.write(part_file.read())
                os.remove(part_file_name)
        os.rmdir(hidden_folder)

    def multi_thread_download(self, url: str, file_name: str) -> None:
        """
        多线程下载文件
        :param url: 文件下载 URL
        :param file_name: 保存文件名
        """
        response = self.session.head(url, stream=True)
        file_size = int(response.headers.get("content-length", 0))
        part_size = file_size // self.num_threads

        hidden_folder = f".{file_name}_parts"
        os.makedirs(hidden_folder, exist_ok=True)
        
        threads = []
        for i in range(self.num_threads):
            start = i * part_size
            end = start + part_size - 1 if i < self.num_threads - 1 else file_size - 1
            thread = threading.Thread(target=self.download_part, args=(url, start, end, file_name, i, hidden_folder))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.merge_files(file_name, hidden_folder, self.num_threads)

    def download(self, url: str, file_name: str, multi_thread: bool = True) -> None:
        """
        根据选择使用单线程或多线程下载文件
        :param url: 文件下载 URL
        :param file_name: 保存文件名
        :param multi_thread: 是否使用多线程下载，默认为 True
        """
        if multi_thread:
            self.multi_thread_download(url, file_name)
        else:
            self.single_thread_download(url, file_name)