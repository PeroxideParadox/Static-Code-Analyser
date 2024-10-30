# calculate_footprint.py
import pandas as pd
from utils.footprint_helper import calculate_cpu_cycles, calculate_carbon_footprint

def main():
    data = pd.read_csv("dataset/labelled_dataset.csv")
    data['cpu_cycles'] = data['nested_loops'] * 1000 + data['inefficient_algorithms'] * 500
    data['carbon_footprint'] = data['cpu_cycles'].apply(calculate_carbon_footprint)
    data.to_csv("dataset/labelled_dataset.csv", index=False)

if __name__ == "__main__":
    main()
