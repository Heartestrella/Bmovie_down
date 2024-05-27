import subprocess

# 执行命令
result = subprocess.run("chromedriver --version", shell=True, capture_output=True, text=True)

# 输出命令结果
output = result.stdout
print(output)
