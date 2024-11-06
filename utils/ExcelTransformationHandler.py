import os
import pandas as pd
import yaml

"""
TODO:
    - The special cases aren't handled yet. We need to also multiply them by the scalar.
    - We need to scale the default values to its max default.
    - We need to also edit the yaml description.
    - We need to come upt with a better transformation name yaml parameter.
"""

class ExcelYAMLHandler:
    def __init__(self, excel_file, yaml_directory, sheet_name='yaml'):
        self.excel_file = excel_file
        self.sheet_name = sheet_name
        self.yaml_directory = yaml_directory
        self.data = self.load_excel_data()
    
    def load_excel_data(self):
        # Load the Excel sheet into a DataFrame
        try:
            df = pd.read_excel(self.excel_file, sheet_name=self.sheet_name)
            return df
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None
    
    def get_strategy_cols(self):
        # Get col names
        col_names = self.data.columns
       
        # return only strategy cols
        return [col for col in col_names if col.startswith('strategy')]
    
    def save_yaml_file(self, yaml_content, yaml_name, column, transformation_code, subsector, transformation_name, scalar_val):
        yaml_content['identifiers']['transformation_code'] = f'{transformation_code}_{column.upper()}'
        yaml_content['identifiers']['transformation_name'] = f'Scaled Default Max Parameters by {scalar_val} - {subsector}: {transformation_name}' # TODO Change this format
        new_yaml_name = f"{os.path.splitext(yaml_name)[0]}_{column}.yaml"
        new_yaml_path = os.path.join(self.yaml_directory, new_yaml_name)
        with open(new_yaml_path, 'w') as new_file:
            yaml.dump(yaml_content, new_file)
    
    def process_yaml_files(self):
        # Ensure that the data was loaded successfully
        if self.data is None:
            print("No data available to process.")
            return
        
        # Loop over each row in the DataFrame
        for _, row in self.data.iterrows():
            yaml_name = row['transformation_yaml_name']
            transformation_code = row['transformation_code']
            transformation_name = row['transformation_name']
            subsector = row['subsector']
            
            yaml_path = os.path.join(self.yaml_directory, yaml_name)

            if not os.path.exists(yaml_path):
                print(f"YAML file {yaml_name} not found in directory {self.yaml_directory}.")
                continue
            
            # Process each relevant column except 'transformation_yaml_name' and 'transformation_code'
            for column in self.get_strategy_cols():

                # This is the magnitude/scalar that we are going to multiply by the default max value in each yaml
                scalar_val = row[column] 

                # Skip if the value is NaN which means the transformation is not used for the strategy
                if pd.isna(scalar_val):
                    continue

                try:
                    # Load the original YAML file
                    with open(yaml_path, 'r') as file:
                        yaml_content = yaml.safe_load(file)
                    
                    # Checks for 'parameters' and 'magnitude'
                    # TODO: This will eventually be different we will multiply all by scalar val
                    if 'parameters' in yaml_content:
                        parameters = yaml_content['parameters']
                        if 'magnitude' not in parameters:
                            print(f"YAML file {yaml_name} for strategy {column} set to default because it does not have magnitude attribute")
                            self.save_yaml_file(yaml_content, yaml_name, column, transformation_code, subsector, transformation_name, scalar_val)
                            continue
                    else:
                        print(f"YAML file {yaml_name} for strategy {column} set to default because it does not have parameters attribute")
                        self.save_yaml_file(yaml_content, yaml_name, column, transformation_code, subsector, transformation_name, scalar_val)
                        continue
                    
                    # Update the 'magnitude' field if applicable
                    curr_magnitude = float(yaml_content['parameters']['magnitude'])
                    yaml_content['parameters']['magnitude'] = float(scalar_val) * curr_magnitude
                    
                    # Save the modified YAML file
                    self.save_yaml_file(yaml_content, yaml_name, column, transformation_code, subsector, transformation_name, scalar_val)
                except Exception as e:
                    print(f"Error processing file {yaml_name} for column {column}: {e}")

class StrategyUpdater:

    def __init__(self, yaml_dir):
        pass