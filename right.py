import csv
import json
import shutil

objects = {}

def process_row(row):
    key = row[1]
    parent_key = row[2]
    rights_value = row[3]
    if not parent_key and rights_value != 'No':
        objects.setdefault(key, {'Rights': set(), 'Parent': set()}) # Use setdefault to simplify code
        objects[key]['Rights'].add(row[1]) # Fix: add row[1] instead of key
    elif parent_key and parent_key != key:
        objects.setdefault(key, {'Rights': set(), 'Parent': set()}) # Use setdefault to simplify code
        objects[key]['Parent'].add(parent_key)

def add_parent_items(key, parent):
    if isinstance(parent, set):
        for x in parent:
            parent_key = x
            try:
                objects[key]['Rights'].update(objects[parent_key]['Rights']) # Fix: use parent_key instead of parent

                if objects[parent_key]['Parent']:
                    add_parent_items(key, objects[parent_key]['Parent']) # Fix: use parent_key instead of parent
            except KeyError:
                #print('Key error encountered for parent:', key, parent)
                            pass
    else:
        try:
            if isinstance(parent, str):
                objects[key]['Rights'].update(objects[parent]['Rights'])

            if objects[parent]['Parent']:
                add_parent_items(key, objects[parent]['Parent'])

        except KeyError:
            pass
            #print('Key error encountered for parent:', key, parent)


with open('File.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        process_row(row)
print([objects['Near Miss']])
print([objects['Incident']])
test6 = [objects['Near Miss']]
test7 = [objects['Incident']]

for key in objects:
    if objects[key]['Parent']:
        for parent in objects[key]['Parent']:
            add_parent_items(key, parent)
print([objects['Near Miss']])
print([objects['Incident']])
test = [objects['Near Miss']]
test2 = [objects['Incident']]

original_file_path = 'File.csv'


copied_file_path = 'File2.csv'


shutil.copyfile(original_file_path, copied_file_path)


with open(copied_file_path) as csv_file:
    reader = csv.reader(csv_file)
    next(reader)

    for row in reader:
        if row[5] != 'FALSE' and not (row[4].startswith("Workflo") and not row[4].startswith("Employe") and not row[4].startswith("Subjec") and not row[4].startswith("Locatio")):
            try:
                objects[row[1]]['Rights'].update(objects[row[4]]['Rights'])
                #print("Object :", row[1], " Added : ", row[4])
            except KeyError:
                #print("KEY ERROR On last loop ",row[1], row[4] )
                            pass

for key in objects:
    if objects[key]['Parent']:
        for parent in objects[key]['Parent']:
            add_parent_items(key, parent)


#test3 = [objects['Near Miss']]
#test4 = [objects['Incident']]

for key in objects:
    objects[key]['Parent'] = list(objects[key]['Parent'])
    objects[key]['Rights'] = list(objects[key]['Rights'])

#print([objects['Near Miss']])
#print([objects['Incident']])



with open('objects2.txt', 'w') as convert_file:
    convert_file.write(json.dumps(objects))
