"""
This program performs the following steps:
1. Loads training, ideal, and test datasets from CSV files.
2. Stores all datasets in a SQLite database.
3. Identifies the best-fitting ideal functions using least squares.
4. Maps test data to functions.
5. Stores the mapping results in the database.
6. Visualizes the data using Bokeh.
"""

import pandas as pd
from Database import database
from Processor import Process
from Visualization import graph

def main():
    """
    Main function:
    Reads CSV input files.
    Loads data into a database.
    Processes training and ideal functions to find the best match.
    Map test data to ideal functions.
    Stores and visualizes the data.
    """
    
    #Load CSVs
    traindataset = pd.read_csv("Data/train.csv")
    idealdataset = pd.read_csv("Data/ideal.csv")
    testdataset = pd.read_csv("Data/test.csv")

    #Save to database
    db = database()
    db.load_to_database(traindataset, "train_data")
    db.load_to_database(idealdataset, "ideal_functions")
    db.load_to_database(testdataset, "test_data")

    #Process and map
    processor = Process(traindataset, idealdataset, testdataset)
    selected = processor.idealfunctions()
    
    mappeddata, unmappedpoints = processor.mapdata(selected)

    if unmappedpoints:
        print(f"Unmapped points ({len(unmappedpoints)}): {unmappedpoints}")

    #Save mapped result
    db.load_to_database(mappeddata, "mapped test data")

    #Visualize
    graph(traindataset, mappeddata, idealdataset, selected)

if __name__ == "__main__":
    main()
