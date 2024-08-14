import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers import Input, Embedding, Flatten, Dense, Concatenate

# 加载数据
with open('data.json', 'r') as f:
    data = json.load(f)

# 转换为DataFrame
bookings_df = pd.DataFrame(data['bookings'])
hotels_df = pd.DataFrame(data['hotels'])

# 预处理数据
# 对于分类数据进行编码
label_encoder = LabelEncoder()
bookings_df['username_encoded'] = label_encoder.fit_transform(bookings_df['username'])
bookings_df['hotel_id_encoded'] = label_encoder.fit_transform(bookings_df['hotel_id'])
bookings_df['room_type_encoded'] = label_encoder.fit_transform(bookings_df['room_type'])
bookings_df['hotel_window_encoded'] = label_encoder.fit_transform(bookings_df['hotel_window'])
bookings_df['breakfast_encoded'] = label_encoder.fit_transform(bookings_df['breakfast'])

# 提取特征和标签
features = bookings_df[['username_encoded', 'hotel_id_encoded', 'room_type_encoded', 'hotel_window_encoded', 'breakfast_encoded']].values
labels = bookings_df['hotel_id_encoded'].values

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# 定义模型
num_users = bookings_df['username_encoded'].nunique()
num_hotels = bookings_df['hotel_id_encoded'].nunique()
num_room_types = bookings_df['room_type_encoded'].nunique()
num_hotel_windows = bookings_df['hotel_window_encoded'].nunique()
num_breakfasts = bookings_df['breakfast_encoded'].nunique()

user_input = Input(shape=(1,), name='user_input')
hotel_input = Input(shape=(1,), name='hotel_input')
room_type_input = Input(shape=(1,), name='room_type_input')
hotel_window_input = Input(shape=(1,), name='hotel_window_input')
breakfast_input = Input(shape=(1,), name='breakfast_input')

user_embedding = Embedding(input_dim=num_users, output_dim=10, name='user_embedding')(user_input)
hotel_embedding = Embedding(input_dim=num_hotels, output_dim=10, name='hotel_embedding')(hotel_input)
room_type_embedding = Embedding(input_dim=num_room_types, output_dim=10, name='room_type_embedding')(room_type_input)
hotel_window_embedding = Embedding(input_dim=num_hotel_windows, output_dim=10, name='hotel_window_embedding')(hotel_window_input)
breakfast_embedding = Embedding(input_dim=num_breakfasts, output_dim=10, name='breakfast_embedding')(breakfast_input)

user_vec = Flatten()(user_embedding)
hotel_vec = Flatten()(hotel_embedding)
room_type_vec = Flatten()(room_type_embedding)
hotel_window_vec = Flatten()(hotel_window_embedding)
breakfast_vec = Flatten()(breakfast_embedding)

concat = Concatenate()([user_vec, hotel_vec, room_type_vec, hotel_window_vec, breakfast_vec])

dense1 = Dense(128, activation='relu')(concat)
dense2 = Dense(64, activation='relu')(dense1)
output = Dense(num_hotels, activation='softmax')(dense2)

model = Model(inputs=[user_input, hotel_input, room_type_input, hotel_window_input, breakfast_input], outputs=output)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 训练模型
history = model.fit([X_train[:, 0], X_train[:, 1], X_train[:, 2], X_train[:, 3], X_train[:, 4]], y_train, epochs=10, batch_size=32, validation_data=([X_test[:, 0], X_test[:, 1], X_test[:, 2], X_test[:, 3], X_test[:, 4]], y_test))

# 保存模型
model.save('hotel_recommendation_model.h5')
