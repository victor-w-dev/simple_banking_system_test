import csv
from io import StringIO
import time
from collections import deque

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.6f} seconds.")
        return result
    return wrapper

class CSVLastRowExtractor:
    """
    A class to extract the last row from a CSV file using a byte-level method.
    
    Methods
    -------
    get_last_line(file_path)
        Reads the last line of the file using byte operations.
    
    extract_last_rows(file_path, columns)
        Extracts the last row's values for the specified columns.
    """
    @classmethod
    @timer
    def get_last_line(cls, file_path):
        """
        Reads the last line of a file by seeking to the end and moving backwards.
        """
        with open(file_path, 'rb') as f:
            f.seek(0, 2)  # Move to the end of the file
            filesize = f.tell()
            offset = -100  # Start reading from the last 100 bytes
            while True:
                if filesize + offset > 0:
                    f.seek(offset, 2)
                    lines = f.readlines()
                    if len(lines) >= 2:  # Ensure we have a complete last line
                        # print(f"need offset: {offset}")
                        # print(f"line: {lines[-1].decode().strip()}")
                        return lines[-1].decode().strip()
                offset *= 2  # Increase offset if the last line is not foundss

    @classmethod
    def extract_last_rows(cls, file_path, columns):
        """
        Extracts the last row's values for the specified columns.
        
        Parameters
        ----------
        file_path : str
            The path to the CSV file.
        columns : list
            A list of column names to extract from the last row.
            
        Returns
        -------
        list
            A list of values from the specified columns in the last row.
        """
        if not columns or not isinstance(columns, list):
            raise ValueError("Columns must be a non-empty list.")
        
        # Get header
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader, None)
            if header is None:
                raise ValueError(f"File {file_path} is empty or has no header")
        
        # Get last line
        last_line = cls.get_last_line(file_path)
        if not last_line:
            raise ValueError(f"File {file_path} has no data rows")
        
        # Parse last line as CSV
        reader = csv.reader(StringIO(last_line))
        last_row = next(reader)
        
        try:
            indices = [header.index(column) for column in columns]
            return [last_row[index] for index in indices]
        except ValueError as e:
            missing = set(columns) - set(header)
            raise ValueError(f"Columns not found in CSV {file_path}: {missing}") from e
            
    # below is CSV Reader with Deque with Time complexity O(n), space complexity O(1)
    # Time complexity O(n) 
    # as csv.reader object reads the file sequentially from beginning before parsing to deque
    # which is slow than byte-level method as above
    
    # @classmethod
    # @timer
    # def _read_file(cls, file_path):
    #     with open(file_path, 'r') as file:
    #         reader = csv.reader(file)
    #         header = next(reader)
    #         last_row = deque(reader, maxlen=1).pop()
    #     return header, last_row

    # @classmethod
    # def extract_last_rows(cls, file_path, columns):
    #     """
    #     Extracts the last row's values for the specified columns.
        
    #     Parameters
    #     ----------
    #     file_path : str
    #         The path to the CSV file.
    #     columns : list
    #         A list of column names to extract from the last row.
            
    #     Returns
    #     -------
    #     list
    #         A list of values from the specified columns in the last row.
    #     """
    #     header, last_row = cls._read_file(file_path)
        
    #     # Find the indices of the desired columns
    #     indices = [header.index(column) for column in columns]
        
    #     # Extract the desired columns
    #     extracted_values = [last_row[index] for index in indices]
        
    #     return extracted_values

# For testing
if __name__ == "__main__":
    try:
        result = CSVLastRowExtractor.extract_last_rows('1_transactions.csv', ['transaction_id', 'amount'])
        print(f"Extracted values: {result}")
    except Exception as e:
        print(f"Error: {e}")