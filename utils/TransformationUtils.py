import os
import pandas as pd
import yaml


class ExcelYAMLHandler:
    def __init__(self, excel_file, yaml_directory, sheet_name='yaml'):
        self.excel_file = excel_file
        self.sheet_name = sheet_name
        self.yaml_directory = yaml_directory
        self.data = self.load_excel_data()
    
    def load_excel_data(self):
        """
        Load the Excel sheet into a DataFrame.

        This method attempts to read an Excel file specified by the instance's
        `excel_file` attribute and load the data from the sheet specified by the
        `sheet_name` attribute into a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the data from the specified Excel sheet.
            None: If there is an error loading the Excel file, None is returned.

        Raises:
            Exception: If there is an error loading the Excel file, an exception is caught
                       and an error message is printed.
        """
        # Load the Excel sheet into a DataFrame
        try:
            df = pd.read_excel(self.excel_file, sheet_name=self.sheet_name)
            return df
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None
    
    def get_strategy_cols(self):
        """
        Retrieve column names that start with 'strategy'.
        This method filters the columns of the DataFrame stored in the `data` attribute
        and returns a list of column names that begin with the prefix 'strategy'.
        Returns:
            list: A list of column names that start with 'strategy'.
        """
        # Get col names
        col_names = self.data.columns
       
        # return only strategy cols
        return [col for col in col_names if col.startswith('strategy')]
    
    def save_yaml_file(self, yaml_content, yaml_name, column, transformation_code, subsector, transformation_name, scalar_val):
        """
        Save the given YAML content to a file with a modified name and updated identifiers.

        Args:
            yaml_content (dict): The content to be saved in the YAML file.
            yaml_name (str): The original name of the YAML file.
            column (str): The column name to be included in the transformation code and new file name.
            transformation_code (str): The transformation code to be included in the identifiers.
            subsector (str): The subsector to be included in the transformation name.
            transformation_name (str): The transformation name to be included in the identifiers.
            scalar_val (float): The scalar value to be included in the transformation name.

        Returns:
            None
        """
        yaml_content['identifiers']['transformation_code'] = f'{transformation_code}_{column.upper()}'
        yaml_content['identifiers']['transformation_name'] = f'Scaled Default Max Parameters by {scalar_val} - {subsector}: {transformation_name}' # TODO Change this format
        new_yaml_name = f"{os.path.splitext(yaml_name)[0]}_{column}.yaml"
        new_yaml_path = os.path.join(self.yaml_directory, new_yaml_name)
        with open(new_yaml_path, 'w') as new_file:
            yaml.dump(yaml_content, new_file)
    
    def get_transformations_per_strategy_dict(self):
        """
        Generates a dictionary of transformation codes for each strategy.

        This method retrieves strategy names and loads data from an Excel file.
        For each strategy, it creates a subset of the data containing transformation
        codes and the strategy column, removes rows with missing values, and formats
        the transformation codes by appending the strategy name in uppercase.
        The result is a dictionary where each key is a strategy name and the value
        is a list of formatted transformation codes.

        Returns:
            dict: A dictionary where keys are strategy names and values are lists
                  of formatted transformation codes.
        """

        transformations_per_strategy = {}
        strategy_names =  self.get_strategy_cols()
        df = self.load_excel_data()
        for strategy in strategy_names:
            subset_df = df[['transformation_code', strategy]]
            subset_df = subset_df.dropna()
            subset_transformation_codes = subset_df['transformation_code'].tolist()
            subset_transformation_codes = [f"{code}_{strategy.upper()}" for code in subset_transformation_codes]
            transformations_per_strategy[strategy] = subset_transformation_codes
        return transformations_per_strategy


    
    def process_yaml_files(self, overwrite_mult_param_transformations=True):
        """
        Processes YAML files based on the data loaded into the instance.
        This method iterates over each row in the DataFrame stored in `self.data`, 
        retrieves the corresponding YAML file, and updates its 'magnitude' parameter 
        based on the scalar values provided in the DataFrame. The updated YAML files 
        are then saved to the specified directory.
        The method performs the following steps:
        1. Checks if data is loaded; if not, prints a message and returns.
        2. Iterates over each row in the DataFrame.
        3. Constructs the path to the YAML file using the 'transformation_yaml_name' column.
        4. Checks if the YAML file exists; if not, prints a message and continues to the next row.
        5. For each relevant column (excluding 'transformation_yaml_name' and 'transformation_code'):
            a. Retrieves the scalar value from the DataFrame.
            b. Skips processing if the scalar value is NaN.
            c. Loads the YAML file.
            d. Checks for the presence of 'parameters' and 'magnitude' attributes.
            e. Updates the 'magnitude' attribute by multiplying it with the scalar value.
            f. Saves the modified YAML file.
        6. Handles exceptions and prints error messages if any issues occur during processing.
        Raises:
            Exception: If an error occurs while processing a YAML file.
        Note:
            This method assumes that the DataFrame `self.data` and the directory 
            `self.yaml_directory` are already set up in the instance.
        """
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
                            if overwrite_mult_param_transformations:
                                print(f"YAML file {yaml_name} for strategy {column} set to default because it does not have magnitude attribute")
                                self.save_yaml_file(yaml_content, yaml_name, column, transformation_code, subsector, transformation_name, scalar_val)
                                continue
                            else:
                                print(f"YAML file {yaml_name} for strategy {column} wasn't updated. Please check it manually.")
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

