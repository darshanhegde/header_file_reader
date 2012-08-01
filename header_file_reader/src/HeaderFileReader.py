'''
Created on Aug 1, 2012

@author: Darshan.hegde

@note: This is a utility class which can read files with headers and helps as utility
which can be used to iterate over files.
'''
import unittest
from collections import namedtuple


class HeaderFileReader:
    
    def __init__(self, delimiter, qualifier, data_file_path):
        ''' Constructor for the class
        :param delimiter: the string by which the data-fields are separated
        :type delimiter: string
        :param qualifier: the string by which the data-fields are surrounded
        :type qualifier: string
        :param data_file_path: path for the data-file which you want to read
        :type data_file_path: string
        :returns: object of HeaderFileReader
        :rtype: HeaderFileReader
        '''
        self._delimiter = delimiter
        self._qualifier = qualifier
        self._data_file = open(data_file_path, 'rU')
        self._fields = namedtuple('fields', [field.strip(self._qualifier) for field in self._data_file.readline().strip().split(self._delimiter)], False)

    def __iter__(self):
        '''Iterator implementation
        '''
        return self
    
    def next(self):
        '''Get the next data_line 
        :returns: object of fields, which will have header name as class variables
        :rtype: fields
        '''
        data_line = self._data_file.readline()
        if data_line:
            field_list = [field.strip(self._qualifier) for field in data_line.strip().split(self._delimiter)]
            return self._fields._make(field_list)
        else:
            raise StopIteration
        
    def __del__(self):
        self._data_file.close()
        
class TestHeaderFileReader(unittest.TestCase):
    
    def setUp(self):
        self.HFR = HeaderFileReader(delimiter='::', qualifier="'", data_file_path='../data/movies.dat')
        
    def test_next(self):
        # simple sanity check on reading first line
        first_line = self.HFR.next()
        self.assertEqual(first_line.movie_id, '1', "Error in next() not reading movie_id")
        self.assertEqual(first_line.movie_name, 'Toy Story (1995)', "Error in next() not reading movie_name")
        self.assertEqual(first_line.genera, "Animation|Children's|Comedy", "Error in next() not reading genera")
        # jump to the last line
        for line in range(5):
            self.HFR.next()
        # simple sanity check on StopIteration
        self.assertRaises(StopIteration, self.HFR.next)

            
def main():
    unittest.main()
            
if __name__ == '__main__':
    main()

            
    