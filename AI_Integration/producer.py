import pandas as pd
import numpy as np
import datetime

# Define the date range for the data
start_date = datetime.datetime(2024, 7, 28)
end_date = datetime.datetime(2024, 7, 30)
date_range = pd.date_range(start=start_date, end=end_date, freq='S')  # Generate data for every second

# Generate random traffic counts
np.random.seed(42)  # For reproducibility
traffic_counts = np.random.randint(10, 3000, size=len(date_range))

# Create a DataFrame
traffic_data = pd.DataFrame({
    'Datetime': date_range,
    'Traffic': traffic_counts
})

# Save to a CSV file
file_path = 'synthetic_traffic_data.csv'
traffic_data.to_csv(file_path, index=False)

print(f"Synthetic traffic data generated and saved to {file_path}")
