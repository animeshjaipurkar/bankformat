# RUN TEST CASES
# python3 -m unittest -v test_script.py 

import unittest
import script

class TestScript(unittest.TestCase):

    def test_read_csv(self):
        test_file = 'test.csv'
        expected_field_keys = set({'col1','col2','col3','col4','col5'})
        expected_row_list = [
            {'col1': '02-09-2019', 'col2': 'add', 'col3': '2000.10', 'col4': '188', 'col5': '198'}, 
            {'col1': '05-09-2019', 'col2': 'add', 'col3': '123.79', 'col4': '178', 'col5': '188'}, 
            {'col1': '01-10-2019', 'col2': 'remove', 'col3': '99.10', 'col4': '198', 'col5': '182'}, 
            {'col1': '02-10-2019', 'col2': 'add', 'col3': '2000.10', 'col4': '188', 'col5': '198'}
        ]

        field_keys, row_list = script.read_csv(test_file)
     
        self.assertEqual(field_keys, expected_field_keys)
        self.assertEqual(len(row_list), len(expected_row_list))
        self.assertListEqual(row_list, expected_row_list)


    def test_convert_to_output_format_TYPE1(self):

        type1_data = [
                        {'timestamp': 'Oct 1 2019', 'type': 'add', 'amount': 2000.10, 'from': '188', 'to': '198'}, 
                        {'timestamp': 'Oct 2 2019', 'type': 'add', 'amount': 123.79, 'from': '178', 'to': '188'}
                    ]
        expected_output = [
                        {'date': '01-10-2019', 'transaction': 'add', 'amount': 2000.10, 'from': '188', 'to': '198'}, 
                        {'date': '02-10-2019', 'transaction': 'add', 'amount': 123.79, 'from': '178', 'to': '188'}, 
                    ]

        output = script.convert_to_output_format(type1_data, 'TYPE_1')

        self.assertEqual(output, expected_output)


    def test_convert_to_output_format_TYPE2(self):

        type2_data = [
                        {'date': '03-10-2019', 'transaction': 'add', 'amounts': 2000.10, 'from': '188', 'to': '198'}, 
                        {'date': '04-10-2019', 'transaction': 'add', 'amounts': 123.79, 'from': '178', 'to': '188'}
                    ]
        expected_output = [
                        {'date': '03-10-2019', 'transaction': 'add', 'amount': 2000.10, 'from': '188', 'to': '198'}, 
                        {'date': '04-10-2019', 'transaction': 'add', 'amount': 123.79, 'from': '178', 'to': '188'}, 
                    ]

        output = script.convert_to_output_format(type2_data, 'TYPE_2')

        self.assertEqual(output, expected_output)


    def test_convert_to_output_format_TYPE3(self):

        type3_data = [
                        {'date_readable': '5 Oct 2019', 'type': 'add', 'euro': 2000, 'cents': 1, 'from': '188', 'to': '198'}, 
                        {'date_readable': '6 Oct 2019', 'type': 'add', 'euro': 123, 'cents': 79, 'from': '178', 'to': '188'}
                    ]
        expected_output = [
                        {'date': '05-10-2019', 'transaction': 'add', 'amount': 2000.01, 'from': '188', 'to': '198'}, 
                        {'date': '06-10-2019', 'transaction': 'add', 'amount': 123.79, 'from': '178', 'to': '188'}, 
                    ]

        output = script.convert_to_output_format(type3_data, 'TYPE_3')

        self.assertEqual(output, expected_output)

    def test_sort_output(self):
        unsorted_data = [
                    {'date': '05-11-2019', 'transaction': 'add', 'amount': 2000.10, 'from': '188', 'to': '198'}, 
                    {'date': '06-10-2019', 'transaction': 'add', 'amount': 123.79, 'from': '178', 'to': '188'}, 
                    {'date': '03-07-2019', 'transaction': 'add', 'amount': 2000.10, 'from': '188', 'to': '198'}, 
                    ]
        expected_output = [                                         
                    {'date': '03-07-2019', 'transaction': 'add', 'amount': 2000.10, 'from': '188', 'to': '198'}, 
                    {'date': '06-10-2019', 'transaction': 'add', 'amount': 123.79, 'from': '178', 'to': '188'}, 
                    {'date': '05-11-2019', 'transaction': 'add', 'amount': 2000.10, 'from': '188', 'to': '198'},
                    ]

        output = script.sort_output(unsorted_data)

        self.assertEqual(output, expected_output)









