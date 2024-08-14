# src/train.py
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os
from data_preprocessing import load_and_preprocess_data, load_json_data
from model import create_model

# 路径设置
booking_json_path = os.path.join('', 'bookings.json')
hotel_json_path = os.path.join('', 'hotels.json')
raw_data_path = os.path.join('', 'raw_data.csv')
processed_data_path = os.path.join('', 'processed_data.csv')

# 加载JSON数据并转换为CSV
load_json_data(booking_json_path, hotel_json_path, raw_data_path)

# 加载并预处理数据
data, user_encoder, item_encoder, hotel_type_encoder, address_vectorizer, name_vectorizer = load_and_preprocess_data(raw_data_path, processed_data_path)

# 准备训练数据
user_ids = data['user_id'].values
item_ids = data['item_id'].values

# 提取特征
user_features = data[['check_in_date', 'check_out_date']].apply(pd.to_datetime)
user_features['check_in_date'] = user_features['check_in_date'].apply(lambda x: x.toordinal())
user_features['check_out_date'] = user_features['check_out_date'].apply(lambda x: x.toordinal())

# 动态确定TF-IDF特征的数量
address_tfidf_features = len([col for col in data.columns if col.startswith('address_tfidf_')])
name_tfidf_features = len([col for col in data.columns if col.startswith('name_tfidf_')])

# 合并所有特征
item_features = data[['hotel_type', 'rating']].values
address_features = data[[f'address_tfidf_{i}' for i in range(address_tfidf_features)]].values
name_features = data[[f'name_tfidf_{i}' for i in range(name_tfidf_features)]].values

item_features = np.concatenate([item_features, address_features, name_features], axis=1)

# 转换为数值类型
user_features = user_features.values.astype(np.float32)
item_features = item_features.astype(np.float32)
user_ids = user_ids.astype(np.int32)
item_ids = item_ids.astype(np.int32)

# 分割数据集
X_train_user, X_val_user, X_train_item, X_val_item, X_train_user_features, X_val_user_features, X_train_item_features, X_val_item_features = train_test_split(
    user_ids, item_ids, user_features, item_features, test_size=0.2, random_state=42)

# 创建模型
num_users = len(user_encoder.classes_)
num_items = len(item_encoder.classes_)
model = create_model(num_users, num_items, user_feature_dim=user_features.shape[1], item_feature_dim=item_features.shape[1])

# 训练模型
history = model.fit(
    [X_train_user, X_train_item, X_train_user_features, X_train_item_features],
    np.ones(len(X_train_user)),  # 用户预定的标签
    epochs=10,
    batch_size=256,
    validation_data=([X_val_user, X_val_item, X_val_user_features, X_val_item_features], np.ones(len(X_val_user)))  # 用户预定的标签
)
# 保存模型
model_path = os.path.join('saved_models', 'model.keras')
model.save(model_path)
