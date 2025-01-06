### Date created
January 5, 2025

### Project Title
Bikeshare Analytics for Chicago, New York, and Washington (USA)

### Description
Bikeshare Analytics is an interactive data analysis tool that summarises key insights for bike share data from three USA cities (Chicago, New York and Washington). 

The tool displays usage trends to help identify:
- Bike-share demand 
- Service/support requirements
- Business/marketing opportunities
- Future planning and service optimisation/expansion needs

## How It Works

The user selects:
- **City**: Chicago, New York or Washington
- **Month**: All, Jan, Feb, Mar, Apr, May, Jun
- **Day**: All, Mon, Tue, Wed, Thu, Fri, Sat, Sun

The primary data outputs are:
- **Confirmation Header**: Displays selected city, month and day.
- **Ride Popularity Statistics**: Total rides, most common month and day, busiest hour and quietest hour (all with usage counts).
- **Station Statistics**: Most popular start/end stations, most popular route (start to end), with usage counts for each.
- **Trip Duration Statistics**: Total time for all trips, average time for all trips (h, m, s)
- **User Statistics**: Displays count and percentages of subscriber and customer, gender breakdown, birth years (earliest, latest, most common), and age calculations based on the current date 

## Example Output

Here is a condensed example of output generated for **New York**:

**City**: New York | **Month**: All | **Day**: All


- **Ride Popularity Statistics**

  Total Rides │ 300,000

  Most common month │ June (76,022 rides)
  Most common day   │ Wednesday (52,087 rides)
  Busiest hour      │ 17:00 (30,041 rides)

- **Station Statistics**

  Most Popular Stations:
  Start       │ Pershing Square North (3,069 rides)
  End         │ Pershing Square North (3,077 rides)

- **Trip Duration Statistics**

  Total Time  │ 74973h 40m 48s
  Average Time│ 0h 14m 59s

- **User Statistics**

  User Types:
  Subscriber  │ 269,149 (89.7%)
  Customer    │ 30,159 (10.1%)

  Subscriber gender:
  Male        │ 200,887 (75%)
  Female      │ 64,859 (24%)
  Unknown     │ 3,403 (1%)

  Subscriber birth year:
  Earliest    │ 1885 (current age: 140)

*Note: Processing time is displayed for each section.*

## Raw Data Viewing Option

Once the analysis completes, the user can view the raw data for their selection, displayed in chunks of 5 rows at a time. The user can request additional chunks of 5 rows until all data is displayed. This process can be stopped after each chunk. 

The tool ends with a final prompt asking if the user would like to restart the process. The restart prompt is triggered when:
- The user opts not to view the raw data
- The user finishes viewing all available raw data
- The user has already seen some raw data chunk and doesn't wish to see more

### Files used
- bikeshare.py
- chicago.csv
- new_york_city.csv
- washington.csv

### Credits

Python Documentation

- Python Documentation: Control Flow and Functions  
  https://docs.python.org/3/tutorial/controlflow.html#defining-functions

Stack Overflow

- Stack Overflow Python CSV Questions  
  https://stackoverflow.com/questions/tagged/csv+python
- General  
  https://stackoverflow.com

Real Python Articles & Tutorials

- Pandas DataFrame  
  https://realpython.com/pandas-dataframe/

- Explore a Dataset with Pandas  
  https://realpython.com/pandas-python-explore-dataset/

- Read and Write Files with Pandas  
  https://realpython.com/pandas-read-write-files/

- Python Pass By Reference  
  https://realpython.com/python-pass-by-reference/

- Defining Your Own Python Function  
  https://realpython.com/defining-your-own-python-function/

- Python Optional Arguments  
  https://realpython.com/python-optional-arguments/

