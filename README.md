# 哔哩哔哩电影爬虫

Bilibili Video: https://www.bilibili.com/video/BV1Aw4m127m9

这个 Python 脚本可以帮助你从哔哩哔哩上爬取高评分的电影并进行下载。

即将推出对于网易云音乐歌单的爬取

## 使用方法

1. **配置：**

   - 在运行脚本之前，请确保配置好 `config.json` 文件：
     - `sorce`: 下载电影的最低评分要求。   （调为8下载所有）
     - `save_path`: 下载的电影保存路径。
     - `qn`: 视频质量（参考分辨率对照表）。
     - `chunk_size`: 下载数据块的大小。
     - `headers`: 请求所需的 HTTP 头部信息。

2. **运行脚本：**
   - `git clone https://github.com/Heartestrella/Bmovie_down.git`
   - 执行 `pip3 install -r packages.txt` 安装依赖
   - 执行 `python main.py` 来运行脚本。
   - 脚本会自动从哔哩哔哩上爬取高评分的电影信息。
   - Linux amd64 和 Windwos10以上 amd64可以到发行页下载可执行文件，其余版本请运行脚本
4. **下载电影：**

   - 爬取完电影信息后，脚本会展示高评分电影列表。
   - 输入 'Y' 或 'YES' 确认要下载的电影。
   - 输入相应的分辨率代码以选择下载的视频质量（留空则使用配置文件中的默认值）。
   - 电影将会下载到指定的 `save_path`。

## 分辨率对照表

- 在下载时，可参考以下分辨率代码：
{

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

## 依赖项

- Python 3.x
- BeautifulSoup
- tqdm
- requests
- selenium（已支持Linux amd64）

## 注意事项

- 建议修改配置文件中的use_webdriver为true(默认值)
- 若您使用的机型为非Linux amd64，请调整为false
- 需要在非64位的主机上获取更多电影可以设置config.json中的html_path，html文件会在支持的Windows平台上运行后生成
- 切勿将multithreading调为true，否则下载的视频不完整(完全不能看)
  
## 免责声明

- 本脚本仅用于学习和研究目的。
- 使用本脚本下载的视频内容需遵守哔哩哔哩网站的相关规定和法律法规。
- 任何使用本脚本导致的版权纠纷或其他法律问题均与脚本作者无关。
- 使用本脚本所造成的一切后果由用户自行承担。

作者不对本脚本的误用、滥用或非法使用负责。

## 问题

![image](https://github.com/Heartestrella/Downlaod-movie/assets/110215026/6548cf52-4438-4f06-a49b-03463011ee03)

1.部分影片可能存在要付费购买的问题导致只有6分钟

2.其他问题可以查看分支

## 更新

Version 1.3.0:
1. 支持扫码自动获取Cookie
2. 支持自定义获取电影CD的功能
   
Version 1.4.0:
1. 添加了对Linux的Selenium模拟请求支持

Version 1.5.0:
1. 添加了多线程下载(没法用)
2. 修改了项目结构



## 感谢

特别感谢 [Bilibili Downloader CLI](https://github.com/open17/Bilibili-Downloader-Cli) 项目提供的灵感和参考。
