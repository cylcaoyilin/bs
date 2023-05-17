import math
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, log, sqrt
import os
os.environ['JAVA_HOME']='/export/server/jdk1.8.0_241'

class ItemCf:
    def __init__(self, data):
        #data:所有用户的数据
        # data = {
        #     'user1': {'item425': 4, 'item431': 4, 'item438': 4, 'item427': 4, 'item442': 4},
        #     'user_1': {'item4': 4},
        #     'user_2': {'item424': 4, 'item425': 4},
        # }
        print("调用item")
        self.data = data
        self.item_similarity = self.calculate_item_similarity()

    def calculate_item_similarity(self):
        item_similarity = {}
        item_counts = {}

        for user_ratings in self.data.values():
            for item in user_ratings:
                if item not in item_counts:
                    item_counts[item] = 0
                item_counts[item] += 1
        print("item_counts：",item_counts)
        for user_ratings in self.data.values():
            for item1 in user_ratings:
                if item1 not in item_similarity:
                    item_similarity[item1] = {}
                for item2 in user_ratings:
                    if item1 != item2:
                        if item2 not in item_similarity[item1]:
                            item_similarity[item1][item2] = 0
                        item_similarity[item1][item2] += 1 / math.log(1 + item_counts[item2])
        print("item_similarity1:",item_similarity)
        for item1 in item_similarity:
            for item2 in item_similarity[item1]:
                item_similarity[item1][item2] /= math.sqrt(item_counts[item1] * item_counts[item2])
        print("item_similarity2:",item_similarity)
        return item_similarity

    def recommend(self, user, num_recommendations=10):
        user_ratings = self.data[user]
        scores = {}

        for item1 in user_ratings:
            for item2 in self.item_similarity[item1]:
                if item2 not in user_ratings:
                    if item2 not in scores:
                        scores[item2] = 0
                    scores[item2] += user_ratings[item1] * self.item_similarity[item1][item2]
        print("scores:",scores)

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        recommendations = sorted_scores[:num_recommendations]

        return recommendations

    def get_item_similarity(self):
        return self.item_similarity


if __name__ == '__main__':
    # 示例数据
    # data = {
    #     'user1': {'item1': 5, 'item2': 1, 'item3': 2},
    #     'user2': {'item1': 4, 'item2': 2},
    #     'user3': {'item1': 4, 'item2': 2},
    #     'user4': {'item1': 2, 'item2': 5, 'item4': 4},
    # }
    data = {
            'user1': {'item425': 4, 'item431': 4, 'item438': 4,'item427': 4,'item442': 4},
            'user_1': {'item4': 4,'item425': 4},
            'user_2': {'item424': 4, 'item425': 4},
            # 'user_3': {'item1': 4, 'item3': 4},
            # 'user_4': {'item1': 4, 'item3': 4, 'item4': 4},
            # 'user_5': {'item3': 4, 'item4': 4},
        }

    spark = SparkSession.builder.getOrCreate()
    itemBasedCF = ItemCf(data)
    recommendations = itemBasedCF.recommend('user1')
    print("Recommendations:", recommendations)

    item_similarity = itemBasedCF.get_item_similarity()
    print("\nItem Similarity:")
    for item1 in item_similarity:
        for item2 in item_similarity[item1]:
            similarity = item_similarity[item1][item2]
            print(f"Similarity between {item1} and {item2}: {similarity}")


