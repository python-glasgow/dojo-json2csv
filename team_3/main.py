# import requests

# data_url = 'http://data.glasgow.gov.uk/api/3/action/current_package_list_with_resources'

# data = requests.get(data_url)
# json_data = data.json()

import json, csv

json_data = json.load(open("data.json"))


def get_keys(doc, base=None):
    for key, value in doc.items():
        if type(value) == dict:
            for k in get_keys(value, key):
                if base:
                    yield "%s.%s" % (base, k)
                else:
                    yield k
        elif type(value) == list:
            for v in value:
                for k in get_keys(v, key):
                    if base:
                        yield "%s.%s" % (base, k)
                    else:
                        yield k
        else:
            if base:
                yield "%s.%s" % (base, key)
            else:
                yield key


def get_mapping(doc, base=None):

    mapping = {}

    for key, value in doc.items():
        if type(value) == dict:
            for k, v in value.items():
                mapping['%s.%s' % (key, k)] = v
        elif type(value) == list:
            pass

        else:
            mapping[key] = value

    return mapping



def column_titles(document):

    found_cols = []

    for row in json_data['result']:

        for colname in get_keys(row):
            if colname not in found_cols:
                found_cols.append(colname)

    return found_cols


names = column_titles(json_data)

for name in names:
    print name

writer = csv.DictWriter(open('out.csv', 'wb'), names)

writer.writerow(dict(zip(names, names)))

for row in json_data['result']:
    row = get_mapping(row)
    for k,v in row.items():
        try:
            row[k] = str(v)
        except:
            row[k] = ''

    writer.writerow(row)

