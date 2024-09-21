import pandas as pd

class DataWriter:

    def __init__(self, data):
        self.data = data
        self.df_data = {}

    def write(self):
        col_titles = map(lambda x : x[0], self.data[0].items())
        for col_title in col_titles:
            col_data = []
            for line in self.data:
                if col_title in line:
                    col_data.append(line[col_title])
                else:
                    col_data.append(None)

            self.df_data[col_title] = col_data

        df = pd.DataFrame(self.df_data)  # 创建DataFrame
        df.to_excel("result.xlsx", index=False)  # 存表，去除原始索引列（0,1,2...）

