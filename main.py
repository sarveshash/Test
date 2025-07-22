from sklearn.ensemble import IsolationForest
import numpy as np

# Simulated data: 100 time intervals (in seconds) between user commands
# For example: [2.1, 3.0, 0.5, ...]
user_times = np.random.normal(loc=2.5, scale=0.8, size=100)  # Assume this is your actual data

# Simulated 'behavior score' for current session (0 to 5, e.g., based on response delay, typing pattern etc.)
current_behavior_score = 1.2  # 0 is most bot-like, 5 is most human-like

# Combine into a feature set
# Here: feature1 = mean of user_times, feature2 = standard deviation of times, feature3 = current score
features = np.array([[np.mean(user_times), np.std(user_times), current_behavior_score]])

# Prepare training data (you can use unlabeled historic sessions)
# For simplicity, assume normal human behavior
training_data = []
for _ in range(200):
    mean = np.random.uniform(2.0, 4.5)
    std = np.random.uniform(0.3, 1.5)
    score = np.random.uniform(2.0, 5.0)
    training_data.append([mean, std, score])
training_data = np.array(training_data)

# Train Isolation Forest
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(training_data)

# Predict: -1 is anomaly (likely bot), 1 is normal (likely human)
prediction = model.predict(features)[0]

if prediction == -1:
    print("⚠️ Likely Auto/Bot Detected")
else:
    print("✅ Likely Human User")
