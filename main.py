# main.py
import fetch_code_samples
import static_analysis
import calculate_footprint

def main():
    print("Fetching code samples...")
    fetch_code_samples.main()
    
    print("Running static analysis for code smells detection...")
    static_analysis.main()
    
    print("Calculating CPU and carbon footprints...")
    calculate_footprint.main()

    print("Process complete. Results saved to dataset/labelled_dataset.csv")

if __name__ == "__main__":
    main()
