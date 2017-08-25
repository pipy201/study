# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import os.path
import re
import sys
import tarfile

import numpy as np
from six.moves import urllib
import tensorflow as tf


class Predict:
    def __init__(self, model_dir, num_top_predictions, DATA_URL, pbtxt, uid):
        self.model_dir = model_dir
        self.num_top_predictions = num_top_predictions
        self.DATA_URL = DATA_URL
        self.label_lookup_path = os.path.join(self.model_dir, pbtxt)
        self.uid_lookup_path = os.path.join(self.model_dir, uid)
        self.final_result = 'NULL'


    def load(self, label_lookup_path, uid_lookup_path):
        if not tf.gfile.Exists(uid_lookup_path):
            tf.logging.fatal('File does not exist %s', uid_lookup_path)
        if not tf.gfile.Exists(label_lookup_path):
            tf.logging.fatal('File does not exist %s', label_lookup_path)

        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
        uid_to_human = {}
        p = re.compile(r'[n\d]*[ \S,]*')
        for line in proto_as_ascii_lines:
            parsed_items = p.findall(line)
            uid = parsed_items[0]
            human_string = parsed_items[2]
            uid_to_human[uid] = human_string
            
        node_id_to_uid = {}
        proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
        for line in proto_as_ascii:
            if line.startswith('  target_class:'):
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                target_class_string = line.split(': ')[1]
                node_id_to_uid[target_class] = target_class_string[1:-2]

        node_id_to_name = {}
        for key, val in node_id_to_uid.items():
            if val not in uid_to_human:
                tf.logging.fatal('Failed to locate: %s', val)
            name = uid_to_human[val]
            node_id_to_name[key] = name

        return node_id_to_name

    def id_to_string(self, node_id):
        if node_id not in self.node_lookup:
            return ''
        return self.node_lookup[node_id]

    def create_graph(self):
        with tf.gfile.FastGFile(os.path.join(
                self.model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
            graph_def = tf.GraphDef()

            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

    def run_inference_on_image(self, image):
        if not tf.gfile.Exists(image):
            tf.logging.fatal('File does not exist %s', image)

        image_data = tf.gfile.FastGFile(image, 'rb').read()

        self.create_graph()

        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
            predictions = sess.run(softmax_tensor,
                                   {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)

            self.node_lookup = self.load(self.label_lookup_path, self.uid_lookup_path)

            top_k = predictions.argsort()[-self.num_top_predictions:][::-1]

            for node_id in top_k:
                human_string = self.id_to_string(node_id)
                score = predictions[node_id]
                print('%s (score = %.5f)' % (human_string, score))
                self.final_result = human_string

    def get_final_result(self):
        return self.final_result


    def maybe_download_and_extract(self):
        """Download and extract model tar file."""
        dest_directory = self.model_dir

        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)

        file_name = self.DATA_URL.split('/')[-1]
        file_path = os.path.join(dest_directory, file_name)

        if not os.path.exists(file_path):
            def _progress(count, block_size, total_size):
                sys.stdout.write('\r>> Downloading %s %.1f%%' % (
                    file_name, float(count * block_size) / float(total_size) * 100.0))
                sys.stdout.flush()

            file_path, _ = urllib.request.urlretrieve(self.DATA_URL, file_path, _progress)
            print()
            stat_info = os.stat(file_path)
            print('Succesfully downloaded', file_name, stat_info.st_size, 'bytes.')

        tarfile.open(file_path, 'r:gz').extractall(dest_directory)
