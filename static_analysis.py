# static_analysis.py
import os
import pandas as pd
from utils.labelling_helper import detect_code_smells_ast

def main():
    directory = "dataset/raw_code_samples/"
    labelled_data = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, "r") as f:
                code = f.read()
            smells = detect_code_smells_ast(code)
            labelled_data.append({"filename": filename, **smells})

    # Save results to CSV
    df = pd.DataFrame(labelled_data)
    df.to_csv("dataset/labelled_dataset.csv", index=False)

if __name__ == "__main__":
    main()
