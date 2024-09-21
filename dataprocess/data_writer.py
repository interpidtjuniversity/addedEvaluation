import pandas as pd


def min_max(array):
    _min, _max = float(array[0]), float(array[0])
    for item in array:
        if item is not None:
            item_int = float(item)
            if item_int < _min:
                _min = item_int
            if item_int > _max:
                _max = item_int
    return _min, _max


def need_normalization(col_title):
    idx = int(col_title[7:])
    if idx ==46 or idx % 3 == 2:
        return True
    return False


class DataWriter:

    def __init__(self, config, data):
        self.data = data
        self.config = config
        self.df_data = {}

    # 答题时间,总分数,总时间 需要归一化
    def write(self):
        col_titles = map(lambda x : x[0], self.data[0].items())
        for col_title in col_titles:
            col_data = []
            for line in self.data:
                if col_title in line:
                    col_data.append(line[col_title])
                else:
                    col_data.append(None)

            # 需要归一化的列
            if need_normalization(col_title):
                _min, _max = min_max(col_data)
                for i in range(len(col_data)):
                    if col_data[i] is not None:
                        col_data[i] = (float(col_data[i]) - _min) / (_max - _min)
            self.df_data[col_title] = col_data

        df = pd.DataFrame(self.df_data)  # 创建DataFrame
        df.to_excel(self.config.exam_name + ".xlsx", index=False)  # 存表，去除原始索引列（0,1,2...）

