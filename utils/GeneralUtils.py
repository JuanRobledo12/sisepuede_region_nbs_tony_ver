import yaml

class GeneralUtils:

    def __init__(self):
        pass


    def get_yaml_values(sefl, file_path):
        try:
            # Open and load the YAML file
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
            
            # Retrieve the specific values
            country_name = data.get("country_name", "Not found")
            ssp_input_file_name = data.get("ssp_input_file_name", "Not found")
            ssp_transformation_cw = data.get("ssp_transformation_cw", "Not found")
            
            # Print the values
            print("Country Name:", country_name)
            print("SSP Input File Name:", ssp_input_file_name)
            print("SSP Transformation CW:", ssp_transformation_cw)
            
            # Return the values as a dictionary
            return {
                "country_name": country_name,
                "ssp_input_file_name": ssp_input_file_name,
                "ssp_transformation_cw": ssp_transformation_cw
            }
        
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return None
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return None

    # Example usage
    if __name__ == "__main__":
        yaml_file_path = "path_to_your_file.yaml"  # Replace with the actual file path
        result = get_yaml_values(yaml_file_path)

        
    def compare_dfs(self, df1, df2):
        # Assuming your DataFrames are df1 and df2
        columns_df1 = set(df1.columns)
        columns_df2 = set(df2.columns)

        # Columns present in df1 but not in df2
        diff_in_df1 = columns_df1 - columns_df2

        # Columns present in df2 but not in df1
        diff_in_df2 = columns_df2 - columns_df1

        print("Columns in df1 but not in df2:", diff_in_df1)
        print("Columns in df2 but not in df1:", diff_in_df2)

    def add_missing_cols(self, df1, df2):
        # Identify columns in df1 but not in df2
        columns_to_add = [col for col in df1.columns if col not in df2.columns]

        # Add missing columns to df2 with their values from df1
        for col in columns_to_add:
            df2[col] = df1[col]
        
        return df2

