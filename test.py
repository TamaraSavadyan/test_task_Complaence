import csv
import chardet

def read_and_filter_csv(file_path, columns, sort_column):
    filtered_data = []
    
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        encoding = result['encoding']
        
    with open(file_path, 'r', encoding=encoding) as file:
        csv_reader = csv.reader(file)
        
        header = next(csv_reader)
        
        column_indices = [header.index(col) for col in columns]
               
        
        for row in csv_reader:
            filtered_row = [row[i] for i in column_indices]
            filtered_data.append(filtered_row)

        new_header = [header[i] for i in column_indices]
        sort_column_index = new_header.index(sort_column)
        
        filtered_data.sort(key=lambda x: x[sort_column_index], reverse=True)
        filtered_data.insert(0, new_header)
    
    return filtered_data

cols = ['TIME', 'NAME']
res = read_and_filter_csv('test.csv', cols, 'NAME')

print(res)

