import json

import numpy as np
from tensorflow.python.keras.models import load_model
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# 加载训练好的模型
model = load_model('hotel_recommendation_model.h5')

# 加载数据和编码器
with open('data.json', 'r') as f:
    data = json.load(f)

bookings_df = pd.DataFrame(data['bookings'])
hotels_df = pd.DataFrame(data['hotels'])

# 准备编码器
username_encoder = LabelEncoder()
username_encoder.fit(bookings_df['username'])
hotel_id_encoder = LabelEncoder()
hotel_id_encoder.fit(bookings_df['hotel_id'])
room_type_encoder = LabelEncoder()
room_type_encoder.fit(bookings_df['room_type'])
hotel_window_encoder = LabelEncoder()
hotel_window_encoder.fit(bookings_df['hotel_window'])
breakfast_encoder = LabelEncoder()
breakfast_encoder.fit(bookings_df['breakfast'])

# 推荐函数
def recommend_hotels(username, room_type, hotel_window, breakfast, top_k=5):
    # 将输入特征进行编码
    username_encoded = username_encoder.transform([username])[0]
    room_type_encoded = room_type_encoder.transform([room_type])[0]
    hotel_window_encoded = hotel_window_encoder.transform([hotel_window])[0]
    breakfast_encoded = breakfast_encoder.transform([breakfast])[0]

    # 构建输入向量
    input_vector = [
        np.array([username_encoded]),
        np.array([room_type_encoded]),
        np.array([hotel_window_encoded]),
        np.array([breakfast_encoded])
    ]

    # 进行预测
    predictions = model.predict(input_vector)

    # 获取前top_k个推荐酒店
    top_k_indices = np.argsort(predictions[0])[-top_k:][::-1]
    recommended_hotels = hotel_id_encoder.inverse_transform(top_k_indices)

    return recommended_hotels

# 示例使用
username = 'user1'
room_type = 'Deluxe'
hotel_window = 'City View'
breakfast = 'Included'

recommended_hotels = recommend_hotels(username, room_type, hotel_window, breakfast)
print("推荐的酒店：", recommended_hotels)
