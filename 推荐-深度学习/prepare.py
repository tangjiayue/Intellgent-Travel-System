# import keras
# import pandas as pd
# import re
# import numpy as np
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split
# from tensorflow.python.keras.models import  Model
# from tensorflow.python.keras.layers import  Input,Embedding,Flatten,Concatenate,Dense,Dropout
# # 加载HotelRec数据集的示例
# data_sample = [
#     {
#         "hotel_url": "Hotel_Review-g194775-d1121769-Reviews-Hotel_Baltic-Giulianova_Province_of_Teramo_Abruzzo.html",
#         "author": "ladispoli",
#         "date": "2010-02-01T00:00:00",
#         "rating": 4.0,
#         "title": "Great customer service",
#         "text": "Great customer service and good restaurant service...",
#         "property_dict": {
#             "sleep quality": 4.0,
#             "value": 4.0,
#             "rooms": 3.0,
#             "service": 5.0,
#             "cleanliness": 3.0,
#             "location": 3.0
#         }
#     }
#     # 添加更多示例数据
# ]
#
# # 转换为DataFrame
# df = pd.DataFrame(data_sample)
#
# # 从hotel_url中提取信息
# def parse_hotel_info(hotel_url):
#     pattern = r'Hotel_Review-(?P<location>[^-]+)-(?P<hotel_id>[^-]+)-Reviews-(?P<hotel_name>[^-]+)'
#     match = re.search(pattern, hotel_url)
#     if match:
#         return match.groupdict()
#     else:
#         return {}
#
# # 应用解析函数
# df = df.join(df['hotel_url'].apply(parse_hotel_info).apply(pd.Series))
#
# # 编码用户和酒店ID
# user_encoder = LabelEncoder()
# hotel_encoder = LabelEncoder()
# df['user_id'] = user_encoder.fit_transform(df['author'])
# df['hotel_id'] = hotel_encoder.fit_transform(df['hotel_id'])
#
# # 提取评分和其他特征
# df['rating'] = df['rating'].astype(float)
# df['stay_duration'] = 1  # 假设所有评论的入住时长为1
#
# # 特征和标签
# X = df[['user_id', 'hotel_id', 'stay_duration', 'rating']]
# y = df['hotel_id']
#
# print("Features (X):\n", X.head())
# print("Labels (y):\n", y.head())
#
# # 训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# def build_model(num_users, num_hotels):
#     input_user = Input(shape=(1,))
#     input_hotel = Input(shape=(1,))
#     input_stay_duration = Input(shape=(1,))
#     input_rating = Input(shape=(1,))
#
#     embedding_user = Embedding(input_dim=num_users, output_dim=50)(input_user)
#     embedding_hotel = Embedding(input_dim=num_hotels, output_dim=50)(input_hotel)
#
#     flatten_user = Flatten()(embedding_user)
#     flatten_hotel = Flatten()(embedding_hotel)
#
#     concat = Concatenate()([flatten_user, flatten_hotel, input_stay_duration, input_rating])
#
#     dense_1 = Dense(128, activation='relu')(concat)
#     dropout_1 = Dropout(0.5)(dense_1)
#     dense_2 = Dense(64, activation='relu')(dropout_1)
#     output = Dense(num_hotels, activation='softmax')(dense_2)
#
#     model = Model(inputs=[input_user, input_hotel, input_stay_duration, input_rating], outputs=output)
#     model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
#     return model
#
# num_users = len(user_encoder.classes_)
# num_hotels = len(hotel_encoder.classes_)
#
# model = build_model(num_users, num_hotels)
#
# # 预训练模型
# model.fit(
#     [X_train['user_id'], X_train['hotel_id'], X_train['stay_duration'], X_train['rating']],
#     y_train,
#     epochs=10,
#     batch_size=32,
#     validation_split=0.2
# )
#
# # 评估预训练模型
# loss, accuracy = model.evaluate(
#     [X_test['user_id'], X_test['hotel_id'], X_test['stay_duration'], X_test['rating']],
#     y_test
# )
# print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
#
#
# # 你的实际酒店数据
# hotel_data = pd.DataFrame({
#     'hotel_id': [1, 2, 3],
#     'location': ['A', 'B', 'C'],
#     'rating': [4.5, 3.7, 4.0],
#     'type': ['luxury', 'budget', 'standard']
# })
#
# booking_data = pd.DataFrame({
#     'user_id': [1, 2, 1],
#     'hotel_id': [1, 2, 3],
#     'checkin_date': ['2023-01-01', '2023-02-01', '2023-03-01'],
#     'checkout_date': ['2023-01-05', '2023-02-05', '2023-03-05']
# })
#
# # 预处理数据
# booking_data['checkin_date'] = pd.to_datetime(booking_data['checkin_date'])
# booking_data['checkout_date'] = pd.to_datetime(booking_data['checkout_date'])
# booking_data['stay_duration'] = (booking_data['checkout_date'] - booking_data['checkin_date']).dt.days
#
# user_encoder = LabelEncoder()
# hotel_encoder = LabelEncoder()
# booking_data['user_id'] = user_encoder.fit_transform(booking_data['user_id'])
# booking_data['hotel_id'] = hotel_encoder.fit_transform(booking_data['hotel_id'])
#
# # 特征和标签
# X = booking_data[['user_id', 'hotel_id', 'stay_duration', 'hotel_id']]  # 假设 'hotel_id' 作为评分的替代
# y = booking_data['hotel_id']
#
# # 训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # 微调模型
# model.fit(
#     [X_train['user_id'], X_train['hotel_id'], X_train['stay_duration'], X_train['hotel_id']],
#     y_train,
#     epochs=5,
#     batch_size=32,
#     validation_split=0.2
# )
#
# # 评估微调后的模型
# loss, accuracy = model.evaluate(
#     [X_test['user_id'], X_test['hotel_id'], X_test['stay_duration'], X_test['hotel_id']],
#     y_test
# )
# print(f'Test Loss after fine-tuning: {loss}, Test Accuracy: {accuracy}')
