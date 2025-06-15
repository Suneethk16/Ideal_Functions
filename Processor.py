import numpy as np
import pandas as pd
from Exceptions import FunctionMappingError

class SetOfFunction:
    """
    Base class represents set of functions defined over x-values.
    """
    def __init__(self, dataframe):
        """
        Initializes the function set with a DataFrame.
        """
        self.df = dataframe
        self.x = dataframe['x']


class Process(SetOfFunction):
    """
    Process training, ideal, and test data to identify best matching functions and map test data.
    Inherits from SetOfFunction.
    """

    def __init__(self, traindataset, idealdataset, testdataset):
        """
        Initializes the processor with training, ideal, and test data.
        """
        super().__init__(traindataset)
        self.traindataset = traindataset
        self.idealdataset = idealdataset
        self.testdataset = testdataset
        self.max_deviations = {}

    def idealfunctions(self):
        """
        Selects the ideal function for each training column based on least squares error.
        For each training column y1 to y4, the ideal function with the smallest squared error is chosen.
        Returns dictionary.
        """
        selected = {}
        for i in range(1, 5):
            y_train = self.traindataset[f'y{i}']
            min_error = float('inf')
            best_func = None
            for col in self.idealdataset.columns[1:]:
                error = np.sum((y_train - self.idealdataset[col])**2)
                if error < min_error:
                    min_error = error
                    best_func = col
            selected[f'y{i}'] = best_func
            self.max_deviations[best_func] = np.max(np.abs(self.traindataset[f'y{i}'] - self.idealdataset[best_func]))
        return selected

    def mapdata(self, selected):
        """
        Maps each test point to the closest ideal function if deviation is within threshold.
        The test point is mapped:
            y_test - y_ideal <= max_deviation_train * sqrt(2)
        Returns tuples.
        """
        mapping_results = []
        unmappedpoints = []

        for _, row in self.testdataset.iterrows():
            x, y = row['x'], row['y']
            mapped = False

            for train_func, ideal_func in selected.items():
                try:
                    ideal_y = self.idealdataset.loc[self.idealdataset['x'] == x, ideal_func].values[0]
                    delta_y = abs(y - ideal_y)
                    threshold = self.max_deviations[ideal_func] * np.sqrt(2)

                    if delta_y <= threshold:
                        mapping_results.append({
                            'x': x,
                            'y': y,
                            'delta_y': delta_y,
                            'ideal_func': ideal_func
                        })
                        mapped = True
                        break

                except IndexError:
                    continue  

            if not mapped:
                unmappedpoints.append((x, y))

        mappeddata = pd.DataFrame(mapping_results)
        return mappeddata, unmappedpoints
