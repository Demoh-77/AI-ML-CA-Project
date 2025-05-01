import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import mutual_info_classif

def load_csvs_from_folder(folder):
    dfs = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder, file))
            dfs.append(df)
    return dfs

def load_and_merge_datasets(nbaiot_path, iot23_path):
    dfs = load_csvs_from_folder(nbaiot_path) + load_csvs_from_folder(iot23_path)
    merged = pd.concat(dfs, ignore_index=True)
    merged = merged.drop_duplicates().dropna()
    return merged

def scale_features(X):
    scaler = MinMaxScaler()
    return scaler.fit_transform(X)

def select_features(X, y, num_features=30):
    mi = mutual_info_classif(X, y)
    top_indices = np.argsort(mi)[-num_features:]
    return X[:, top_indices], top_indices

def preprocess(df, label_column='label'):
    y = df[label_column]
    X = df.drop(columns=[label_column])
    X_scaled = scale_features(X)
    X_selected, selected_indices = select_features(X_scaled, y)
    return train_test_split(X_selected, y, test_size=0.2, random_state=42), selected_indices