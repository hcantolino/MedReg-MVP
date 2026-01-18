import pandas as pd

# Mock survival data for testing Kaplan-Meier chart
data = {
    "PatientID": list(range(1, 21)),
    "time": [5, 6, 6, 7, 9, 10, 12, 15, 17, 25, 30, 32, 33, 34, 40, 8, 11, 13, 18, 22],
    "event": [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1]
}

df = pd.DataFrame(data)
df.to_csv("test_survival.csv", index=False)

print("test_survival.csv created successfully!")
print("\nPreview:")
print(df)