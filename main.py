import numpy as np
import random
import scipy.stats

# === Simulated user delays (replace with real data if needed) ===
user_delays = [round(random.uniform(0.5, 5.0), 2) for _ in range(100)]
behavior_score = round(random.uniform(0.0, 5.0), 2)  # Extra variable between 0–5

print("📝 User Delay List (in seconds):")
print(user_delays)
print(f"\n🧠 Simulated behavior_score variable: {behavior_score}")

# === Rule 1: Uniformity Check ===
diffs = np.diff(user_delays)  # Difference between consecutive delays
uniform_score = np.std(diffs)

# === Rule 2: Checkpoint Behavior Change ===
checkpoint_start = 45
checkpoint_end = 55
before = user_delays[checkpoint_start-10:checkpoint_start]
after = user_delays[checkpoint_end:checkpoint_end+10]

mean_before = np.mean(before)
mean_after = np.mean(after)
pattern_change = abs(mean_after - mean_before)

# === Rule 3: Entropy (randomness of delays) ===
hist, _ = np.histogram(user_delays, bins=10)
entropy = scipy.stats.entropy(hist)

# === Decision Scoring ===
flags = 0
if uniform_score < 0.3:
    print("\n⚠️ Uniform timing detected (likely bot)")
    flags += 1
if pattern_change < 0.2:
    print("⚠️ No pattern change after checkpoint (likely bot)")
    flags += 1
if entropy < 1.0:
    print("⚠️ Low entropy in delays (likely bot)")
    flags += 1
if behavior_score < 1.5:
    print("⚠️ Low behavior score (likely bot)")
    flags += 1

# === Final Decision ===
print("\n🔎 Analysis Summary:")
print(f"→ Uniform Score (std of intervals): {uniform_score:.3f}")
print(f"→ Pattern Change (before vs after checkpoint): {pattern_change:.3f}")
print(f"→ Entropy of delays: {entropy:.3f}")
print(f"→ Behavior Score: {behavior_score}")

print("\n📢 Final AI-style Decision:")
if flags >= 2:
    print("❌ Likely BOT Detected (Auto)")
else:
    print("✅ Likely HUMAN Detected (Manual)")
