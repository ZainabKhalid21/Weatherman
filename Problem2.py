import os
import pandas as pd
from colorama import Fore, Style

def load_data(city, year):
    folder_path = f"C:/Users/DELL/Desktop/P2-weatherman/{city}_weather"
    all_data = []
    date_columns = ['PKT', 'PKST', 'GST']  
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt') and str(year) in file:
                file_path = os.path.join(root, file)
                # Find the matching date column
                data = None
                for date_column in date_columns:
                    try:
                        data = pd.read_csv(
                            file_path, skip_blank_lines=True, skipfooter=1, engine='python')
                        if date_column in data.columns:
                            break
                    except pd.errors.ParserError:
                        # If the date_column is not found, try the next one
                        continue
                if data is not None:
                    data['Date'] = pd.to_datetime(data[date_column])
                    all_data.append(data)
    if not all_data:
        raise ValueError(
            f"No valid data files found for {city} in year {year}.")
    
    return pd.concat(all_data, ignore_index=True)

def extract_data_for_year(data, year):
    data['Date'] = pd.to_datetime(data['Date'])
    return data[data['Date'].dt.year == year]

def extract_data_for_month(data, year, month):
    data['Date'] = pd.to_datetime(data['Date'])
    return data[(data['Date'].dt.year == year) & (data['Date'].dt.month == month)]

def draw_horizontal_bar_chart(data, title):
    data.loc[:, 'Day'] = data['Date'].dt.day
    data.loc[:, 'DayStr'] = data['Day'].apply(lambda x: f"{x:02d}")

    for _, row in data.iterrows():
        highest_temp = row['Max TemperatureC']
        lowest_temp = row['Min TemperatureC']

        # Handle NaN values for highest_temp and lowest_temp
        if pd.notna(highest_temp):
            highest_temp_color = Fore.RED + '+' * int(highest_temp) + Style.RESET_ALL
        else:
            highest_temp_color = Fore.RED + '+'
        if pd.notna(lowest_temp):
            lowest_temp_color = Fore.BLUE + '+' * int(lowest_temp) + Style.RESET_ALL
        else:
            lowest_temp_color = Fore.BLUE + '+'

        if (pd.notna(highest_temp) and pd.notna(lowest_temp) ):

            print(f"{row['DayStr']} {highest_temp_color} {highest_temp:.0f}C")
            print(f"{row['DayStr']} {lowest_temp_color} {lowest_temp:.0f}C")



def generate_report_for_given_year(data, year):
    year_data = extract_data_for_year(data, year)
    highest_temp_row = year_data.loc[year_data['Max TemperatureC'].idxmax()]
    lowest_temp_row = year_data.loc[year_data['Min TemperatureC'].idxmin()]
    humid_row = year_data.loc[year_data['Max Humidity'].idxmax()]

    highest_temp = highest_temp_row['Max TemperatureC']
    highest_temp_day = highest_temp_row['Date']

    lowest_temp = lowest_temp_row['Min TemperatureC']
    lowest_temp_day = lowest_temp_row['Date']

    highest_humidity = humid_row['Max Humidity']
    highest_humidity_day = humid_row['Date']

    print(f"Highest: {highest_temp}C on {highest_temp_day}")
    print(f"Lowest: {lowest_temp}C on {lowest_temp_day}")
    print(f"Humid: {highest_humidity}% on {highest_humidity_day}")

def generate_report_for_given_month(data, year, month):
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May','Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_abbr = month[:3].capitalize()

    if month_abbr not in month_names:
        raise ValueError("Invalid month input.")
    month_num = month_names.index(month_abbr) + 1

    month_data = extract_data_for_month(data, year, month_num)
    print(f"{month} {year}")

    # Functionality 3
    draw_horizontal_bar_chart(month_data, f"{month} {year}")

    # Bonus Functionality 4
    for day in range(1, 32):  # Assuming at most 31 days in a month
        day_data = month_data[month_data['Date'].dt.day == day]
        if len(day_data) > 0:
            highest_temp = day_data['Max TemperatureC'].max()
            lowest_temp = day_data['Min TemperatureC'].min()
            highest_temp = highest_temp if not pd.isna(highest_temp) else -99
            lowest_temp = lowest_temp if not pd.isna(lowest_temp) else -99
            highest_temp_color = Fore.RED + '+' * int(highest_temp - lowest_temp) + Style.RESET_ALL
            lowest_temp_color = Fore.BLUE + '+' * int(highest_temp - lowest_temp) + Style.RESET_ALL
            print(f"{day:02d}{highest_temp_color}{lowest_temp_color} {lowest_temp:.0f}C-{highest_temp:.0f}C")

    avg_highest_temp = month_data['Max TemperatureC'].max()
    avg_lowest_temp = month_data['Min TemperatureC'].min()
    avg_humidity = month_data['Max Humidity'].mean()

    print(f"\nAverage Highest: {avg_highest_temp:.2f}C")
    print(f"Average Lowest: {avg_lowest_temp:.2f}C")
    print(f"Average Humidity: {avg_humidity:.2f}%")

if __name__ == "__main__":
    city = input("Enter the city (Dubai, Lahore, Murree): ").strip().lower()
    year = int(input("Enter the year: ").strip())

    data = load_data(city, year)
    option = input(
        "Do you want to generate a report for a specific month? (yes/no): ").strip().lower()

    if option == 'yes':
        month = input("Enter the month (e.g., Jan, Feb, Mar): ").strip()
        generate_report_for_given_month(data, year, month)
    else:
        generate_report_for_given_year(data, year)
