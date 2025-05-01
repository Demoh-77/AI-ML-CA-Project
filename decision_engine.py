def rule_based_decision(auth_preds, anomaly_scores, threshold=0.01):
    decisions = []
    for pred, score in zip(auth_preds, anomaly_scores):
        if score > threshold or pred == 0:
            decisions.append(False)
        else:
            decisions.append(True)
    return decisions