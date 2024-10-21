class Config:
    def __init__(self, url, exam_name, per_student_wait_time, remove_none_line = True, remove_student_name_and_number = False):
        self.url = url
        self.exam_name = exam_name
        self.per_student_wait_time = per_student_wait_time
        # 去除未答题的学生
        self.remove_none_line = remove_none_line
        # 去除姓名和学号
        self.remove_student_name_and_number = remove_student_name_and_number



AppConfig = Config(
    url = "https://www.yuketang.cn/v2/web/index",
    exam_name = "15.7前测",
    # 每次点开学生答题详情后需要等待的时间, 取决于网络情况和服务器状态, 找不到页面标签元素时可以稍微增加时长
    per_student_wait_time = 2.5
)