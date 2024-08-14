import os
import numpy as np
import pandas as pd
from keras import models
from data_preprocessing import load_and_preprocess_data, load_json_data

# 加载数据和模型
hotel_json_path = os.path.join('', 'hotels.json')
booking_json_path = os.path.join('', 'bookings.json')
raw_data_path = os.path.join('', 'raw_data.csv')
processed_data_path = os.path.join('', 'processed_data.csv')

# 加载JSON数据并转换为CSV
load_json_data(booking_json_path, hotel_json_path, raw_data_path)

# 加载并预处理数据
data, user_encoder, item_encoder, hotel_type_encoder, address_vectorizer, name_vectorizer = load_and_preprocess_data(raw_data_path, processed_data_path)

model_path = os.path.join('saved_models', 'model.keras')
model = models.load_model(model_path)

# 测试用户和酒店
test_user_id = 'liu'
test_hotel_id = 'B0JR4C9RJR'

# 检查用户和酒店ID是否在训练数据中
print(f"User ID classes: {user_encoder.classes_}")
print(f"Hotel ID classes: {item_encoder.classes_}")

if test_user_id not in user_encoder.classes_:
    print(f"User ID {test_user_id} not in training data.")
else:
    print(f"User ID {test_user_id} found in training data.")
if test_hotel_id not in item_encoder.classes_:
    print(f"Hotel ID {test_hotel_id} not in training data.")
else:
    print(f"Hotel ID {test_hotel_id} found in training data.")

# 编码用户和酒店ID
encoded_user_id = user_encoder.transform([test_user_id])[0]
encoded_hotel_id = item_encoder.transform([test_hotel_id])[0]

print(f"Encoded user ID: {encoded_user_id}")
print(f"Encoded hotel ID: {encoded_hotel_id}")

# 获取酒店特征
hotel_row = data[data['item_id'] == encoded_hotel_id]
if hotel_row.empty:
    print(f"Hotel ID {encoded_hotel_id} not found in processed data.")
    exit()
else:
    hotel_row = hotel_row.iloc[0]
    print(f"Hotel row: {hotel_row}")

# 确认日期格式
print(f"check_in_date: {hotel_row['check_in_date']}, check_out_date: {hotel_row['check_out_date']}")

# 提取并处理用户特征
user_features = pd.DataFrame({
    'check_in_date': [hotel_row['check_in_date']],
    'check_out_date': [hotel_row['check_out_date']]
})

# 确保日期列的类型为字符串，然后转换为日期
user_features['check_in_date'] = pd.to_datetime(user_features['check_in_date'].astype(str))
user_features['check_out_date'] = pd.to_datetime(user_features['check_out_date'].astype(str))

# 转换日期为数值类型
user_features['check_in_date'] = user_features['check_in_date'].apply(lambda x: x.toordinal())
user_features['check_out_date'] = user_features['check_out_date'].apply(lambda x: x.toordinal())

# 确保用户特征维度匹配模型输入维度
user_feature_dim = 2  # 模型期望的用户特征维度
user_features_array = np.zeros((1, user_feature_dim), dtype=np.float32)
user_features_array[0, :2] = user_features.values[0]

# 动态确定TF-IDF特征的数量
address_tfidf_columns = [col for col in data.columns if col.startswith('address_tfidf_')]
name_tfidf_columns = [col for col in data.columns if col.startswith('name_tfidf_')]

# 提取并处理酒店特征
hotel_features = np.concatenate([
    np.array([[hotel_row['hotel_type'], hotel_row['rating']]]),
    hotel_row[address_tfidf_columns].values.reshape(1, -1),
    hotel_row[name_tfidf_columns].values.reshape(1, -1)
], axis=1)

# 只选择前item_feature_dim个特征来匹配模型输入
item_feature_dim = 12  # 模型期望的酒店特征维度
hotel_features_array = np.zeros((1, item_feature_dim), dtype=np.float32)
hotel_features_array[0, :item_feature_dim] = hotel_features[0, :item_feature_dim]

# 检查特征维度
print(f"User features shape: {user_features_array.shape}")
print(f"Hotel features shape: {hotel_features_array.shape}")

# 预测推荐
prediction = model.predict([np.array([encoded_user_id]), np.array([encoded_hotel_id]), user_features_array, hotel_features_array])
print(f'Recommendation score for user {test_user_id} and hotel {test_hotel_id}: {prediction[0][0]:.4f}')