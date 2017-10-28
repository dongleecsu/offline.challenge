import os
import random
import pickle
import PIL.Image
import tensorflow as tf

flags = tf.app.flags
flags.DEFINE_string('data_dir', '', 'Root directory to raw pet dataset.')
flags.DEFINE_string('output_dir', '', 'Path to directory to output TFRecords.')
flags.DEFINE_string('label_map_path', 'data/pet_label_map.pbtxt',
                    'Path to label map proto')
FLAGS = flags.FLAGS

def read_all_samples(src_path):
    '''Recursively read all filenames in dirs and subdirs
    Return full path files list
    '''
    samples_list = []
    for root, dirs, files in os.walk(src_path):
        for name in files:
            samples_list.append(os.path.join(root, name))
    return samples_list

def get_label_map_dict(src_path):
    '''Generate label_map dict'''
    with open(src_path, 'rb') as f:
        all_items = pickle.load(f)
    label_map_dict = {}
    counter = 1
    for name, subdict in all_items.iteritems():
        # For subdict,
        # key 'names' --> label names
        # key 'values' --> bbox coordinates
        for name in subdict['names']:
            if name not in label_map_dict.keys():
                label_map_dict[name] = counter
                counter += 1
    return label_map_dict

def dict_to_tf_sample(sample,
                      label_map_dict,
                      annotation):
    image = PIL.Image.open(sample)
    width, height = image.size

    xmin = []
    ymin = []
    xmax = []
    ymax = []
    classes = []
    classes_text = []

    xmin.append(float(annotation['']))

def create_tf_record(output_filename,
                     samples_list,
                     label_map_dict,
                     annotations_path):
    writer = tf.python_io.TFRecordWriter(output_filename)
    for idx, sample in enumerate(samples_list):
        for idx % 100 == 0:
            print 'On image %d of %d', idx, len(samples_list)
        tf_sample = dict_to_tf_sample(sample, 
                                      label_map_dict, 
                                      annotations_path)
        writer.write(tf_sample.SerializeToString())
    writer.close()

def main(_):
    '''Pipeline
    1. Read samples, labels and label_map
    2. Shuffle sample name list, and generate train/val list
    3. Create tf record
    '''
    # Read samples, labels and label map
    data_dir = FLAGS.data_dir
    label_map_dict = get_label_map_dict(FLAGS.label_map_path)
    samples_list = read_all_samples(data_dir)

    # Shuffle and generate train/val list
    random.seed(1234)
    random.shuffle(samples_list)
    num_samples = len(samples_list)
    num_train = int(0.7 * num_samples)
    train_samples_list = samples_list[:num_train]
    val_samples_list = samples_list[num_train:]
    print '%d training and %d validation samples.',
            len(train_samples_list), , len(val_samples_list)
    
    train_out_path = os.path.join(FLAGS.output_dir, 'signal_trian.record')
    val_out_path = os.path.join(FLAGS.output_dir, 'signal_val.record')
    create_tf_record(train_out_path, train_samples_list, 
                    label_map_dict, annotations_path)
    create_tf_record(val_out_path, val_samples_list, 
                    label_map_dict, annotations_path)


    # Create tf record

if __name__ == '__main__':
    tf.app.run()
