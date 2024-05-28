import shutil


def whereis(program):
    path = shutil.which(program)
    if path:
        return path
    else:
        return f"{program} not found"


# 示例用法
print(whereis("google-chrome"))
print(whereis("chromedriver"))
