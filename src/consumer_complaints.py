import csv
from collections import defaultdict
import os
import sys
def run_program(input_file, output_file):
    # read the file and clean the data
    if not os.path.isfile(input_file):
        print(f'The file {input_file} does not exist!')
        exit(-1)
    elif os.stat(input_file).st_size == 0:
        print(f'The file {input_file} is empty!')
        exit(-1)
    else:
        records = []
        with open(input_file, "r") as this_csv_file:
            this_csv_reader=csv.reader(this_csv_file,delimiter=",")
            for i, line in enumerate(this_csv_reader):
                # to not consider the header and extract the indices of the date, product and company columns
                if i == 0:
                    index_company = line.index('Company')
                    index_date_received = line.index('Date received')
                    index_product = line.index('Product')
                    continue
                # remove the lines with missing values for date, product or company
                if line[index_company] in (None, "") or line[index_date_received] in (None, "") or line[index_product] in (None, ""):
                    continue
                records.append(line)
        n_records = len(records)
    # count complaints according to year and product
        total_complaint = defaultdict(lambda: 0)
        for idx in range(n_records):
            key_year = records[idx][index_date_received]
            key_year = key_year.split('-')[index_date_received]
            key_product = records[idx][index_product].lower()
            key = (key_product, key_year)
            total_complaint[key] = total_complaint[key] + 1
    # count number of complaints for each company
        company_complaint = defaultdict(lambda: 0)
        for idx in range(n_records):
            key_year = records[idx][index_date_received]
            key_year = key_year.split('-')[index_date_received]
            key_product = records[idx][index_product].lower()
            key_company = records[idx][index_company].lower()
            key = (key_product, key_year, key_company)
            company_complaint[key] = company_complaint[key] + 1
    # write the records into the file
        report = []
        with open(output_file, 'w', newline='') as csv_report:
            writer = csv.writer(csv_report)
            keys_product_date = [key[0:2]for key in list(company_complaint.keys())]
            for key, value in total_complaint.items():
                line_to_add = list(key + (value,))
                n_compony_complaints_in_productYear = keys_product_date.count(key)
                line_to_add.append(n_compony_complaints_in_productYear)
                company_complaints = [v for k, v in company_complaint.items() if k[0:2] == key]
                # Calculate the highest percentage complaint of companies
                max_value = max(company_complaints)
                highest_percentage = (max_value/value)*100
                highest_percentage = round(1 if highest_percentage == 0.5 else highest_percentage)
                line_to_add.append(highest_percentage)
                report.append(line_to_add)
            # sort report by product (alphabetically) and year (ascending)
            report = sorted(report, key=lambda x: (x[0], x[1]))

            writer.writerows(report)
def main():
    # input_file = "../input/complaints.csv"
    # output_file = "../output/report.csv"
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    run_program(input_file, output_file)
    print('Output saved successfully in', output_file)
if __name__ == '__main__':
    main()

