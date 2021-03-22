from datetime import datetime

class BaseFormatter:
    def __init__(self):
        self._output = {}

    @property    
    def output(self):            
        return self._output

class FormatterType1(BaseFormatter):
    def __init__(self, row):
        super().__init__()
        self._output['date'] = datetime.strptime(row['timestamp'], '%b %d %Y').strftime("%d-%m-%Y")
        self._output['transaction'] = row['type']
        self._output['amount'] = row['amount']
        self._output['from'] = row['from']
        self._output['to'] = row['to']

class FormatterType2(BaseFormatter):
    def __init__(self, row):
        super().__init__()
        self._output['date'] = datetime.strptime(row['date'], '%d-%m-%Y').strftime("%d-%m-%Y")
        self._output['transaction'] = row['transaction']
        self._output['amount'] = row['amounts']
        self._output['from'] = row['from']
        self._output['to'] = row['to']

class FormatterType3(BaseFormatter):
    def __init__(self, row):
        super().__init__()
        self._output['date'] = datetime.strptime(row['date_readable'], '%d %b %Y').strftime("%d-%m-%Y")
        self._output['transaction'] = row['type']
        self._output['amount'] = float(row['euro']) + float(row['cents'])/100
        self._output['from'] = row['from']
        self._output['to'] = row['to']
