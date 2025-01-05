import os
import platform
import time
import pandas as pd
import numpy as np

# Clear the screen based on operating system
if platform.system() == "Windows":
    os.system('cls') # Clear screen if using Windows
else:
    os.system('clear') # Clear screen for Mac/Linux

# Constants for output text colour
BLUE = '\033[38;2;94;94;255m'       
GREEN = '\033[38;2;0;195;0m'        
MAGENTA = '\033[38;2;173;127;168m'  
RED = '\033[38;2;255;0;0m'
YELLOW = '\033[38;2;128;96;0m'               
ENDC = '\033[0m'                    

# Mapping city names to source files
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def get_filter_description(city, month, day):
    """
    Creates a consistent filter description string based on selected city, month, and day.

    Parameters:
        city (str): The name of the city (e.g., 'chicago', 'new york').
        month (str): The month selected (e.g., 'January', 'February', or 'all').
        day (str): The day selected (e.g., 'Monday', 'Tuesday', or 'all').

    Returns:
        str: A string summarizing the filter parameters in a readable format, 
             formatted as "City: <city> | Month: <month> | Day: <day>".
    """
    # Assumes that 'city', 'month' and 'day' are provided, because they are compulsory inputs (used for filtering and generating results).
    city_part = f"City: {city.title()} | "
    month_part = f"Month: {'All' if month == 'all' else month.title()}"
    day_part = f"Day: {'All' if day == 'all' else day.title()}"
    
    return f"{city_part}{month_part} | {day_part}"


