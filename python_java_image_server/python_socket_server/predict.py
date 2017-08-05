import tensorflow as tf


class Predict:
    def __int__(self):
        pass

    def load_image(self, filename):
        """Read in the image_data to be classified."""
        return tf.gfile.FastGFile(filename, 'rb').read()

    def load_labels(self, filename):
        """Read in labels, one label per line."""
        return [line.rstrip() for line in tf.gfile.GFile(filename)]

    def load_graph(self, filename):
        """Unpersists graph from file as default graph."""
        with tf.gfile.FastGFile(filename, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')

    def run_graph(self, image_data, labels, input_layer_name, output_layer_name,
                  num_top_predictions):
        result_list = []
        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
            predictions, = sess.run(softmax_tensor, {input_layer_name: image_data})

            # Sort to show labels in order of confidence
            top_k = predictions.argsort()[-num_top_predictions:][::-1]
            print_count = 0
            for node_id in top_k:
                human_string = labels[node_id]
                result_list.append(labels[node_id])
                score = predictions[node_id]
                print('%s (score = %.5f)' % (human_string, score))

                print_count += 1
                if print_count == 5:
                    print(result_list)
                    break

            return result_list[0]
