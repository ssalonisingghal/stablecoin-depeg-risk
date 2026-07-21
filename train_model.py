import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings("ignore")

# --- 1. pool the three coins ---
frames = []
for name in ["usdc", "usdt", "dai"]:
    df = pd.read_csv(f"data/{name}_features.csv")
    df["coin"] = name
    frames.append(df)
data = pd.concat(frames, ignore_index=True)
data["date"] = pd.to_datetime(data["date"])
data = data.sort_values("date").reset_index(drop=True)

# --- 2. one-hot encode coin identity ---
data = pd.get_dummies(data, columns=["coin"], prefix="is", dtype=int)
feature_cols = [c for c in data.columns if c.startswith("f_") or c.startswith("is_")]

# --- 2b. clean infinities/NaNs BEFORE splitting (from z-score divide-by-zero) ---
data[feature_cols] = data[feature_cols].replace([np.inf, -np.inf], np.nan)
data = data.dropna(subset=feature_cols).reset_index(drop=True)

# --- 3. split by DATE (never random) ---
split_date = "2024-01-01"
train = data[data["date"] < split_date]
test  = data[data["date"] >= split_date]
X_train, y_train = train[feature_cols], train["label"]
X_test,  y_test  = test[feature_cols],  test["label"]
print(f"Train: {len(X_train)} rows, {y_train.sum()} positives")
print(f"Test:  {len(X_test)} rows, {y_test.sum()} positives")

# --- 4. scale (fit on train only) ---
f_cols  = [c for c in feature_cols if c.startswith("f_")]
is_cols = [c for c in feature_cols if c.startswith("is_")]

scaler = StandardScaler()
X_train_f = scaler.fit_transform(X_train[f_cols])
X_test_f  = scaler.transform(X_test[f_cols])

# recombine scaled features with unscaled 0/1 coin flags
X_train_s = np.hstack([X_train_f, X_train[is_cols].values])
X_test_s  = np.hstack([X_test_f,  X_test[is_cols].values])

# --- 5. logistic regression, balanced ---
model = LogisticRegression(class_weight="balanced", max_iter=1000)
model.fit(X_train_s, y_train)

# --- 6. evaluate ---
pred = model.predict(X_test_s)
print("\nConfusion matrix:")
print(confusion_matrix(y_test, pred))
print("\nClassification report:")
print(classification_report(y_test, pred, zero_division=0))

# --- 7. feature coefficients ---
coefs = pd.Series(model.coef_[0], index=f_cols + is_cols).sort_values()
print("\nFeature coefficients (negative = pushes toward event):")
print(coefs.to_string())