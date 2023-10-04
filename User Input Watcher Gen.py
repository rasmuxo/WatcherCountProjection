import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy import interpolate

# Function to get user input for dates and watcher counts
def get_dates_and_counts():
    dates_input = input("Enter a comma-separated list of dates in MM/DD/YYYY format: ")
    watcher_counts_input = input("Enter a comma-separated list of watcher counts: ")

    dates = []
    watcher_counts = []

    date_strings = dates_input.split(',')
    watcher_count_strings = watcher_counts_input.split(',')

    if len(date_strings) != len(watcher_count_strings):
        print("The number of dates must match the number of watcher counts.")
        return dates, watcher_counts

    for date_str, watcher_count_str in zip(date_strings, watcher_count_strings):
        try:
            date = datetime.strptime(date_str.strip(), "%m/%d/%Y")
            watcher_count = int(watcher_count_str.strip())
            dates.append(date)
            watcher_counts.append(watcher_count)
        except ValueError:
            print("Invalid date or watcher count. Please make sure the format is MM/DD/YYYY and numbers are valid.")

    return dates, watcher_counts

# Function to generate interpolated data
def generate_interpolated_data(dates, watcher_counts, start_date, end_date):
    numerical_days = [(date - start_date).days for date in dates]
    interp_func = interpolate.interp1d(numerical_days, watcher_counts, kind='linear', fill_value='extrapolate')
    date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    estimated_watcher_counts = interp_func([(date - start_date).days for date in date_range])
    return date_range, estimated_watcher_counts

# Function to save data to CSV
def save_to_csv(date_range, estimated_watcher_counts, ticker):
    estimated_data = {'Date': date_range, 'Estimated Watcher Count': estimated_watcher_counts}
    df = pd.DataFrame(estimated_data)
    file_name = f'{ticker} Watcher Data.csv'
    df.to_csv(file_name, index=False)
    return file_name

# Function to create and save the line plot
def create_line_plot(date_range, estimated_watcher_counts, ticker):
    plt.figure(figsize=(10, 6))
    plt.plot(date_range, estimated_watcher_counts, color='blue', label='Interpolation')
    plt.xlabel('Date')
    plt.ylabel('Watcher Count')
    plt.legend()
    plot_title = f'Estimated Watcher Count Growth for ${ticker}'
    plt.title(plot_title)
    plt.tight_layout()
    plt.savefig(f'{ticker} Watcher Plot.png')

def main():
    print("Welcome to the Watcher Count Estimation Program!")

    # Get user input for the ticker symbol
    ticker = input("Enter the ticker symbol: ")

    # Get user input for dates and watcher counts
    dates, watcher_counts = get_dates_and_counts()

    # Get user input for the time frame
    start_date = min(dates)
    end_date = max(dates)
    print(f"Data available from {start_date.strftime('%Y')} to {end_date.strftime('%Y')}")
    target_start_date = datetime.strptime(input("Enter the start date of the desired time frame (MM/DD/YYYY): "), "%m/%d/%Y")
    target_end_date = datetime.strptime(input("Enter the end date of the desired time frame (MM/DD/YYYY): "), "%m/%d/%Y")

    # Generate and save interpolated data
    date_range, estimated_watcher_counts = generate_interpolated_data(dates, watcher_counts, target_start_date, target_end_date)
    csv_file_name = save_to_csv(date_range, estimated_watcher_counts, ticker)

    # Create and save the line plot
    create_line_plot(date_range, estimated_watcher_counts, ticker)

    print(f"Data has been generated and saved to '{csv_file_name}'. Line plot has been created and saved as '{ticker} Watcher Plot.png'.")

if __name__ == "__main__":
    main()
