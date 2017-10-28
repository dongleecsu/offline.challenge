import os
import pickle
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
    all_items = pickle.load(src_path).read()
    


def create_tf_record(parameter_list):
    pass

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


    # Create tf record

if __name__ == '__main__':
    tf.app.run()
