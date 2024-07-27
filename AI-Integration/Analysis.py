import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import datetime
import pytz
import numpy as np
# Load the dataset
file_path = 'D:/Website_Optimization/server_requests_july_2023.xlsx'
data = pd.read_excel(file_path)

# Convert Date column to string before combining
data['Date'] = data['Date'].astype(str)

# Combine Date and Time columns into a single datetime column
data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

# Set the datetime column as the index
data.set_index('Datetime', inplace=True)

# Drop the original Date and Time columns
data.drop(columns=['Date', 'Time'], inplace=True)

# Resample the data to a per-minute frequency, summing the number of requests in each minute
data_resampled = data.resample('min').sum().fillna(0)

# Create features for the model
data_resampled['Hour'] = data_resampled.index.hour
data_resampled['Minute'] = data_resampled.index.minute
data_resampled['DayOfWeek'] = data_resampled.index.dayofweek

# Split the data into training and testing sets
X = data_resampled[['Hour', 'Minute', 'DayOfWeek']]
y = data_resampled['Number of Requests']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a predictive model (Linear Regression)
model = LinearRegression()
model.fit(X_train, y_train)

# Calculate Mean Squared Error
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Get the current time in India (IST)
india_timezone = pytz.timezone('Asia/Kolkata')
current_time_ist = datetime.datetime.now(india_timezone)

# Generate future timestamps for the next 10 minutes
future_times = [current_time_ist + datetime.timedelta(minutes=i) for i in range(1, 11)]

# Create features for these future timestamps
future_features = pd.DataFrame({
    'Hour': [t.hour for t in future_times],
    'Minute': [t.minute for t in future_times],
    'DayOfWeek': [t.weekday() for t in future_times]
}, index=future_times)

# Make predictions using the trained model
future_predictions = model.predict(future_features)

# Print the predictions with the corresponding datetime
for time, prediction in zip(future_times, future_predictions):
    print(f'Datetime: {time}, Predicted Number of Requests: {prediction}')





# ---------------------------------------------------------------------------------------------------

# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error
# import datetime
# import pytz
# import numpy as np

# # Load the dataset
# file_path = 'D:/Website_Optimization/server_requests_july_2023.xlsx'
# data = pd.read_excel(file_path)

# # Convert Date column to string before combining
# data['Date'] = data['Date'].astype(str)

# # Combine Date and Time columns into a single datetime column
# data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

# # Set the datetime column as the index
# data.set_index('Datetime', inplace=True)

# # Drop the original Date and Time columns
# data.drop(columns=['Date', 'Time'], inplace=True)

# # Resample the data to a per-minute frequency, summing the number of requests in each minute
# data_resampled = data.resample('min').sum().fillna(0)

# # Create features for the model
# data_resampled['Hour'] = data_resampled.index.hour
# data_resampled['Minute'] = data_resampled.index.minute
# data_resampled['DayOfWeek'] = data_resampled.index.dayofweek

# # Split the data into training and testing sets
# X = data_resampled[['Hour', 'Minute', 'DayOfWeek']]
# y = data_resampled['Number of Requests']

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train a predictive model (e.g., a Random Forest)
# model = RandomForestRegressor(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Calculate Mean Squared Error
# predictions = model.predict(X_test)
# mse = mean_squared_error(y_test, predictions)
# print(f'Mean Squared Error: {mse}')

# # Get the current time in India (IST)
# india_timezone = pytz.timezone('Asia/Kolkata')
# current_time_ist = datetime.datetime.now(india_timezone)

# # Generate future timestamps for the next 10 minutes
# future_times = [current_time_ist + datetime.timedelta(minutes=i) for i in range(1, 11)]

# # Create features for these future timestamps
# future_features = pd.DataFrame({
#     'Hour': [t.hour for t in future_times],
#     'Minute': [t.minute for t in future_times],
#     'DayOfWeek': [t.weekday() for t in future_times]
# }, index=future_times)

# # Make predictions using the trained model
# future_predictions = model.predict(future_features)

# # Print the predictions with the corresponding datetime
# for time, prediction in zip(future_times, future_predictions):
#     print(f'Datetime: {time}, Predicted Number of Requests: {prediction}')



avg_data = np.sum(future_predictions)/len(future_predictions)
print(avg_data)





# ___________________________________________________________________________________________________________________


# import pandas as pd

# # Load the dataset
# file_path = 'D:/Website_Optimization/server_requests_july_2023.xlsx'
# data = pd.read_excel(file_path)

# # Convert Date column to string before combining
# data['Date'] = data['Date'].astype(str)

# # Combine Date and Time columns into a single datetime column
# data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

# # Set the datetime column as the index
# data.set_index('Datetime', inplace=True)

# # Drop the original Date and Time columns
# data.drop(columns=['Date', 'Time'], inplace=True)

# # Resample the data to a per-minute frequency, summing the number of requests in each minute
# data_resampled = data.resample('min').sum().fillna(0)


# # Create features for the model
# data_resampled['Hour'] = data_resampled.index.hour
# data_resampled['Minute'] = data_resampled.index.minute
# data_resampled['DayOfWeek'] = data_resampled.index.dayofweek



# # Split the data into training and testing sets
# from sklearn.model_selection import train_test_split

# X = data_resampled[['Hour', 'Minute', 'DayOfWeek']]
# y = data_resampled['Number of Requests']

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# # Train a predictive model 
# from sklearn.ensemble import RandomForestRegressor

# model = RandomForestRegressor(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Make predictions
# predictions = model.predict(X_test)

# # Evaluate the model
# from sklearn.metrics import mean_squared_error

# mse = mean_squared_error(y_test, predictions)
# print(f'Mean Squared Error: {mse}')







