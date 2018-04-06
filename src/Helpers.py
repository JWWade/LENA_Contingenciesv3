"""
The MIT License (MIT)
Copyright (c) 2018 Paul Yoder, Joshua Wade, Kenneth Bailey, Mena Sargios, Joseph Hull, Loraina Lampley, John Peden,
Bishoy Boktor, Kate Lovett, Joel Norris, Joseph London, Jesse Offei-nkansah

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import csv
import xlsxwriter
import datetime

# Sequence Analysis Data Object
# Holds all items needed for analysis
class SeqData:
    its_dict = None
    seq_config = None
    num_threads = None
    output_format = None

    def __init__(self, its_dict, seq_config, num_threads, output_format):
        self.num_threads = num_threads
        self.its_dict = its_dict
        self.seq_config = seq_config
        self.output_format = output_format

# Sequence Analysis Run Object
# Put into queue; used in Perform()
class SeqRun:
    p_id = None
    path = None

    def __init__(self, p_id, path):
        self.p_id = p_id
        self.path = path

# Output Object
# sent to output functions
class OutData:
    batch_store = None
    seq_config = None
    results = None

    def __init__(self, batch_store, seq_config, results):
        self.batch_store = batch_store
        self.seq_config = seq_config
        self.results = results

# Output to CSV format
def output_csv(out_data):
    """This method outputs the analysis results to a .csv file"""
    # output code
    print("Output in .csv")

    # create + write csv file
    out_file = out_data.seq_config['outputDirPath'] +'//'+ "LC2-"+out_data.batch_store+"-"+out_data.seq_config['seqType']+"-"+str(out_data.seq_config['PauseDur']).replace('.','p')+"-"+str(out_data.seq_config['roundingEnabled'])+"-"+datetime.datetime.now().strftime('%m%d%y-%H%M')+".csv"
    with open( out_file, 'wb') as f:#open csv file to be written in
        csv_writer = csv.writer(f, delimiter = ',')
        for line in out_data.results:#loop to write rows to csv file
            line = line.split(',')
            csv_writer.writerow(line)

# Output to TXT format
def ouput_txt(out_data):
    """This method outputs the analysis results to a .txt file"""
    # output code 
    print("Output in .txt")

    # create + write txt file
    out_file = out_data.seq_config['outputDirPath'] +'//'+ "LC2-"+out_data.batch_store+"-"+out_data.seq_config['seqType']+"-"+str(out_data.seq_config['PauseDur']).replace('.','p')+"-"+str(out_data.seq_config['roundingEnabled'])+"-"+datetime.datetime.now().strftime('%m%d%y-%H%M')+".txt"
    with open(out_file,'w') as f:
        for line in out_data.results:
            f.writelines(line+"\n")

# Output to Excel format
def output_xlsx(out_data):
    """This method outputs the analysis results to a .xlsx file"""
    print("Output in .xlsx")
    # create workbook & add sheet
    out_file = out_data.seq_config['outputDirPath'] +'//'+ "LC2-"+out_data.batch_store+"-"+out_data.seq_config['seqType']+"-"+str(out_data.seq_config['PauseDur']).replace('.','p')+"-"+str(out_data.seq_config['roundingEnabled'])+"-"+datetime.datetime.now().strftime('%m%d%y-%H%M')+".xlsx"
    workbook = xlsxwriter.Workbook(out_file)
    worksheet = workbook.add_worksheet()

    # start from first cell
    row = 0
    
    # insert into worksheet
    for line in out_data.results:
        col = 0
        for cell in str(line).split(","):
            worksheet.write(row, col, cell)
            col += 1
        row += 1

    # close file
    workbook.close()