# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# # from tensorflow.keras.models import Model
# # from keras.layers import Input, Embedding, Flatten, Concatenate, Dense, Dropout
#
# # 假设我们有以下数据
# # hotel_data = pd.read_csv('hotel_data.csv')
# # booking_data = pd.read_csv('booking_data.csv')
#
# # 示例数据
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
# # 数据预处理
# # 例如：对类别特征进行编码，对日期特征进行处理等
# # 这里仅作为示例，具体预处理步骤根据实际数据决定
#
# # 特征和标签
# X = booking_data[['user_id', 'hotel_id']]
# y = booking_data['hotel_id']
#
# # 训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # 定义模型
# input_user = Input(shape=(1,))
# input_hotel = Input(shape=(1,))
#
# # 用户和酒店ID的嵌入层
# embedding_user = Embedding(input_dim=1000, output_dim=50)(input_user)
# embedding_hotel = Embedding(input_dim=1000, output_dim=50)(input_hotel)
#
# # 展平层
# flatten_user = Flatten()(embedding_user)
# flatten_hotel = Flatten()(embedding_hotel)
#
# # 合并层
# concat = Concatenate()([flatten_user, flatten_hotel])
#
# # 全连接层
# dense_1 = Dense(128, activation='relu')(concat)
# dropout_1 = Dropout(0.5)(dense_1)
# dense_2 = Dense(64, activation='relu')(dropout_1)
# output = Dense(1, activation='sigmoid')(dense_2)
#
# # 定义模型
# model = Model(inputs=[input_user, input_hotel], outputs=output)
#
# # 编译模型
# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#
# # 训练模型
# model.fit([X_train['user_id'], X_train['hotel_id']], y_train, epochs=10, batch_size=32, validation_split=0.2)
#
# # 评估模型
# loss, accuracy = model.evaluate([X_test['user_id'], X_test['hotel_id']], y_test)
# print(f'Test Accuracy: {accuracy}')