class StrategyCSVHandler:
    def __init__(self, csv_file, yaml_dir_path, yaml_mapping_file, transformation_per_strategy_dict):
        self.csv_file = csv_file
        self.data = self.load_csv()
        self.yaml_dir_path = yaml_dir_path
        self.yaml_mapping_file = yaml_mapping_file
        self.mapping = self.load_yaml_mapping()
        self.transformations_per_strategy_dict = transformation_per_strategy_dict
    
    def load_csv(self):
        """
        Loads a CSV file into a pandas DataFrame. If the file is not found, it creates an empty DataFrame with predefined columns.
        
        Returns:
            pd.DataFrame: DataFrame containing the CSV data or an empty DataFrame if the file is not found.
        
        Raises:
            FileNotFoundError: If the CSV file is not found.
            Exception: For any other exceptions that occur during the loading of the CSV file.
        """
        try:
            df = pd.read_csv(self.csv_file)
            # Convert 'strategy_id' to integers, handle any non-integer values
            df['strategy_id'] = pd.to_numeric(df['strategy_id'], errors='coerce')
            df['strategy_id'] = df['strategy_id'].fillna(0).astype(int)
            return df
        except FileNotFoundError:
            print(f"{self.csv_file} not found. Creating a new DataFrame.")
            columns = ['strategy_id', 'strategy_code', 'strategy', 'description', 'transformation_specification']
            return pd.DataFrame(columns=columns)
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return None

        
    def load_yaml_mapping(self):
        """
        Load the YAML mapping file and return the 'strategy_groups' section.

        This method attempts to open and read a YAML file specified by 
        `self.yaml_mapping_file`. If successful, it returns the 'strategy_groups' 
        section of the YAML file as a dictionary. If the file is not found or 
        another error occurs during the loading process, it prints an error 
        message and returns an empty dictionary.

        Returns:
            dict: The 'strategy_groups' section of the YAML file if successful, 
                  otherwise an empty dictionary.
        """
        try:
            with open(self.yaml_mapping_file, 'r') as file:
                mapping = yaml.safe_load(file)
            return mapping['strategy_groups']
        except FileNotFoundError:
            print(f"{self.yaml_mapping_file} not found.")
            return {}
        except Exception as e:
            print(f"Error loading YAML file: {e}")
            return {}
    
    def get_strategy_id(self, strategy_group):
        """
        Retrieve the next available strategy ID for a given strategy group.

        This method checks the existing strategy IDs for the specified strategy group
        and returns the next available ID within the defined range. If the strategy group
        is not recognized or the ID range is exceeded, a ValueError is raised.

        Parameters:
        strategy_group (str): The strategy group for which to retrieve the next ID.

        Returns:
        int: The next available strategy ID.

        Raises:
        ValueError: If the strategy group is unknown or the ID range is exceeded.
        """
        if strategy_group not in self.mapping:
            raise ValueError(f"Unknown strategy group: {strategy_group}")

        id_range = self.mapping[strategy_group]
        min_id, max_id = map(int, id_range.split('-'))
        existing_ids = self.data.loc[self.data['strategy_code'].str.startswith(strategy_group), 'strategy_id']

        # Ensure existing_ids is numeric
        existing_ids = pd.to_numeric(existing_ids, errors='coerce').dropna().astype(int)

        if existing_ids.empty:
            return min_id

        max_existing_id = existing_ids.max()
        next_id = max_existing_id + 1

        if next_id > max_id:
            raise ValueError(f"Exceeded ID range for {strategy_group}")

        return next_id
    
    def get_strategy_code(self, strategy_group, strategy_name):
        """
        Generates a strategy code by combining the strategy group and strategy name.
        Args:
            strategy_group (str): The group to which the strategy belongs.
            strategy_name (str): The name of the strategy.
        Returns:
            str: A string in the format "STRATEGY_GROUP:STRATEGY_NAME" where both parts are in uppercase.
        """
    
        return f"{strategy_group.upper()}:{strategy_name.upper()}"
    
    def get_transformation_specification(self, yaml_file_suffix):
        """
        Retrieves the transformation specification for a given strategy based on the provided YAML file suffix.
        This method searches for YAML files in the specified directory that match the given suffix,
        extracts transformation codes from these files, and filters them based on the strategy's
        transformation dictionary. The resulting transformation codes are concatenated into a single
        string separated by pipe symbols.
        Args:
            yaml_file_suffix (str): The suffix of the YAML files to search for.
        Returns:
            str: A string containing the filtered transformation codes separated by pipe symbols.
        """
       
        all_entries = os.listdir(self.yaml_dir_path)
        strategy_transformation_yamls = [file for file in all_entries if file.endswith(f'{yaml_file_suffix}.yaml')]
        transformation_codes = []
        
        for yaml_file in strategy_transformation_yamls:
            yaml_path = os.path.join(self.yaml_dir_path, yaml_file)
            # Open the yaml file
            with open(yaml_path, 'r') as file:
                yaml_content = yaml.safe_load(file)

            transformation_code = yaml_content['identifiers']['transformation_code']
            transformation_codes.append(transformation_code)
        
        # Filter the transformation_codes to only include the ones that are used in the strategy
        transformation_codes_filtered = [
            code for code in transformation_codes 
            if code in self.transformations_per_strategy_dict.get(f'strategy_{yaml_file_suffix}', [])
        ]
        # Join transformation codes with a pipe symbol, excluding the trailing one
        transformation_specification = '|'.join(transformation_codes_filtered)
        return transformation_specification

    def add_strategy(self, strategy_group, description, yaml_file_suffix, custom_id=None, update_flag=False):
        """
        Add or update a strategy in the dataset.
        Parameters:
        strategy_group (str): The group to which the strategy belongs.
        description (str): A description of the strategy.
        yaml_file_suffix (str): The suffix of the YAML file associated with the strategy.
        custom_id (int, optional): A custom ID for the strategy. Required if update_flag is True. Defaults to None.
        update_flag (bool, optional): Flag indicating whether to update an existing strategy. Defaults to False.
        Returns:
        None
        Raises:
        ValueError: If update_flag is True and custom_id is not provided.
        ValueError: If update_flag is True and custom_id does not exist in the dataset.
        ValueError: If custom_id is provided and already exists in the dataset.
        ValueError: If the generated strategy_code already exists in the dataset.
        """
        # Reload the data to ensure we have the latest version
        self.data = self.load_csv()

        # If update_flag is true then we update the current strategy
        if update_flag:
            # Check if custom_id is provided
            if custom_id is None:
                print("Error: custom_id is required for updating a strategy.")
                return
            # Check if the custom_id exists
            if custom_id not in self.data['strategy_id'].values:
                print(f"Error: strategy_id {custom_id} does not exist. Please provide a valid ID.")
                return
            
            # Get the index of the row to update
            idx = self.data.index[self.data['strategy_id'] == custom_id].tolist()[0]

            # Update the transformation_specification
            self.data.at[idx, 'transformation_specification'] = self.get_transformation_specification(yaml_file_suffix)

            self.save_csv()
            print(f"Updated row with strategy_id {custom_id}")
            return
        
        # Check if a custom ID was provided
        if custom_id is not None:
            if custom_id in self.data['strategy_id'].values:
                print(f"Error: strategy_id {custom_id} already exists. Please use a different ID or leave it to be auto-generated.")
                return
            strategy_id = custom_id
        else:
            strategy_id = self.get_strategy_id(strategy_group)

        # Generate the strategy_code and check for uniqueness
        strategy_code = self.get_strategy_code(strategy_group, yaml_file_suffix)
        if strategy_code in self.data['strategy_code'].values:
            print(f"Error: strategy_code {strategy_code} already exists. Please use a different code or eliminate the existing one.")
            return

        new_row = {
            'strategy_id': strategy_id,  # Keep as an integer
            'strategy_code': strategy_code,
            'strategy': yaml_file_suffix,
            'description': description,
            'transformation_specification': self.get_transformation_specification(yaml_file_suffix)
        }

        self.data = pd.concat([self.data, pd.DataFrame([new_row])], ignore_index=True)
        self.save_csv()
        print(f"Updated file with new row: {new_row}")
      


    
    def save_csv(self):
        # Save the DataFrame back to the CSV file
        try:
            self.data.to_csv(self.csv_file, index=False)
            print(f"Data saved to {self.csv_file}")
        except Exception as e:
            print(f"Error saving CSV file: {e}")
