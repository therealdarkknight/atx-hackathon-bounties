import pandas as pd
import json

def create_exporter_dict_with_pandas(csv_file_path):
    # Read the CSV file with Pandas
    # Using engine='python' or specifying quotechar can help if there are unusual quoting issues
    df = pd.read_csv(csv_file_path)
    
    # If your headers still contain extra quotes, strip them out:
    # df.columns = [col.strip('"') for col in df.columns]
    
    # Create a dictionary keyed by 'Exporter Name'
    exporter_dict = {}
    for _, row in df.iterrows():
        # Convert the row (a Pandas Series) into a dict
        row_data = row.to_dict()
        
        # Get the exporter name and remove it from the dictionary
        exporter_name = row_data.get("Record ID")
        if exporter_name:
            del row_data["Record ID"]
            exporter_dict[exporter_name] = row_data
    
    return exporter_dict

if __name__ == "__main__":
    csv_file_path = "../data/traceability_data.csv"
    result_dict = create_exporter_dict_with_pandas(csv_file_path)
    print(json.dumps(result_dict, indent=2, ensure_ascii=False))
