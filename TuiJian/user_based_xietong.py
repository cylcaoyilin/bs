from math import sqrt,pow
import operator
import math
from pyspark.sql import SparkSession
import os
os.environ['JAVA_HOME']='/export/server/jdk1.8.0_241'

class UserCf():
    def __init__(self,data):
        self.data=data
        print("调用user")

    def getUsers(self,username1,username2):
        return self.data[username1],self.data[username2]

    def Euclidean(self,user1, user2):
        # 取出两位用户评论过的短视频和评分
        user1_data = self.data[user1]
        user2_data = self.data[user2]

        # print("user1_data:",user1_data)
        # print("user2_data:",user2_data)

        fm = sqrt(sum([ i*i for i in user1_data.values()]))*sqrt(sum([ i*i for i in user2_data.values()]))
        fz = 0
        for key in user1_data.keys():
            if key in user2_data.keys():
                fz += user1_data[key]*user2_data[key]

        if fm > 0:
            return fz/fm

        return 0


# 计算某个用户与其他用户的相似度
    def top10_simliar(self,userID):
        res = []
        for userid in self.data.keys():
            # 排除与自己计算相似度
            if not userid == userID:
                simliar = self.Euclidean(userID, userid)
                res.append((userid, simliar))
        res.sort(key=lambda val: val[1],reverse=True)
        return res[:10]

# 根据用户推荐短视频给其他人
    def recommend(self,user):
        # 相似度最高的用户
        print("\n用户-用户相似度:")
        print(self.top10_simliar(user))
        top_sim_user = self.top10_simliar(user)[0][0]
        print("相似度最高的用户：",top_sim_user)
        # 相似度最高的用户的观影记录
        items = self.data[top_sim_user]
        recommendations = []
        # 筛选出该用户未观看的短视频并添加到列表中
        for item in items.keys():
            if item not in self.data[user].keys():
                recommendations.append((item, items[item]))
        recommendations.sort(key=lambda val: val[1], reverse=True)  # 按照评分排序
        # 返回全部排序好的短视频
        return recommendations


  # 输出用户-物品评分矩阵
    def ratingMatrix(self):
        users = list(self.data.keys())
        # print("users:",users)
        items = list(set([item for user in self.data.values() for item in user.keys()]))
        # print("items:",items)  3 1 4 5 2
        rating_matrix = [[self.data[user].get(item, 0) for item in items] for user in users]
        return rating_matrix

  # 输出用户-用户相似度矩阵
    def similarityMatrix(self):
        users = list(self.data.keys())
        similarity_matrix = [[self.Euclidean(user1, user2) for user2 in users] for user1 in users]
        return similarity_matrix

if __name__ == '__main__':
    # users = {
    #     'current_user': {'item1': 5, 'item2': 4},
    #     'user_1': {'item1': 5,'item2': 4,'item3': 5,'item4': 4},
    #     'user_2': {'item1': 4, 'item2': 2, 'item5': 5},
    #     'user_3': {'item1': 2, 'item3': 2},
    #     'user_4': {'item1': 1, 'item3': 4, 'item4': 5},
    #     'user_5': {'item3': 4, 'item4': 5},
    # }

    spark = SparkSession.builder.getOrCreate()
    users = {
        'current_user': {'item425': 4, 'item431': 4, 'item438': 4, 'item427': 4, 'item442': 4},
        'user_1': {'item4': 4},
        'user_2': {'item424': 4, 'item425': 4},
        # 'user_3': {'item1': 4, 'item3': 4},
        # 'user_4': {'item1': 4, 'item3': 4, 'item4': 4},
        # 'user_5': {'item3': 4, 'item4': 4},
    }
    userCf = UserCf(data=users)

# 用户-物品评分矩阵
    rating_matrix = userCf.ratingMatrix()
    print("用户-物品评分矩阵：")
    for row in rating_matrix:
        print(row)

# 用户-用户相似度矩阵
    similarity_matrix = userCf.similarityMatrix()
    print("\n用户-用户相似度矩阵：")
    for row in similarity_matrix:
        row_str = " ".join([f"{similarity:.2f}" for similarity in row])
        print(row_str)

    recommendations = userCf.recommend('current_user')
    print("\nrecommendations:",recommendations)
    print("推荐短视频：")
    for item in recommendations:
        print(f"短视频：{item[0]}, 评分：{item[1]}")
