import yaml
from passlib.context import CryptContext
import csv
import chardet

def load_config():
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
        return config
    

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def read_and_filter_csv(default_file, columns, sort_column='', sort_type='ASC'):
    filtered_data = []
    
    with open(default_file, 'rb') as file:
        result = chardet.detect(file.read())
        encoding = result['encoding']
        
    with open(default_file, 'r', encoding=encoding) as file:
        csv_reader = csv.reader(file)
        
        header = next(csv_reader)
        
        column_indices = [header.index(col) for col in columns]
        
        for row in csv_reader:
            filtered_row = [row[i] for i in column_indices]
            filtered_data.append(filtered_row)

        filtered_header = [header[i] for i in column_indices]
        if sort_column:
            sort_column_index = filtered_header.index(sort_column)
            if sort_type == 'ASC':
                to_reverse = False     
            else:
                to_reverse = True
            filtered_data.sort(key=lambda x: x[sort_column_index], reverse=to_reverse)

        filtered_data.insert(0, filtered_header)
    
    return filtered_data