from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

class DataFetcher:
    def __init__(self, config):
        self.config = config
        if sys.platform.startswith("win32"):
            self.driver = webdriver.Edge()
        elif sys.platform.startswith("darwin"):
            self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(config.url)
        time.sleep(10)
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.get(config.url)
        self.fetched_data = {}

    def reload(self):
        self.driver.get(self.config.url)

    def close(self):
        self.driver.close()

    def exec(self):
        self._exec(0)

    def _exec(self, lesson_index):
        lessons = self.driver.find_elements("class name", "lesson-cardT")
        if lesson_index > len(lessons) - 1:
            return
        lesson_title = lessons[lesson_index].find_element("class name", "top").find_element("tag name", "h1").text
        if lesson_title not in self.fetched_data:
            self.exec_lesson(lessons[lesson_index], lesson_title)
            self.reload()
            self._exec(lesson_index + 1)


    def exec_lesson(self, lesson: WebElement, lesson_title: str):
        # 保存当前的窗口
        window_handle_main = self.driver.current_window_handle

        # 点击进课程详情
        lesson.click()
        WebDriverWait(self.driver, 50).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "el-radio-button__inner")))
        actions = self.driver.find_elements("class name", "el-radio-button__inner")
        for action in actions:
            if action.text == "试卷":
                action.click()
                time.sleep(1)
                break

        WebDriverWait(self.driver, 50).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "activity-info")))
        activities = self.driver.find_elements("class name", "activity-info")

        for activity in activities:
            if activity.find_element("tag name", "h2").text.__contains__(self.config.exam_name):
                activity.click()
                time.sleep(1)
                break

        students_grade = []
        while True:
            current_page_rows = self.driver.find_elements("class name", "el-table__row")
            for current_page_row in current_page_rows:
                student_name = current_page_row.find_element(By.CSS_SELECTOR,
                                                             ".el-table_1_column_2.is-center.el-table__cell").find_element(
                    "class name", "cell").text
                student_number = current_page_row.find_element(By.CSS_SELECTOR,
                                                               ".el-table_1_column_4.is-center.el-table__cell").find_element(
                    "class name", "cell").text
                student_score = current_page_row.find_element(By.CSS_SELECTOR,
                                                              ".el-table_1_column_6.is-center.el-table__cell").find_element(
                    "class name", "cell").text
                student_detail_btn = current_page_row.find_element(By.CSS_SELECTOR, ".el-table_1_column_7.is-center.el-table__cell").find_element("tag name", "span")
                # 如果按钮不可用(学生没有提交)
                if student_detail_btn.get_attribute("style").__contains__("no-drop"):
                    students_grade.append({
                        'student_name': student_name,
                        'student_number': student_number,
                        'student_score': None,
                        'is_finish': False,
                        'answer_time': {}
                    })
                    continue
                # 这里打开了新窗口
                student_detail_btn.click()
                time.sleep(2)

                # 切换到新窗口句柄
                for handle in self.driver.window_handles:
                    if handle != window_handle_main:
                        self.driver.switch_to.window(handle)
                        # 每次打开一个新窗口
                        break

                students_grade.append({
                    'student_name': student_name,
                    'student_number': student_number,
                    'student_score': student_score,
                    'is_finish': True,
                    'answer_time': self.exec_student()
                })
                # 关闭打开的新窗口
                for handle in self.driver.window_handles:
                    if handle != window_handle_main:
                        self.driver.close()
                        # 每次关闭一个新窗口
                        break
                self.driver.switch_to.window(window_handle_main)

            btn = self.driver.find_element("id", "examdetail").find_element("class name", "btn-next")
            if btn.get_attribute("disabled") == None:
                btn.click()
                # 主动等待有什么bug一直调试不好,由于时间紧急就先用sleep强制等待
                time.sleep(1)
            else:
                break
        self.fetched_data[lesson_title] = students_grade

    def exec_student(self):
        # 构建答题卡
        answer_card = {}
        cards = self.driver.find_elements(By.CSS_SELECTOR,".subject-item.primary")
        for card in cards:
            if card.text.__contains__("\n") or card.text.__contains__("未答"):
                answer_card[card.text.replace(" ", "").replace("\n","").replace("未答","")] = None
                continue
            try:
                card.find_element(By.CSS_SELECTOR, ".dot.dot-success")
                is_correct = True
            except:
                try:
                    card.find_element(By.CSS_SELECTOR, ".dot.dot-danger")
                    is_correct = False
                except:
                    is_correct = None
            answer_card[card.text.replace(" ","")] = is_correct

        ans_cost = {}
        index = 0
        ans_start = self.driver.find_element(By.CLASS_NAME, "show-details").find_element(By.TAG_NAME, "li").text
        ans_cost[index] = {'time': ans_start[8:27]}
        index += 1
        time_total = self.driver.find_element(By.CSS_SELECTOR, ".list-inline.head-time").find_element(By.CLASS_NAME,"time-result")
        time_ps = self.driver.find_elements(By.CLASS_NAME, "item-type")
        # 总时长放在前面
        time_ps.insert(0, time_total)
        # time_ps里第一个(总耗时)需要剔除,
        for idx, time_p in enumerate(time_ps):
            if idx == 0:
                ans_cost[len(answer_card) + 1] = time_p.text
            else:
                num_str = time_p.text
                if num_str.__contains__("最后作答时间"):
                    num = num_str[0:len(num_str)-40]
                else:
                    num = num_str[0:len(num_str)-9]
                # 题目未作答
                if answer_card[str(num)] is None:
                    ans_cost[index] = {
                        'time': None,
                        'is_correct': None
                    }
                    index += 1
                    continue

                span = time_p.find_element(By.CLASS_NAME, "time-result").find_element(By.TAG_NAME, "span").text
                ans_cost[index] = {
                    'time': span.replace("'",""),
                    'is_correct':answer_card[str(index)]
                }
                index += 1
        return ans_cost