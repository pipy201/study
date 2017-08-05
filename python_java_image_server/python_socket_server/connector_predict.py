# -*- coding:utf8 -*-

import predict
import os


class Connect:
    def __init__(self, file_name):
        # predict setting
        image = file_name
        label = 'retrained_labels.txt'
        graph = 'retrained_graph.pb'
        input_layer = 'DecodeJpeg/contents:0'
        output_layer = 'final_result:0'
        top_predictions = 5

        # predict exec
        pre = predict.Predict()
        image_file = pre.load_image(image)

        os.remove(file_name)

        labels_file = pre.load_labels(label)
        pre.load_graph(graph)
        self.result = pre.run_graph(image_file, labels_file, input_layer, output_layer, top_predictions)

    def get_result(self):
        return self.result
