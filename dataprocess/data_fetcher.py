from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DataFetcher:
    def __init__(self, config):
        self.driver = webdriver.Chrome()
        self.config = config

        self.driver.maximize_window()
        self.driver.get(config.url)
        time.sleep(10)
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.get(config.url)
        self.grade = {}

    def reload(self):
        self.driver.get(self.config.url)

    def close(self):
        self.driver.close()

    def exec(self, lesson_index):
        lessons = self.driver.find_elements("class name", "lesson-cardT")
        if lesson_index > len(lessons) - 1:
            return
        lesson_title = lessons[lesson_index].find_element("class name", "top").find_element("tag name", "h1").text
        if lesson_title not in self.grade:
            self.exec_lesson(lessons[lesson_index], lesson_title)
            self.reload()
            self.exec(lesson_index + 1)


    def exec_lesson(self, lesson: WebElement, lesson_title: str):
        # 点击进课程详情
        lesson.click()
        WebDriverWait(self.driver, 50).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "el-radio-button__inner")))
        actions = self.driver.find_elements("class name", "el-radio-button__inner")
        for action in actions:
            if action.text == "试卷":
                action.click()
                break

        WebDriverWait(self.driver, 50).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "activity-info")))
        activities = self.driver.find_elements("class name", "activity-info")

        for activity in activities:
            if activity.find_element("tag name", "h2").text.__contains__(self.config.exam_name):
                activity.click()
                break

        students_grade = []
        while True:
            WebDriverWait(self.driver, 50).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "el-table__row")))
            current_page_rows = self.driver.find_elements("class name", "el-table__row")
            for current_page_row in current_page_rows:
                print(lesson_title, len(students_grade), len(current_page_rows))
                student_name = current_page_row.find_element(By.CSS_SELECTOR,
                                                             ".el-table_1_column_2.is-center.el-table__cell").find_element(
                    "class name", "cell").text
                student_number = current_page_row.find_element(By.CSS_SELECTOR,
                                                               ".el-table_1_column_4.is-center.el-table__cell").find_element(
                    "class name", "cell").text
                student_score = current_page_row.find_element(By.CSS_SELECTOR,
                                                              ".el-table_1_column_6.is-center.el-table__cell").find_element(
                    "class name", "cell").text
                print(student_name, student_number, student_score)
                students_grade.append(student_name + student_number + student_score)
                # student_detail_btn = current_page_row.find_element("class name", "el-table_1_column_7 is-center  el-table__cell").find_element("tag name", "span")
                # student_detail_btn.click()
            btn = self.driver.find_element("id", "examdetail").find_element("class name", "btn-next")
            if btn.get_attribute("disabled") == None:
                btn.click()
            else:
                break
        self.grade[lesson_title] = students_grade


