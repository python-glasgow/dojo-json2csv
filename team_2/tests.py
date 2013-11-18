# Released to the Public Domain

import unittest
import csv
import json

"""
Parser for:

http://data.glasgow.gov.uk/api/3/action/current_package_list_with_resources
"""


def get_row_headers(data):
    """
    Take a dictionary and walk the dictionary identifying allthe unique row
    headers.
    """
    headers = set()
    try:
        for key, value in data.iteritems():
            try:
                iter(value)
                if not isinstance(value, basestring):
                    if isinstance(value, dict):
                      headers.update(value.keys())
                    else:
                        for subrow in value:
                            headers.update(get_row_headers(subrow))
                else:
                    headers.add(key)
            except TypeError:
                headers.add(key)
    except AttributeError, e:
        raise
    return headers


def get_rows_from_data(headers, data):
    """
    """
    yield list(headers)
    for key, value in data.iteritems():
        current_row = dict(zip(headers, [None for x in headers]))
        if key in headers:
            current_row[key] = value
        else:
            for subrow in value:
                for subkey, subvalue in subrow.iteritems():
                    if subkey in headers:
                        current_row[subkey] = subvalue
                yield current_row


def convert_json_to_csv(inputname, outputname):
    """
    """
    data = json.load(open(inputname))
    output = csv.writer(open(outputname, 'w'))

    headers = get_row_headers(data)
    for row in get_rows_from_data(headers, data):
        output.writerow(row)
    output.close()


class JSONtoCSVTestCase(unittest.TestCase):

    def create_dummy_data(self):
        result = []
        for x in range(5):
            row = {u'author': 'Author %d' % x,
                   u'author_email': 'author@example.com',
                   u'extras': 'extras',
                   u'groups': 'groups',
                   u'tracking_summary': {u'recent': 2, u'total': 2},
                   u'id': x}
            result.append(row)
        initial_data = {'help': 'This is the help',
                        'success': True,
                        'result': result}
        return initial_data

    def test_get_row_headers(self):
        """
        get_row_headers should analyse the provided data and return a 
        list with all the row headers.
        """
        data = self.create_dummy_data()
        self.assertEqual(
            set(['help', 'success', 'author', 'author_email', 'extras', 'groups', 'id', 'recent', 'total']),
            get_row_headers(data))

    def test_get_rows_from_data(self):
        """
        Given a set of headers and a dictionary structure, return a complete list
        of all rows to be written to a CSV file.
        """
        data = self.create_dummy_data()
        result = list(get_rows_from_data(
            set(['help', 'success', 'author', 'author_email', 'extras', 'groups', 'id']),
            data))

        self.assertEqual(6, len(result))
        self.assertEqual(
          ['help', 'success', 'author', 'author_email', 'extras', 'groups', 'id'],
          result[0])
