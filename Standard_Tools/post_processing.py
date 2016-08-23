import sys
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def location(headers, data):
    location_pos = []
    extra_pos = {}
    for h in range(0, len(headers)):
        if headers[h] == 'Organization_Name_COUNTRY':
            extra_pos['ONC'] = h
        if headers[h] == 'Organization_Name_PROVINCE':
            extra_pos['ONP'] = h
        if 'LOCATION' in headers[h]:
            location_pos.append(h)

    if extra_pos != {}:
        for line in data:
            if ''.join([line[i] for i in location_pos]) == '':
                for p in location_pos:
                    if line[p] == '':
                        line.append(line[extra_pos['ONC']])
                        break


def process_file(in_file):
    csvin = open(in_file, 'rU')
    reader = csv.reader(csvin, delimiter=',')
    headers = reader.next()
    data = [i for i in reader]
    location(headers, data)
    headers.append('putative_LOCATION')
    csvin.close()
    with open(in_file, 'w') as csvout:
        csvwriter = csv.writer(csvout, delimiter=',')
        csvwriter.writerow(headers)
        for d in data:
            csvwriter.writerow(d)


if __name__ == '__main__':
    for i in sys.argv[1:]:
        process_file(i)
