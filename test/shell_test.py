# import subprocess

# # 执行命令
# result = subprocess.run("chromedriver --version", shell=True, capture_output=True, text=True)

# # 输出命令结果
# output = result.stdout
# print(output)

import os

cpu_count = os.cpu_count()
print(f"CPU 核心数: {cpu_count}")
