import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import datetime

def predict_traffic_average(file_path: str) -> float:
    """
    Predict the average number of requests for the next 10 minutes based on synthetic traffic data.

    Returns:
    - float: The average predicted number of requests for the next 10 minutes.
    """

    # Load the generated synthetic data
    # file_path = 'synthetic_traffic_data.csv'  # Hardcoded path to the data file
    traffic_data = pd.read_csv(file_path)

    # Convert the 'Datetime' column to datetime object if it's not already
    traffic_data['Datetime'] = pd.to_datetime(traffic_data['Datetime'])

    # Enhance Feature Set
    traffic_data['Minute'] = traffic_data['Datetime'].dt.minute
    traffic_data['Hour'] = traffic_data['Datetime'].dt.hour
    traffic_data['DayOfWeek'] = traffic_data['Datetime'].dt.dayofweek
    traffic_data['IsWeekend'] = traffic_data['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
    traffic_data['Lag1'] = traffic_data['Traffic'].shift(1).fillna(0)  # Traffic from the previous minute

    # Features and target
    X = traffic_data[['Minute', 'Hour', 'DayOfWeek', 'IsWeekend', 'Lag1']]
    y = traffic_data['Traffic']

    # Train the Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Make Predictions for the Next 10 Minutes
    # Define the time range for prediction (next 10 minutes)
    current_time = datetime.datetime.now()
    future_times = pd.date_range(start=current_time, periods=10, freq='T')

    # Create features for future predictions
    future_features = pd.DataFrame({
        'Minute': future_times.minute,
        'Hour': future_times.hour,
        'DayOfWeek': future_times.weekday,
        'IsWeekend': future_times.weekday >= 5,
        'Lag1': y.iloc[-1]  # Last observed traffic
    })

    # Predict traffic for the next 10 minutes
    future_predictions = model.predict(future_features)

    # Calculate the average predicted traffic
    average_prediction = np.mean(future_predictions)

    req = 1
    if average_prediction > 500:
        req = 2
    else: 
        req = 3 

    return req

# Example usage:
average_predicted_traffic = predict_traffic_average("../data/synthetic_traffic_data.csv")
print(f"Average Predicted Number of Requests for the next 10 minutes: {average_predicted_traffic}")