def get_filters():
    """
    Prompts user input for city, month, and day preferences for filtering bikeshare data.
    Asks user to input a city (Chicago, New York, or Washington), a month (All, January, February, March, April, May, or June), 
    and a day (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday). The inputs are validated. Unsuitable inputs get a prompt to try again.

    Args:
        None
    
    Returns:
        tuple: A tuple containing three values:
            - city (str): The city selected by the user (e.g., "chicago", "new york", "washington").
            - month (str): The month selected by the user (e.g., "all", "january", "february", etc.).
            - day (str): The day selected by the user (e.g., "all", "monday", "tuesday", etc.).
    """
    print()
    print(f'{BLUE}Welcome to bikeshare analytics.{ENDC}')
    print()
    
    # Initialise city variable
    city = None
    while city is None:
        try:
            city_input = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
            print()
            # Validate city input (case-insensitive)
            if city_input in CITY_DATA:
                city = city_input
            else:
                print(f'{RED}Error: Invalid city input. Please choose Chicago, New York, or Washington.{ENDC}')
        except Exception as e:
            print(f'{RED}An error occurred: {e}. Please try again.{ENDC}')

    # Initialise and validate month input
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = None
    while month is None:
        try:
            month_input = input('Which month? All, January, February, March, April, May, or June?\n').lower()
            print()
            # Validate month input (case-insensitive)
            if month_input in valid_months:
                month = month_input
            else:
                print(f'{RED}Error: Invalid month option. Please try again.{ENDC}')
        except Exception as e:
            print(f'{RED}An error occurred: {e}. Please try again.{ENDC}')

    # Initialise and validate day input
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = None
    while day is None:
        try:
            day_input = input('Which day? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()
            # Validate day input (case-insensitive)
            if day_input in valid_days:
                day = day_input
            else:
                print(f'{RED}Error: Invalid day input.{ENDC}')
        except Exception as e:
            print(f'{RED}An error occurred: {e}. Please try again.{ENDC}')

    return city, month, day


def load_data(city, month, day):
    """
    Loads and filters data based on user selections.

    This function reads the appropriate CSV file, extracts relevant components from the 
    'Start Time' column (month, day of the week, and hour), and then filters 
    this data based on the user's preferences for month and day. It returns the filtered dataset.
    
    Args:
        city (str): City selected by user ('chicago', 'new york', 'washington')
        month (str): Month selected by user ('all', 'january', 'february', ..., 'june')
        day (str): Day selected by user ('all', 'monday', 'tuesday', ..., 'sunday')
        
    Returns:
        pandas.DataFrame: The filtered bikeshare data, with rows corresponding to the selected
                          month and day. If no data is found, or an error occurs, returns None.
    """
    # Letting the user know that analytics have commenced
    print()
    print(f'{BLUE}Loading your selected data...{ENDC}')
    print()
    
    try:
        # Load the relevant city data CSV file, based on user's selection
        df = pd.read_csv(CITY_DATA[city])
        # Convert time columns to datetime format for easier manipulation
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        
        # Extract 'month', 'day_of_week' and 'hour' from 'Start Time' column for filtering
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.day_name()
        df['hour'] = df['Start Time'].dt.hour

        # Filter by selected month (unless 'all')
        if month != 'all':
            # List of month names in lowercase for comparison
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            # Get numeric representation for month 
            month_num = months.index(month.lower()) + 1
            # Filter dataframe records by selected month.
            df = df[df['month'] == month_num]
        
        # Filter by selected day (unless 'all') 
        if day != 'all':
            # Filter dataframe to only include records for the selected day.
            df = df[df['day_of_week'].str.lower() == day.lower()]
        
        # Return the filtered dataframe
        return df
    
    except FileNotFoundError as e:
        # Print error message if city data file is missing
        print(f'{RED}Error loading data: {e}{ENDC}')
        return None

    except Exception as e:
        # Handle unexpected errors
        print(f'{RED}An unexpected error occurred: {e}{ENDC}')
        return None


def display_header(city, month, day):
    """Displays the report header with filter selections."""
    
    # Use helper function to get formatted status line
    status_line = get_filter_description(city, month, day)
    
    # Print the status line and separator
    print(status_line)
    print('-' * len(status_line))
    print()


def display_ride_stats(df):
    """
    Displays ride statistics for the filtered data:
        - Total rides
        - Busiets and quietest hours
        - Calculation time
    
    Args:
        df (pandas.DataFrame): Filtered data

    Returns:
        None
    """
    # Start timer for calculations
    start_time = time.time()
    
    # Section heading
    print(f'{GREEN}Ride Count Statistics{ENDC}')
    print()
    
    # Subheading for ride count
    print(f'Total Rides │ {len(df):,}')
    print()
    
    # Subheading for hour
    print('Hours:')
    hourly_rides = df['hour'].value_counts().sort_index()
    busiest_hour = hourly_rides.idxmax()
    quietest_hour = hourly_rides.idxmin()
    
    # Display the hour data
    print(f'Busiest     │ {busiest_hour:02d}:00 ({hourly_rides[busiest_hour]:,} rides)')
    print(f'Quietest    │ {quietest_hour:02d}:00 ({hourly_rides[quietest_hour]:,} rides)')
    
    # Stop timer and display the calculation time (3 decimals)
    print()
    print(f'{MAGENTA}Calculation time: {time.time() - start_time:.3f}s{ENDC}')
    print()


def display_station_stats(df):
    """
    Displays station statistics for the filtered data:
        - Most popular start and end stations
        - Most popular route (start and end station)
        - Calculation time
    
    Handles missing data by excluding NaN values in the station columns. The most popular
    route is calculated by combining the 'Start Station' and 'End Station' columns and finding
    the most frequent combination.

    Args:
        df (pandas.DataFrame): Filtered data containing 'Start Station' and 'End Station' columns.

    Returns:
        None
    """
    start_time = time.time()
    
    print(f'{GREEN}Station Statistics{ENDC}')
    print()

    print('Most Popular Stations:')
    start_station_counts = df['Start Station'].dropna().value_counts() # NaN handling
    end_station_counts = df['End Station'].dropna().value_counts() # Nan handling
    
    print(f'Start       │ {start_station_counts.index[0]} ({start_station_counts.iloc[0]:,} rides)')
    print(f'End         │ {end_station_counts.index[0]} ({end_station_counts.iloc[0]:,} rides)')
    print()
    
    # Calculate most popular route by combining start and end stations (with NaN handling)
    route_series = df['Start Station'].dropna() + ' to ' + df['End Station'].dropna()
    popular_route = route_series.mode()[0]
    route_count = route_series.value_counts().iloc[0]
    
    print('Most Popular Route:')
    print(f'{popular_route} ({route_count:,} rides)')
    
    # Stop timer and display the calculation time (3 decimals)
    print()
    print(f'{MAGENTA}Calculation time: {time.time() - start_time:.3f}s{ENDC}')
    print()


def format_time(seconds):
    """
    Converts total seconds to a time string format showing all time units (hours, minutes, seconds).
    
    Args:
        seconds (float): Time duration in seconds
    
    Returns:
        str: Formatted string as 'Xh Ym Zs' (always includes all time units; e.g., '1h 6m 10s').
    """
    seconds = abs(int(seconds))  # Convert to integer to handle negative values and convert floats
    
    # Calculate hours, minutes and remaining seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    # Returns formatted string as hours, minutes and seconds.
    return f'{hours}h {minutes}m {seconds}s'


def display_trip_duration_stats(df):
    """
    Displays trip duration statistics for the filtered dataframe.
    
    Args:
        df (pandas.DataFrame): Filtered data

    Returns:
        None
    """
    # Start timer for calculations
    start_time = time.time()
    
    # Heading for trip duration statistics section
    print(f'{GREEN}Trip Duration Statistics{ENDC}')
    print()
    
    # Calculate total and average trip durations from the 'Trip Duration' column
    total_duration = df['Trip Duration'].sum()
    avg_duration = df['Trip Duration'].mean()
    
    # Display the total and average trip durations using formatted time
    print(f'Total Time  │ {format_time(total_duration)}')
    print(f'Average Time│ {format_time(avg_duration)}')
    
    # Stop timer and display the calculation time (3 decimals)
    print()
    print(f'{MAGENTA}Calculation time: {time.time() - start_time:.3f}s{ENDC}')
    print()


# Import datetime to calculate age of users, based on current year
from datetime import datetime


def display_user_stats(df):
    """
    Displays user statistics for the filtered data.
    
    Args:
        df (pandas.DataFrame): Filtered data: 'User Type', 'Gender' and 'Birth Year'.

    Returns:
        None
    """
    # Start timer for calculations
    start_time = time.time()
    
    # Print heading for user statistics section.
    print(f'{GREEN}User Statistics{ENDC}')
    print()
    
    # Calculate total users
    total_users = len(df)
    
    # Display user types count and percentage. 
    user_types = df['User Type'].value_counts()
    print('User Types:')
    for user_type, count in user_types.items():
        percentage = (count / total_users) * 100
        print(f'{user_type:<10}  │ {count:,} ({percentage:.1f}%)')
    print()
    
    # Check if 'Gender' or 'Birth Year' columns exist to determine if subscriber data is available.
    has_subscriber_data = 'Gender' in df.columns or 'Birth Year' in df.columns
    if has_subscriber_data:
        subscriber_df = df[df['User Type'] == 'Subscriber']
        subscriber_total = len(subscriber_df)
    
    # Gender (if available - subscriber data only)
    if 'Gender' in df.columns:
        # Filter to only look at subscriber data
        subscriber_df = df[df['User Type'] == 'Subscriber']
        gender_counts = subscriber_df['Gender'].value_counts(dropna=False)
        subscriber_total = len(subscriber_df)
        
        # Managing missing gender data so the user understands why it's not being presented
        if gender_counts.empty:
            print(f'{YELLOW}* Subscriber gender data missing/unavailable for your selection{ENDC}')
        else:
            # Subheading for the gender, highlighting it is for subscribers only
            print('Subscriber gender:')
            for gender in gender_counts.index: # Iterate through all gender categories in the index
                count = gender_counts[gender] # Get total for current gender
                percentage = (count / subscriber_total) * 100 # Calculate percentage total for this gender
                gender_display = 'Unknown' if pd.isna(gender) else gender # Replace NaN with 'unknown' if needed
                print(f'{gender_display:<10}  │ {count:,} ({percentage:.0f}%)') # Display gender, count and percentage
            print()
    else:
        print(f'{YELLOW}* Subscriber gender data missing/unavailable for your selection{ENDC}')
    
    # Birth Year (if available - subscriber data only)
    if 'Birth Year' in df.columns:
        subscriber_birth_years = df[df['User Type'] == 'Subscriber']['Birth Year'].dropna()
        
        # Managing missing birth year data so the user understands why it's not being presented
        if subscriber_birth_years.empty:
            print(f'{YELLOW}* Subscriber birth year data missing/unavailable for your selection{ENDC}')
        else:
            print('Subscriber birth year:')
            earliest = int(subscriber_birth_years.min())
            latest = int(subscriber_birth_years.max())
            common = int(subscriber_birth_years.mode()[0])
            current_year = datetime.now().year
            print(f'Earliest    │ {earliest} (current age: {current_year - earliest})')
            print(f'Latest      │ {latest} (current age: {current_year - latest})')
            print(f'Most Common │ {common} (current age: {current_year - common})')
    else:
        print(f'{YELLOW}* Subscriber birth year data missing/unavailable for your selection{ENDC}')

    # Stop timer and display the calculation time (3 decimals)
    print()
    print(f'{MAGENTA}Calculation time: {time.time() - start_time:.3f}s{ENDC}')
    print()


# Add tabulate for neater CSV data display
from tabulate import tabulate


def display_raw_data(df, city, month, day):
    """
    Displays raw data from the DataFrame filtered by city, month, and day.
    """
    # Get complete filter description
    filter_description = get_filter_description(city, month, day)
    
    print(f'{GREEN}Raw data is available for your selection ({filter_description}).{ENDC}')
    print()

    # Define columns to display (exclude non-raw columns)
    original_columns = [col for col in df.columns if col not in ['month', 'day_of_week', 'hour']]
    

    def get_yes_no_input(prompt):
        """
        Function to ensure valid 'yes' or 'no' input from the user.

        Args:
            prompt (str): The message displayed to the user when asking for input.

        Returns:
            bool: 
                - True if the user responds with 'yes' or 'y'.
                - False if the user responds with 'no' or 'n'.
        """
        while True:
            response = input(prompt).strip().lower() # Prompt for input
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print(f'{RED}Error: Invalid input. Please enter "yes" or "no"{ENDC}')

    # Ask if user wants to view the raw data
    if get_yes_no_input('Would you like to view the raw data? [yes/no]: '):
        # Initiliase variable start_idx 
        start_idx = 0
        while start_idx < len(df):
            # Prepare table data in chunks of 5
            chunk_end = min(start_idx + 5, len(df))
            current_chunk = df.iloc[start_idx:chunk_end]
            table_data = current_chunk[original_columns].fillna('').astype(str).values.tolist()

            # Print the table using tabulate
            print(tabulate(table_data, headers=original_columns, tablefmt="fancy_grid", numalign="left", stralign="left"))

            start_idx += 5
            # Check that there are rows of data still available, or if the user wants to stop
            if start_idx < len(df) and not get_yes_no_input('\nWould you like to see 5 more rows? [yes/no]: '):
                break # exit loop if no further data, or user wants to stop


def main():
    """
    Main function to run the bikeshare analysis program.
    
    This function handles user input for selecting city, month, and day filters,
    loads the corresponding data, displays various statistics (ride, stations, etc.),
    and allows the user to view raw data. It also offers the option to restart.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        if df is not None:
            display_header(city, month, day)
            display_ride_stats(df)
            display_station_stats(df)
            display_trip_duration_stats(df)
            display_user_stats(df)
            display_raw_data(df, city, month, day)
        
        # Display end of session message
        print()
        print(f'{BLUE}End of session{ENDC}')
        print()
        
        # Restart prompt with non-case-senstive input
        restart = input('Would you like to restart? [yes/no]: ').lower()
        # Unexpected input warning and prompt
        while restart not in ['yes', 'no', 'y', 'n']:
            print(f'{RED}Error: Invalid input. Please enter "yes" or "no"{ENDC}')
            restart = input('Would you like to restart? [yes/no]: ').lower()
        
        if not restart.startswith('y'):
            break # If 'no' then stop
        print('\n' * 2)

if __name__ == "__main__":
    main()