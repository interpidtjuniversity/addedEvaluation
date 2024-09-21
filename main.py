from dataprocess.data_fetcher import DataFetcher
from dataprocess.config import AppConfig


print("hello")
data_fetcher = DataFetcher(AppConfig)
data_fetcher.exec(0)
data_fetcher.close()
print(data_fetcher.grade)