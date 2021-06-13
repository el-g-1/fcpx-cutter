import xml.etree.ElementTree as ET
from copy import deepcopy
import argparse


def get_duration(elem):
    return int((elem.attrib['duration'].split('/'))[0])


def get_offset(elem):
    if elem.attrib['offset'] == '0s':
        return 0
    return int((elem.attrib['offset'].split('/'))[0])


def get_start(elem):
    return int((elem.attrib['start'].split('/'))[0])


def get_line_iter(root, cut_time):
    local_offset = 0
    for k in range(len(root[1][0][0][0][0])):
        if cut_time > local_offset + get_duration(root[1][0][0][0][0][k]):
            local_offset += get_duration(root[1][0][0][0][0][k])
        else:
            return k


def split_in_two(root, split_line_number, cuts, i):
    insert_line = deepcopy(root[1][0][0][0][0][split_line_number])
    split_line = root[1][0][0][0][0][split_line_number]
    split_line.attrib['duration'] = str(cuts[i] - get_offset(split_line)) + '/30000s'
    insert_line.attrib['offset'] = str(cuts[i]) + '/30000s'
    insert_line.attrib['duration'] = str(get_duration(insert_line) - get_duration(split_line)) + '/30000s'
    insert_line.attrib['start'] = str(get_start(split_line) + get_duration(split_line)) + '/30000s'
    root[1][0][0][0][0].insert(split_line_number + 1, insert_line)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='FCPX file cutter')
    parser.add_argument('--input_file', '-i', required=True,
                        help='XML input file')
    parser.add_argument('--cuts_timestamps', '-c', required=True,
                        help='File with timestamps of cuts', )

    args = parser.parse_args()

    cuts_file = args.cuts_timestamps
    with open(cuts_file, 'r') as cuts_data:
        cuts = [int(line) for line in cuts_data.readlines()]

    input_file = args.input_file
    tree = ET.parse(input_file)
    root = tree.getroot()

    for i in range(len(cuts)):
        split_line_number = get_line_iter(root, cuts[i])
        split_in_two(root, split_line_number, cuts, i)

    with open('output_file.fcpxml', 'wb') as output_file:
        output_file.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode('utf-8'))
        output_file.write('<!DOCTYPE fcpxml>\n\n'.encode('utf-8'))

        tree.write(output_file)
