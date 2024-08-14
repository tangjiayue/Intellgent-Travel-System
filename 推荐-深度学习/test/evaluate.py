# import os
#
# import numpy as np
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from keras.models import load_model
# from data_preprocessing import load_and_preprocess_data
#
# # 加载数据和模型
# processed_data_path = os.path.join('', 'processed_data.csv')
# data = pd.read_csv(processed_data_path)
# model_path = os.path.join('saved_models', 'model.keras')
# model = load_model(model_path)
#
# # 准备测试数据
# user_ids = data['user_id'].values
# item_ids = data['item_id'].values
#
# # 提取特征
# user_features = data[['check_in_date', 'check_out_date']].apply(pd.to_datetime)
# user_features['check_in_date'] = user_features['check_in_date'].apply(lambda x: x.toordinal())
# user_features['check_out_date'] = user_features['check_out_date'].apply(lambda x: x.toordinal())
#
# # 动态确定TF-IDF特征的数量
# address_tfidf_features = len([col for col in data.columns if col.startswith('address_tfidf_')])
# name_tfidf_features = len([col for col in data.columns if col.startswith('name_tfidf_')])
#
# # 合并所有特征
# item_features = data[['hotel_type', 'rating']].values
# address_features = data[[f'address_tfidf_{i}' for i in range(address_tfidf_features)]].values
# name_features = data[[f'name_tfidf_{i}' for i in range(name_tfidf_features)]].values
#
# item_features = np.concatenate([item_features, address_features, name_features], axis=1)
#
# # 转换为数值类型
# user_features = user_features.values.astype(np.float32)
# item_features = item_features.astype(np.float32)
# user_ids = user_ids.astype(np.int32)
# item_ids = item_ids.astype(np.int32)
#
# # 分割数据集
# X_train_user, X_val_user, X_train_item, X_val_item, X_train_user_features, X_val_user_features, X_train_item_features, X_val_item_features, y_train, y_val = train_test_split(
#     user_ids, item_ids, user_features, item_features, test_size=0.2, random_state=42)
#
# # 评估模型
# evaluation = model.evaluate([X_val_user, X_val_item, X_val_user_features, X_val_item_features], y_val)
# print(f'Accuracy: {evaluation[1]:.4f}')
