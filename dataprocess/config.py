class Config:
    def __init__(self, url, exam_name):
        self.url = url
        self.exam_name = exam_name


AppConfig = Config(
    url = "https://www.yuketang.cn/v2/web/index",
    exam_name = "7.2后测"
)