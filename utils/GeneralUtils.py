import yaml

class GeneralUtils:
    """
    A utility class that provides general helper functions.
    Methods
    -------
    __init__():
        Initializes the GeneralUtils class.
    get_yaml_values(file_path):
        Reads a YAML file and retrieves specific values.
        Parameters:
        file_path (str): The path to the YAML file.
        Returns:
        dict: A dictionary containing the retrieved values.
        None: If the file is not found or there is an error parsing the YAML file.
    compare_dfs(df1, df2):
        Compares the columns of two DataFrames and prints the differences.
        Parameters:
        df1 (pandas.DataFrame): The first DataFrame.
        df2 (pandas.DataFrame): The second DataFrame.
    add_missing_cols(df1, df2):
        Adds missing columns from df1 to df2.
        Parameters:
        df1 (pandas.DataFrame): The first DataFrame.
        df2 (pandas.DataFrame): The second DataFrame.
        Returns:
        pandas.DataFrame: The second DataFrame with the missing columns added.
    """


    def __init__(self):
        """
        Initializes the instance of the class. Currently, this constructor does not perform any operations.
        """
        pass


    def get_yaml_values(sefl, file_path):
        """
        Reads a YAML file from the given file path and retrieves specific values.
        Args:
            file_path (str): The path to the YAML file.
        Returns:
            dict: A dictionary containing the retrieved values with keys:
                - "country_name" (str): The name of the country.
                - "ssp_input_file_name" (str): The name of the SSP input file.
                - "ssp_transformation_cw" (str): The SSP transformation CW value.
            None: If the file is not found or there is an error parsing the YAML file.
        Raises:
            FileNotFoundError: If the file is not found at the given file path.
            yaml.YAMLError: If there is an error parsing the YAML file.
        """

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
        """
        Compares the columns of two pandas DataFrames and prints the differences.
        Parameters:
        df1 (pandas.DataFrame): The first DataFrame to compare.
        df2 (pandas.DataFrame): The second DataFrame to compare.
        Returns:
        None
        Prints:
        - Columns present in df1 but not in df2.
        - Columns present in df2 but not in df1.
        """

        # Assuming your DataFrames are df1 and df2
        columns_df1 = set(df1.columns)
        columns_df2 = set(df2.columns)

        # Columns present in df1 but not in df2
        diff_in_df1 = columns_df1 - columns_df2

        # Columns present in df2 but not in df1
        diff_in_df2 = columns_df2 - columns_df1

        print("Columns in df1(example) but not in df2(yours):", diff_in_df1)
        print("Columns in df2(yours) but not in df1(example):", diff_in_df2)

    def add_missing_cols(self, df1, df2):
        """
        Add missing columns from one DataFrame to another.
        This method identifies columns that are present in the first DataFrame (df1)
        but not in the second DataFrame (df2), and adds those columns to df2 with 
        their corresponding values from df1.
        Parameters:
        df1 (pd.DataFrame): The DataFrame containing the columns to be added.
        df2 (pd.DataFrame): The DataFrame to which the missing columns will be added.
        Returns:
        pd.DataFrame: The updated DataFrame (df2) with the missing columns added.
        """
        # Identify columns in df1 but not in df2
        columns_to_add = [col for col in df1.columns if col not in df2.columns]

        # Check if there are any columns to add
        if not columns_to_add:
            print("No missing columns to add.")
            return df2

        # Add missing columns to df2 with their values from df1
        for col in columns_to_add:
            df2[col] = df1[col]
        
        return df2

