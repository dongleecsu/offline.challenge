import xml.dom.minidom
import os
import pickle

base = 'f:\groundtruth'
files = os.listdir(base)
files = [base + '\\' + e for e in files]

def parse_xml_to_dict(file):
    dom = xml.dom.minidom.parse(files[0])
    root = dom.documentElement
    types = root.getElementsByTagName('Type')
    positions = root.getElementsByTagName('Position')

    label = dict(names=[], values=[])
    for t, p in zip(types, positions):
        name = t.firstChild.data
        value = p.firstChild.data
        # convert unicode to float
        x = value.encode().strip().split()
        value = [float(e) for e in x]
        label['names'].append(name)
        label['values'].append(value)
    return label

all_groundtruth = dict()
for f in files:
    label_dict = parse_xml_to_dict(f)
    all_groundtruth[f] = label_dict

with open('all_groundtruth', 'wb') as f:
    pickle.dump(all_groundtruth, f)

# check the results
test = 1
if test:
    with open('all_groundtruth', 'rb') as f:
        data = pickle.load(f)
        print data.keys()
        gt0 = data[files[0]]
        # print type(data)
        for k, v in zip(gt0['names'], gt0['values']):
            print k, v
