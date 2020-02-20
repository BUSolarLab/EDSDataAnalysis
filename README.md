# EDSDataAnalysis

## Overview
This project is a analytical tool to help analyze the data from the EDS Field Test Unit (FTU). The Field Test Unit has 3 modes:

- Manual Mode: manual measurements for one designated panel in the FTU triggered by a button.
- Noon Mode: automated daily measurements for all panels during solar noon time.
- Testing Mode: multiple automated daily measurements for all panels for testing purposes.

This GUI is made using tkinter, a python framework, which works on both Windows or Mac. The GUI essentially allows the user to take average data calculations based on the desired number of days (since the FTU only takes daily data, and getting 2-day/weekly/monthly average data is highly desirable)

## Graphical User Interface


## Getting Started
1. Clone the github repository
```
git clone https://github.com/BUSolarLab/EDSDataAnalysis.git
```
2. Install Dependancies
```
pip install -r requirements.txt
```
3. Run the desired script
For Windows:
```
python eds_analysis_windows.py
```
For Mac:
```
python eds_analysis_ios.py
```

## How To Use GUI:
1. Select the desired FTU CSV data file (manual_data.csv, testing_data.csv, or noon_data.csv).
2. Select the desired output location. The manipulated data will be saved as manual_sorted.csv, testing_sorted.csv, or noon_sorted.csv (depending on which mode was selected initially).
3. Input a valid average day in the input field
4. Click "Get Table" to manipulate the table
5. Click "Get Soiling Rate" to get the soiling rates of that mode
6. Click "Get Plot" to get the plot of that table. Plotting is only for Isc, Power, PR, and SR (please specify which metric to plot from the radio buttons).

## Notes
Testing Mode does not measure SR. Therefore, soiling rate and plotting will not be available for testing mode data.
