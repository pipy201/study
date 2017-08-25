# -*- coding: utf-8 -*-
import predict
import os


class Connect:
    def __init__(self, image_file):
        model_dir = 'imagenet_model'
        num_top_predictions = 1
        pbtxt = 'imagenet_2012_challenge_label_map_proto.pbtxt'
        uid = 'imagenet_synset_to_human_label_map.txt'
        DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'

        predict_inst = predict.Predict(model_dir,num_top_predictions, DATA_URL, pbtxt, uid)

        predict_inst.maybe_download_and_extract()

        predict_inst.run_inference_on_image(image_file)

        self.result = predict_inst.get_final_result()

        os.remove(image_file)

    def get_result(self):
        final_result = self.result.split(',')[0].strip()
        print('last : ' + final_result)
        return final_result
