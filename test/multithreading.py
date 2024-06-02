import os
import time
import requests
import threading

# 普通单线程下载文件
def single_thread_download(url, file_name):
    response = requests.get(url, stream=True)
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

# 多线程下载文件（包含之前的实现）
def download_part(url, start, end, file_name, part_num, hidden_folder, chunk_size=1024):
    headers = {"Range": f"bytes={start}-{end}"}
    response = requests.get(url, headers=headers, stream=True)
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

def merge_files(file_name, hidden_folder, num_parts):
    with open(file_name, "wb") as merged_file:
        for i in range(num_parts):
            part_file_name = os.path.join(hidden_folder, f"{file_name}.part{i}")
            with open(part_file_name, "rb") as part_file:
                merged_file.write(part_file.read())
            os.remove(part_file_name)
    os.rmdir(hidden_folder)

def multi_thread_download(url, file_name, num_threads=4):
    response = requests.head(url)
    file_size = int(response.headers.get("content-length", 0))
    part_size = file_size // num_threads

    hidden_folder = f".{file_name}_parts"
    os.makedirs(hidden_folder, exist_ok=True)
    
    threads = []
    for i in range(num_threads):
        start = i * part_size
        end = start + part_size - 1 if i < num_threads - 1 else file_size - 1
        thread = threading.Thread(target=download_part, args=(url, start, end, file_name, i, hidden_folder))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    merge_files(file_name, hidden_folder, num_threads)

# 示例URL和保存文件名
url = 'https://download2.aida64.com/aida64extreme730.exe'
file_name_single = '单线程.exe'
file_name_multi = '多线程.exe'

# 执行并比较两种下载方式的速度
# start_time = time.time()
# single_thread_download(url, file_name_single)
# end_time = time.time()
# print(f"Single-threaded download took {end_time - start_time:.2f} seconds")

start_time = time.time()
multi_thread_download(url, file_name_multi, num_threads=12)
end_time = time.time()
print(f"Multi-threaded download took {end_time - start_time:.2f} seconds")
