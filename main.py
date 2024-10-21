from dataconstruct.data_fetcher import DataFetcher
from dataconstruct.config import AppConfig
from dataconstruct.data_processor import DataProcessor
from dataconstruct.data_writer import DataWriter

# 获取数据
data_fetcher = DataFetcher(AppConfig)
data_fetcher.exec()
data_fetcher.close()
# 处理数据
data_processor = DataProcessor(AppConfig, data_fetcher.fetched_data)
data_processor.exec()

#写数据
data_writer = DataWriter(AppConfig, data_processor.write_result)
data_writer.write()