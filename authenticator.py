import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

class ContinuousAuthenticator:
    def __init__(self):
        self.rf = RandomForestClassifier(n_estimators=100, max_depth=15, min_samples_split=10)
        self.gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)

    def train(self, X_train, y_train):
        self.rf.fit(X_train, y_train)
        self.gb.fit(X_train, y_train)

    def predict(self, X):
        rf_probs = self.rf.predict_proba(X)
        gb_probs = self.gb.predict_proba(X)
        combined = 0.6 * rf_probs + 0.4 * gb_probs
        return np.argmax(combined, axis=1)