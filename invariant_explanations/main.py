# coding=utf-8
# Copyright 2022 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Main file used for approxNN project."""

from typing import Sequence
import warnings

from absl import app
from absl import flags

from invariant_explanations import config
from invariant_explanations import other
from invariant_explanations import utils


FLAGS = flags.FLAGS

_RANDOM_SEED = flags.DEFINE_integer(
    'random_seed',
    42,
    'The seed used for all numpy random operations.',
)
_DATASET = flags.DEFINE_string(
    'dataset',
    'cifar10',
    'The dataset, chosen from config.ALLOWABLE_DATASETS.',
)
_EXPLANATION_TYPE = flags.DEFINE_string(
    'explanation_type',
    'ig',
    'The explanation method, chosen from config.ALLOWABLE_EXPLANATION_METHODS.',
)
_RUN_ON_TEST_DATA = flags.DEFINE_boolean(
    'run_on_test_data',
    False,
    'The flag used to specify whether or not to run on sample test data.',
)
_NUM_BASE_MODELS = flags.DEFINE_integer(
    'num_base_models',
    30000,
    'The number of base models to load from the CNN Zoo.',
)
_NUM_SAMPLES_PER_BASE_MODEL = flags.DEFINE_integer(
    'num_samples_per_base_model',
    32,
    'The number of sample images to use per base model.',
)
_NUM_SAMPLES_TO_PLOT_TE_FOR = flags.DEFINE_integer(
    'num_samples_to_plot_te_for',
    8,
    'The number of samples for which to plot treatment effects.',
)
_KEEP_MODELS_ABOVE_TEST_ACCURACY = flags.DEFINE_float(
    'keep_models_above_test_accuracy',
    0.55,
    'The threshold to use when select models from the CNN Zoo.',
)
_USE_IDENTICAL_SAMPLES_OVER_BASE_MODELS = flags.DEFINE_boolean(
    'use_identical_samples_over_base_models',
    True,
    'A flag indicating whether or not to use identical samples on base models.',
)

warnings.simplefilter('ignore')


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  # Update config file defaults if the arguments are passed in via the cmd line.
  config.cfg.set_config_paths({
      'RANDOM_SEED': _RANDOM_SEED.value,
      'DATASET': _DATASET.value,
      'EXPLANATION_TYPE': _EXPLANATION_TYPE.value,
      'RUN_ON_TEST_DATA': _RUN_ON_TEST_DATA.value,
      'NUM_BASE_MODELS': _NUM_BASE_MODELS.value,
      'NUM_SAMPLES_PER_BASE_MODEL': _NUM_SAMPLES_PER_BASE_MODEL.value,
      'NUM_SAMPLES_TO_PLOT_TE_FOR': _NUM_SAMPLES_TO_PLOT_TE_FOR.value,
      'KEEP_MODELS_ABOVE_TEST_ACCURACY': _KEEP_MODELS_ABOVE_TEST_ACCURACY.value,
      'USE_IDENTICAL_SAMPLES_OVER_BASE_MODELS': (
          _USE_IDENTICAL_SAMPLES_OVER_BASE_MODELS.value
      ),
  })

  utils.create_experimental_folders()

  # utils.analyze_accuracies_of_base_models()

  utils.process_and_resave_cnn_zoo_data(
      config.cfg.RANDOM_SEED,
      other.get_model_wireframe(),
      config.cfg.COVARIATES_SETTINGS,
  )

  # utils.plot_treatment_effect_values()

  # utils.train_meta_model_over_different_setups(config.cfg.RANDOM_SEED)

  # utils.save_heat_map_of_meta_model_results()

  # utils.process_per_class_explanations(config.cfg.RANDOM_SEED)

  # utils.measure_prediction_explanation_variance(config.cfg.RANDOM_SEED)


if __name__ == '__main__':
  app.run(main)
