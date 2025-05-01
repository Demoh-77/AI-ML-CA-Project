from preprocessing import load_and_merge_datasets, preprocess
from autoencoder_module import build_autoencoder, compute_anomaly_scores
from authenticator import ContinuousAuthenticator
from decision_engine import rule_based_decision
from evaluator import evaluate_model, evaluate_access_rate
import os

def download_datasets():
    os.makedirs("data/nbaiot", exist_ok=True)
    os.makedirs("data/iot23", exist_ok=True)
    if not os.listdir("data/nbaiot"):
        os.system("kaggle datasets download -d mkashifn/nbaiot-dataset -p data/nbaiot --unzip")
    if not os.listdir("data/iot23"):
        os.system("kaggle datasets download -d engraqeel/iot23preprocesseddata -p data/iot23 --unzip")

def main():
    print("⬇️ Downloading datasets if not present...")
    download_datasets()

    print("📦 Loading and merging data...")
    merged_df = load_and_merge_datasets("data/nbaiot", "data/iot23")

    print("🧪 Preprocessing...")
    (X_train, X_test, y_train, y_test), selected_indices = preprocess(merged_df)

    print("🧠 Training Autoencoder...")
    autoencoder = build_autoencoder(X_train.shape[1])
    autoencoder.fit(X_train, X_train, epochs=30, batch_size=64, validation_split=0.1, verbose=0)

    print("🔍 Computing anomaly scores...")
    anomaly_scores = compute_anomaly_scores(autoencoder, X_test)

    print("🔐 Training authenticator...")
    auth = ContinuousAuthenticator()
    auth.train(X_train, y_train)

    print("✅ Predicting authentication results...")
    auth_preds = auth.predict(X_test)

    print("⚖️ Applying Zero Trust decision engine...")
    access_decisions = rule_based_decision(auth_preds, anomaly_scores)

    evaluate_model(y_test, auth_preds)
    evaluate_access_rate(access_decisions)

if __name__ == "__main__":
    main()