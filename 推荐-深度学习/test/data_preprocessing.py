# src/data_preprocessing.py
import json
import jieba
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# 定义分词函数
def jieba_tokenizer(text):
    return " ".join(jieba.cut(text))

def load_json_data(booking_json_path, hotel_json_path, output_csv_path):
    # 读取JSON文件
    with open(booking_json_path, 'r', encoding='utf-8') as f:
        bookings = json.load(f)

    with open(hotel_json_path, 'r', encoding='utf-8') as f:
        hotels = json.load(f)

    # 创建DataFrame
    booking_df = pd.DataFrame(bookings)
    hotel_df = pd.DataFrame(hotels)

    # 合并数据，根据预订信息中的hotel_id和酒店信息中的id
    merged_df = booking_df.merge(hotel_df, left_on='hotel_id', right_on='id', suffixes=('_booking', '_hotel'))

    # 选择需要的列并重命名
    merged_df = merged_df[
        ['username', 'hotel_id', 'check_in_date', 'check_out_date', 'rating', 'address', 'name', 'hotel_type',
         'location']]
    merged_df.rename(columns={'username': 'user_id', 'hotel_id': 'item_id'}, inplace=True)

    # 保存为CSV文件
    merged_df.to_csv(output_csv_path, index=False)
    return merged_df

def load_and_preprocess_data(input_path, output_path):
    # 读取数据
    data = pd.read_csv(input_path)

    # 编码用户和物品ID
    user_encoder = LabelEncoder()
    item_encoder = LabelEncoder()

    data['user_id'] = user_encoder.fit_transform(data['user_id'])
    data['item_id'] = item_encoder.fit_transform(data['item_id'])

    # 查看和打印用户编码器的映射关系
    user_mapping = dict(zip(user_encoder.classes_, range(len(user_encoder.classes_))))
    print("User ID Mapping:")
    for user, code in user_mapping.items():
        print(f"{user} -> {code}")

    # 查看和打印酒店编码器的映射关系
    item_mapping = dict(zip(item_encoder.classes_, range(len(item_encoder.classes_))))
    print("Hotel ID Mapping:")
    for item, code in item_mapping.items():
        print(f"{item} -> {code}")

    # 编码酒店类型
    hotel_type_encoder = LabelEncoder()
    data['hotel_type'] = hotel_type_encoder.fit_transform(data['hotel_type'])

    # 对地址和名称进行分词
    data['address'] = data['address'].apply(jieba_tokenizer)
    data['name'] = data['name'].apply(jieba_tokenizer)

    # 文本特征编码
    address_vectorizer = TfidfVectorizer(max_features=5)
    name_vectorizer = TfidfVectorizer(max_features=5)

    address_tfidf = address_vectorizer.fit_transform(data['address']).toarray()
    name_tfidf = name_vectorizer.fit_transform(data['name']).toarray()

    # 获取实际的特征数量
    address_tfidf_features = address_tfidf.shape[1]
    name_tfidf_features = name_tfidf.shape[1]

    # 将编码后的文本特征合并到原始数据中
    address_df = pd.DataFrame(address_tfidf, columns=[f'address_tfidf_{i}' for i in range(address_tfidf_features)])
    name_df = pd.DataFrame(name_tfidf, columns=[f'name_tfidf_{i}' for i in range(name_tfidf_features)])

    data = pd.concat([data, address_df, name_df], axis=1)

    data.to_csv(output_path, index=False)
    return data, user_encoder, item_encoder, hotel_type_encoder, address_vectorizer, name_vectorizer

if __name__ == "__main__":
    booking_json_path = os.path.join('', 'bookings.json')
    hotel_json_path = os.path.join('', 'hotels.json')
    raw_data_path = os.path.join('', 'raw_data.csv')
    processed_data_path = os.path.join('', 'processed_data.csv')

    # 加载JSON数据并转换为CSV
    load_json_data(booking_json_path, hotel_json_path, raw_data_path)

    # 预处理数据
    load_and_preprocess_data(raw_data_path, processed_data_path)