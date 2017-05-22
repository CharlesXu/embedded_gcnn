from lib.datasets import PascalVOC as Data
from lib.model import (Model as BaseModel, generate_placeholders, train)
from lib.segmentation import slic_fixed, extract_features_fixed
from lib.pipeline import preprocess_pipeline_fixed
from lib.layer import EmbeddedGCNN as Conv, MaxPool, AveragePool, FC

DATA_DIR = 'data/pascal_voc'
PREPROCESS_FIRST = 'data/pascal_voc/slic'

LEVELS = 5
SCALE_INVARIANCE = False
STDDEV = 1

LEARNING_RATE = 0.001
TRAIN_DIR = 'data/savings/pascal_slic_embedded'
LOG_DIR = 'data/summaries/pascal_slic_embedded'

DROPOUT = 0.5
BATCH_SIZE = 64
MAX_STEPS = 20000
DISPLAY_STEP = 10
FORM_FEATURES = [15, 21, 24, 25, 26, 28, 29, 31, 36]
NUM_FEATURES = len(FORM_FEATURES) + 3

data = Data(DATA_DIR)

segmentation_algorithm = slic_fixed(
    num_segments=800, compactness=30, max_iterations=10, sigma=0)

feature_extraction_algorithm = extract_features_fixed(FORM_FEATURES)

filter_algorithm = None

preprocess_algorithm = preprocess_pipeline_fixed(
    segmentation_algorithm, feature_extraction_algorithm, LEVELS,
    filter_algorithm, SCALE_INVARIANCE, STDDEV)


class Model(BaseModel):
    def _build(self):
        conv_1_1 = Conv(
            NUM_FEATURES,
            32,
            adjs_dist=self.placeholders['adj_dist_1'],
            adjs_rad=self.placeholders['adj_rad_1'],
            logging=self.logging)
        conv_1_2 = Conv(
            32,
            32,
            adjs_dist=self.placeholders['adj_dist_1'],
            adjs_rad=self.placeholders['adj_rad_1'],
            logging=self.logging)
        max_pool_1 = MaxPool(size=2)
        conv_2_1 = Conv(
            32,
            64,
            adjs_dist=self.placeholders['adj_dist_2'],
            adjs_rad=self.placeholders['adj_rad_2'],
            logging=self.logging)
        conv_2_2 = Conv(
            64,
            64,
            adjs_dist=self.placeholders['adj_dist_2'],
            adjs_rad=self.placeholders['adj_rad_2'],
            logging=self.logging)
        max_pool_2 = MaxPool(size=2)
        conv_3_1 = Conv(
            64,
            128,
            adjs_dist=self.placeholders['adj_dist_3'],
            adjs_rad=self.placeholders['adj_rad_3'],
            logging=self.logging)
        conv_3_2 = Conv(
            128,
            128,
            adjs_dist=self.placeholders['adj_dist_3'],
            adjs_rad=self.placeholders['adj_rad_3'],
            logging=self.logging)
        max_pool_3 = MaxPool(size=2)
        conv_4_1 = Conv(
            128,
            256,
            adjs_dist=self.placeholders['adj_dist_4'],
            adjs_rad=self.placeholders['adj_rad_4'],
            logging=self.logging)
        conv_4_2 = Conv(
            256,
            256,
            adjs_dist=self.placeholders['adj_dist_4'],
            adjs_rad=self.placeholders['adj_rad_4'],
            logging=self.logging)
        max_pool_4 = MaxPool(size=2)
        conv_5_1 = Conv(
            256,
            512,
            adjs_dist=self.placeholders['adj_dist_5'],
            adjs_rad=self.placeholders['adj_rad_5'],
            logging=self.logging)
        conv_5_2 = Conv(
            512,
            512,
            adjs_dist=self.placeholders['adj_dist_5'],
            adjs_rad=self.placeholders['adj_rad_5'],
            logging=self.logging)
        max_pool_5 = MaxPool(size=2)
        average_pool = AveragePool()
        fc_1 = FC(512, 256, weight_decay=0.004, logging=self.logging)
        fc_2 = FC(256, 128, weight_decay=0.004, logging=self.logging)
        fc_3 = FC(128,
                  data.num_classes,
                  dropout=self.placeholders['dropout'],
                  act=lambda x: x,
                  logging=self.logging)

        self.layers = [
            conv_1_1, conv_1_2, max_pool_1, conv_2_1, conv_2_2, max_pool_2,
            conv_3_1, conv_3_2, max_pool_3, conv_4_1, conv_4_2, max_pool_4,
            conv_5_1, conv_5_2, max_pool_5, average_pool, fc_1, fc_2, fc_3
        ]


placeholders = generate_placeholders(BATCH_SIZE, LEVELS, NUM_FEATURES,
                                     data.num_classes)

model = Model(
    placeholders=placeholders,
    isMultilabel=True,
    learning_rate=LEARNING_RATE,
    # epsilon=0.1,
    train_dir=TRAIN_DIR,
    log_dir=LOG_DIR)

train(model, data, preprocess_algorithm, BATCH_SIZE, DROPOUT, MAX_STEPS,
      PREPROCESS_FIRST, DISPLAY_STEP)
