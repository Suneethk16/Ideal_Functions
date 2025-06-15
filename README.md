# Python Project: Mapping Test Data to Ideal Functions

# Overview
This project processes training, ideal, and test data to:
Select the best ideal functions using least squares
Map test data points to those ideal functions
Save all results in a SQLite database
Visualize everything using Bokeh

# How to Run
1. Install required packages:
   pip3 install pandas numpy bokeh sqlalchemy

2. Run Main.py file
   python3 Main.py

3. Run Tests
   python3 -m unittest Unit_Test.py

# Technologies Used
   Python 3
   Pandas, NumPy
   Bokeh (for visualization)
   SQLAlchemy (for SQLite)
   unittest (for testing)

# Notes
   Test points are only mapped if their deviation from ideal functions is within the allowed threshold.
   All data is stored in functions.db.
   Results are shown in your browser.

# Creater
   SuneethKokala - StudentId