# Zero Trust IoT Security Framework

## Project Overview
This project implements a **Zero Trust security framework** for IoT networks, leveraging machine learning to perform continuous authentication and anomaly detection. It processes network traffic data from the **NBAIoT** and **IoT-23** datasets to:
- Detect anomalies using an autoencoder.
- Authenticate devices using an ensemble of Random Forest and Gradient Boosting classifiers.
- Make access decisions based on a rule-based decision engine.
- Evaluate model performance and access grant rates.

The framework is designed to ensure robust security in IoT environments by assuming no inherent trust and continuously verifying device behavior.

## Features
- **Data Preprocessing**: Loads and merges CSV files, scales features, and selects top features using mutual information.
- **Anomaly Detection**: Uses an autoencoder to compute anomaly scores for network traffic.
- **Continuous Authentication**: Combines Random Forest and Gradient Boosting classifiers for device authentication.
- **Zero Trust Decision Engine**: Applies rule-based logic to grant or deny access based on authentication and anomaly scores.
- **Evaluation**: Provides detailed metrics (confusion matrix, classification report, access grant rate).

## Datasets
- **NBAIoT**: Network traffic data from IoT devices (~7GB, multiple CSV files). [Kaggle Link](https://www.kaggle.com/datasets/mkashifn/nbaiot-dataset).
- **IoT-23**: Preprocessed network traffic data (~1-2GB, multiple CSV files). [Kaggle Link](https://www.kaggle.com/datasets/engraqeel/iot23preprocesseddata).

## Prerequisites
- **Hardware**:
  - Minimum: 2 vCPUs, 5GB RAM (for subset of data).
  - Recommended: 4+ vCPUs, 16GB+ RAM (for full dataset).
- **Software**:
  - Python 3.8+
  - Kaggle API for dataset download
  - Deepnote (optional, for cloud execution) or local environment
- **Dependencies** (see `requirements.txt`):
  - `numpy`
  - `pandas`
  - `scikit-learn`
  - `tensorflow`
  - `kaggle`

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd zero-trust-iot-security
```

### 2. Install Dependencies
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Kaggle API
To download datasets automatically:
1. Go to [Kaggle Account Settings](https://www.kaggle.com/account), create a new API token, and download `kaggle.json`.
2. Place `kaggle.json` in `~/.kaggle/`:
   ```bash
   mkdir -p ~/.kaggle
   cp path/to/kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```
3. Verify:
   ```bash
   kaggle datasets list
   ```

Alternatively, set environment variables:
```bash
export KAGGLE_USERNAME=your_username
export KAGGLE_KEY=your_api_key
```

### 4. Download Datasets
Run the script to download datasets (or manually download and place in `data/nbaiot/` and `data/iot23/`):
```bash
python main.py
```
This creates:
- `data/nbaiot/`: NBAIoT CSV files
- `data/iot23/`: IoT-23 CSV files

### 5. (Optional) Run in Deepnote
1. Upload project files to Deepnote.
2. Upload `kaggle.json` to `/work/` and configure:
   ```bash
   mkdir -p ~/.kaggle
   mv /work/kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```
3. Install dependencies in Deepnote terminal:
   ```bash
   pip install numpy pandas scikit-learn tensorflow kaggle
   ```

## Usage
Run the main script:
```bash
python main.py
```

### Workflow
1. Downloads datasets (if not present).
2. Loads and merges CSV files from `data/nbaiot/` and `data/iot23/`.
3. Preprocesses data (scaling, feature selection, train-test split).
4. Trains an autoencoder for anomaly detection.
5. Trains a continuous authenticator (Random Forest + Gradient Boosting).
6. Computes anomaly scores and authentication predictions.
7. Applies Zero Trust decision rules.
8. Evaluates model performance and access grant rate.

### Expected Output
```
⬇️ Downloading datasets if not present...
📦 Loading and merging data...
🧪 Preprocessing...
🧠 Training Autoencoder...
🔍 Computing anomaly scores...
🔐 Training authenticator...
✅ Predicting authentication results...
⚖️ Applying Zero Trust decision engine...
--- Authentication Evaluation ---
[[...]]  # Confusion matrix
              precision    recall  f1-score   support
...  # Classification report
Access Granted: X/Y (Z%)
```

## Project Structure
```
zero-trust-iot-security/
├── data/
│   ├── nbaiot/          # NBAIoT dataset CSVs
│   └── iot23/           # IoT-23 dataset CSVs
├── authenticator.py     # Continuous authentication model
├── autoencoder_module.py # Autoencoder for anomaly detection
├── decision_engine.py   # Rule-based decision logic
├── evaluator.py         # Model evaluation functions
├── main.py              # Main script
├── preprocessing.py     # Data loading and preprocessing
├── requirements.txt     # Dependencies
└── README.md            # This file
```

### File Descriptions
- **`authenticator.py`**: Defines `ContinuousAuthenticator` class using Random Forest and Gradient Boosting for authentication.
- **`autoencoder_module.py`**: Implements an autoencoder for anomaly detection and computes anomaly scores.
- **`decision_engine.py`**: Contains `rule_based_decision` function for Zero Trust access decisions.
- **`evaluator.py`**: Provides functions to evaluate model performance and access rates.
- **`main.py`**: Orchestrates the workflow, from data loading to evaluation.
- **`preprocessing.py`**: Handles dataset loading, merging, scaling, and feature selection.

## Performance Considerations
- **Memory**: The full dataset (~9GB) requires 16GB+ RAM. For 5GB RAM, process a subset (1-2 CSVs) using chunked loading:
  ```python
  # In preprocessing.py
  pd.read_csv(file, chunksize=10000, dtype=np.float32)
  ```
- **Runtime**: On 2 vCPUs, 5GB RAM with a subset (~500,000 rows):
  - ~16-60 minutes (loading: 2-5 min, preprocessing: 2-10 min, training: 10-35 min, evaluation: 1-5 min).
  - Full dataset is infeasible on 5GB RAM.
- **Optimization**:
  - Use `float32` for numerical data.
  - Process CSVs in chunks.
  - Limit to 1-2 CSVs:
    ```bash
    mkdir -p data/nbaiot_subset
    mkdir -p data/iot23_subset
    cp data/nbaiot/*.csv data/nbaiot_subset/ -v | head -n 1
    cp data/iot23/*.csv data/iot23_subset/ -v | head -n 1
    ```
    Update `main.py`:
    ```python
    merged_df = load_and_merge_datasets("data/nbaiot_subset", "data/iot23_subset")
    ```

## Troubleshooting
- **Stuck at "Loading and merging data..."**:
  - Check dataset directories:
    ```bash
    ls -lh data/nbaiot/
    ls -lh data/iot23/
    ```
  - Ensure sufficient RAM (use subset or upgrade to 16GB).
  - Add debug prints to `preprocessing.py`:
    ```python
    def load_csvs_from_folder(folder):
        dfs = []
        print(f"Loading CSVs from {folder}...")
        for file in os.listdir(folder):
            if file.endswith(".csv"):
                print(f"  Reading {file}...")
                df = pd.read_csv(os.path.join(folder, file), dtype=np.float32)
                print(f"  Loaded {file} with shape {df.shape}")
                dfs.append(df)
        return dfs
    ```
- **Kaggle API Errors**:
  - Verify `~/.kaggle/kaggle.json`:
    ```bash
    ls -la ~/.kaggle/
    ```
  - Re-download from Kaggle if invalid.
- **Memory Errors**:
  - Use chunked loading or subset data.
  - Run locally with 16GB+ RAM.
- **TensorFlow CUDA Warnings**:
  - Safe to ignore (falls back to CPU).
  - Suppress with:
    ```bash
    export TF_CPP_MIN_LOG_LEVEL=2
    ```

## Future Improvements
- **Optimize Memory**: Stream data directly from CSVs without loading all into memory.
- **Parallel Processing**: Use `dask` or `multiprocessing` for faster CSV loading.
- **Hyperparameter Tuning**: Optimize autoencoder and classifier parameters.
- **Real-Time Processing**: Adapt for streaming IoT data.
- **Visualization**: Add plots for anomaly scores and model performance.

## License
This project is licensed under the MIT License.

## Contact
For questions or contributions, please open an issue or contact the project maintainer.

---
*Generated on May 1, 2025*