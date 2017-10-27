import xml.dom.minidom
import os
import pickle
import codecs
import chardet

base = './datasets/TSD-Signal-GT/'
f_names = os.listdir(base)
f_paths = [base + e for e in f_names]

def convert_enc(f, out_enc = "UTF-8"):
    content = codecs.open(f, 'r').read()
    src_encoding = chardet.detect(content)['encoding']
    print 'File ' + f + ' encoding: ' + str(src_encoding)
    content = content.decode(src_encoding).encode(out_enc)
    codecs.open(f, 'w').write(content)

def parse_xml_to_dict(f):
    convert_enc(f)
    dom = xml.dom.minidom.parse(f)
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
for f_path, f_name in zip(f_paths, f_names):
    label_dict = parse_xml_to_dict(f_path)
    all_groundtruth[f_name] = label_dict

with open('all_groundtruth', 'wb') as f:
    pickle.dump(all_groundtruth, f)

# check the results
test = 1
if test:
    with open('all_groundtruth', 'rb') as f:
        data = pickle.load(f)
        print data.keys()
        gt0 = data[f_names[0]]
        # print type(data)
        for k, v in zip(gt0['names'], gt0['values']):
            print k, v