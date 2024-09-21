import datetime


def hh_mm_ss_to_s(time_str: str):
    if time_str is None:
        return None
    parts = time_str.split(':')
    if len(parts) != 3:
        raise ValueError("Invalid time string format")

    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])

    total_seconds = hours * 3600 + minutes * 60 + seconds

    return total_seconds


class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.process_result = {}
        self.write_result = []

    def exec(self):
        for class_name, class_grades in self.data.items():
            for student_info in class_grades:
                student_data = self.process_student(student_info)
                self.process_result[student_info['student_number']] = student_data
                student_write_data = {
                    # 去掉姓名和学号
                    # 'student_name': student_info['student_name'],
                    # 'student_number': student_info['student_number'],
                }
                for i in range(len(student_data[1])):
                    if student_data[1][i+1] is not None:
                        student_write_data['feature'+str(i*3+1)] = int(student_data[1][i+1])
                    else:
                        student_write_data['feature'+str(i*3+1)] = None

                    if student_data[0][i+1] is not None:
                        student_write_data['feature'+str(i*3+2)] = student_data[0][i+1]
                    else:
                        student_write_data['feature'+str(i*3+2)] = None

                    if i in (0,1,6,7,8):
                        student_write_data['feature'+str(i*3+3)] = 1
                    elif i in (2,3,9,10,11):
                        student_write_data['feature' + str(i*3+3)] = 2
                    elif i in (4,5,12,13,14):
                        student_write_data['feature' + str(i*3+3)] = 3
                # 总分
                student_write_data['feature46'] = student_info['student_score']
                # 总时长
                student_write_data['feature47'] = hh_mm_ss_to_s(student_data[2])
                # 初始化未作弊
                student_write_data['feature48'] = 'N'

                self.write_result.append(student_write_data)


    # 每道题的用时, 正确与否, 总时长
    def process_student(self, student_info):
        answer_time = student_info['answer_time']
        if not student_info['is_finish']:
            return {}, {}, None
        # 总时长 分钟 HH:SS
        total_time = answer_time[len(answer_time) - 1]
        del answer_time[len(answer_time) - 1]

        for idx, idx_time in answer_time.items():
            if idx_time['time'] is not None:
                idx_time['time'] = datetime.datetime.strptime(idx_time['time'], '%Y-%m-%d %H:%M:%S').timestamp()

        sorted_dict={}
        sorted_temp = sorted(map(lambda x: (x[1]['time'] is None, x[1]['time'],x),answer_time.items()))
        for item in sorted_temp:
            sorted_dict[item[2][0]] = item[2][1]

        time_use={}
        correct={}

        prev = None
        for key, value in sorted_dict.items():
            if prev is None:
                prev = key
                continue
            if value['time'] is not None and sorted_dict[prev]['time'] is not None:
                time_use[int(key)] = value['time'] - sorted_dict[prev]['time']
            else:
                time_use[int(key)] = None
            correct[int(key)] = value['is_correct']
            prev = key

        return time_use, correct, total_time
