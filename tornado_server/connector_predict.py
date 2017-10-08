# -*- coding: utf-8 -*-
import os
import predict


class Connector:
    def __init__(self, image_file):
        MODEL_DIR = 'imagenet_model'
        NUM_TOP_PREDICTIONS = 1
        PBTXT = 'imagenet_2012_challenge_label_map_proto.pbtxt'
        UID = 'imagenet_synset_to_human_label_map.txt'
        DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'

        predict_inst = predict.Predict(MODEL_DIR, NUM_TOP_PREDICTIONS, DATA_URL, PBTXT, UID)

        predict_inst.maybe_download_and_extract()

        predict_inst.run_inference_on_image(image_file)

        self.result = predict_inst.get_final_result()

        # os.remove(image_file)

    def get_result(self):
        final_result = self.result.split(',')[0].strip()
        print('last : ' + final_result)
        return final_result


# if __name__ == '__main__':
#     Connector('test.jpg')

