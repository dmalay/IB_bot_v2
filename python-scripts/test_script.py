import numpy as np
import pandas as pd

def analyze_data():
    data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    print("Sample Data:")
    print(data)
    print("\nSum of column A:", np.sum(data['A']))

if __name__ == "__main__":
    analyze_data()
