import tensorflow as tf
from keras import layers, models, optimizers, regularizers

def create_model(num_users, num_items, embedding_dim=50, user_feature_dim=10, item_feature_dim=5):
    # 输入层
    user_input = layers.Input(shape=(1,), name='user_input')
    item_input = layers.Input(shape=(1,), name='item_input')
    user_features_input = layers.Input(shape=(user_feature_dim,), name='user_features_input')
    item_features_input = layers.Input(shape=(item_feature_dim,), name='item_features_input')

    # 嵌入层
    user_embedding_gmf = layers.Embedding(input_dim=num_users, output_dim=embedding_dim, name='user_embedding_gmf')(user_input)
    item_embedding_gmf = layers.Embedding(input_dim=num_items, output_dim=embedding_dim, name='item_embedding_gmf')(item_input)
    user_embedding_mlp = layers.Embedding(input_dim=num_users, output_dim=embedding_dim, name='user_embedding_mlp')(user_input)
    item_embedding_mlp = layers.Embedding(input_dim=num_items, output_dim=embedding_dim, name='item_embedding_mlp')(item_input)

    # 展平嵌入层
    user_embedding_gmf = layers.Flatten()(user_embedding_gmf)
    item_embedding_gmf = layers.Flatten()(item_embedding_gmf)
    user_embedding_mlp = layers.Flatten()(user_embedding_mlp)
    item_embedding_mlp = layers.Flatten()(item_embedding_mlp)

    # GMF 部分
    gmf_vector = layers.multiply([user_embedding_gmf, item_embedding_gmf])

    # MLP 部分
    mlp_vector = layers.Concatenate()([user_embedding_mlp, item_embedding_mlp, user_features_input, item_features_input])
    mlp_vector = layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.01))(mlp_vector)
    mlp_vector = layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.01))(mlp_vector)
    mlp_vector = layers.Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.01))(mlp_vector)
    mlp_vector = layers.Dense(16, activation='relu', kernel_regularizer=regularizers.l2(0.01))(mlp_vector)

    # 组合 GMF 和 MLP
    concat_vector = layers.Concatenate()([gmf_vector, mlp_vector])
    output = layers.Dense(1, activation='sigmoid')(concat_vector)

    # 构建模型
    model = models.Model(inputs=[user_input, item_input, user_features_input, item_features_input], outputs=output)
    model.compile(optimizer=optimizers.Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

    return model
