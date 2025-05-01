from sklearn.metrics import classification_report, confusion_matrix

def evaluate_model(y_true, y_pred, label="Authentication"):
    print(f"\n--- {label} Evaluation ---")
    print(confusion_matrix(y_true, y_pred))
    print(classification_report(y_true, y_pred))

def evaluate_access_rate(access_decisions):
    granted = sum(access_decisions)
    total = len(access_decisions)
    print(f"Access Granted: {granted}/{total} ({granted / total:.2%})")