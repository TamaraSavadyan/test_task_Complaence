from chardet import detect

contents = 'file contents'
encoding = detect(contents)['encoding']
file_content = contents.decode(encoding)

columns = ['NAME', 'Mw']
file = 'test.csv'


