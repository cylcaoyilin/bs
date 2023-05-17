import os
os.environ['JAVA_HOME']='/export/server/jdk1.8.0_241'
import pandas as pd
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local").appName("Short video recommendation system").config("spark.some.config.option", "some-value").getOrCreate()
# print("ok")
filepath=r"../TuiJian/result.csv"

# 读取csv
df = spark.read.csv(filepath, sep=',', header=False, inferSchema=True)

# 去重
print("去重后的数据：")
df_distinct = df.distinct()
# 显示去重后的结果
df_distinct.show()
# 去除含有空值的行
print("去空后的数据：")
df_no_empty = df.dropna()
# 显示结果
df_no_empty.show()





