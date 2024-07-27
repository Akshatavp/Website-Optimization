import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define the date for which we want to generate data
specific_date = datetime(2023, 7, 28)

# Generate a list of all seconds in the specific date
start_time = datetime(specific_date.year, specific_date.month, specific_date.day)
end_time = start_time + timedelta(days=1)  # End of the day

# Generate all seconds in the day
time_index = pd.date_range(start=start_time, end=end_time, freq='S')[:-1]  # Exclude the last timestamp (next day start)

# Generate random number of requests for each second
requests = np.random.randint(500, 3000, size=len(time_index))

# Create DataFrame
df = pd.DataFrame({
    'Datetime': time_index,
    'Number of Requests': requests
})

# Split the Datetime column into Date and Time
df['Date'] = df['Datetime'].dt.date
df['Time'] = df['Datetime'].dt.time

# Reorder columns
df = df[['Date', 'Time', 'Number of Requests']]

# Export to Excel
excel_filename = 'server_requests_27_july_2023.xlsx'
df.to_excel(excel_filename, index=False, engine='openpyxl')

print(f"Data successfully generated and saved to {excel_filename}")


# --------------------------------------------------------------------------------------------------
# import pandas as pd
# import numpy as np
# from datetime import datetime, timedelta

# # Parameters
# start_date = datetime(2023, 7, 1)
# end_date = datetime(2023, 7, 31)
# total_rows = 3000

# # Function to generate random times
# def generate_random_time():
#     seconds_in_day = 86400
#     random_seconds = np.random.randint(0, seconds_in_day)
#     return str(timedelta(seconds=random_seconds))

# # Generate dates
# date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
# dates = np.random.choice(date_range, size=total_rows, replace=True)

# # Generate times and number of requests
# times = [generate_random_time() for _ in range(total_rows)]
# requests = np.random.randint(500, 3000, size=total_rows)

# # Create DataFrame
# data = {
#     'Date': dates,
#     'Time': times,
#     'Number of Requests': requests
# }

# df = pd.DataFrame(data)

# # Export to Excel
# excel_filename = 'server_requests_july_2023.xlsx'
# df.to_excel(excel_filename, index=False, engine='openpyxl')

# print(f"Data successfully generated and saved to {excel_filename}")
