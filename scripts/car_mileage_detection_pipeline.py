#!/usr/bin/python

"""

"""

import argparse
import json
import os
import tempfile
import shutil

from sklearn.preprocessing import OneHotEncoder, PowerTransformer
from sklearn.pipeline import Pipeline
from sklearn.compose import TransformedTargetRegressor, ColumnTransformer
from residual_water_prediction.utils import log_array, exp_array

def main(config_file: str):
    with open(config_file, 'r', encoding='utf-8') as f:
        config_params = json.load(f)
    input_path = config_params['input_path']
    coordinates = tuple(config_params['crop_coordinates'])
    image_shape = tuple(config_params['image_shape'])
    output_path = config_params['output_path']
    with tempfile.TemporaryDirectory(dir=os.path.expanduser('~')) as tmp_folder:
        tmp_image_path = os.path.join(tmp_folder, 'sample.raw')
        filtered_data_path = os.path.join(tmp_folder, 'filtered.raw')
        shutil.copy(input_path, tmp_image_path)
        config_dict = crop_image(tmp_image_path, coordinates, image_shape)
        tensor_dict_x = get_tensor(config_dict, output_path, direction='x')
        tensor_dict_y = get_tensor(config_dict, output_path, direction='y')
        tensor_dict_z = get_tensor(config_dict, output_path, direction='z')
        if permeability_test(tensor_dict_x, tensor_dict_y, tensor_dict_z):
            data_x = tensor_dict_x['filtered_data']
            data_y = tensor_dict_y['filtered_data']
            data_z = tensor_dict_z['filtered_data']
            filtered_data_common = (data_x == 1) & (
               data_y == 1) & (data_z == 1)
            filtered_data_common.tofile(filtered_data_path)
            runner = PartitionerRunner()
            result = runner.run(
                image_path=filtered_data_path,
                output_path='../data/cube_200_masked_partition.raw',
                sample_size=config_dict['size']
            )
            return result
        
def make_pipeline(
        regressor: str,
        iterations: int,
        lr: float,
        random_seed: int,
        loss_func: str,
        eval_metric: str,
        num_feats: list,
        cat_feats: list
):
    if regressor == 'xgb':
        regr = xgb.XGBRegressor(nthread=1)
    elif regressor == 'catb':
        regr = CatBoostRegressor(
            iterations=iterations,
            learning_rate=lr,
            random_seed=random_seed,
            loss_function=loss_func,
            eval_metric=eval_metric,
            verbose=False
        )
    else:
        raise NameError('Сhoose one: "catb", "xgb"')
    numeric_transformer = Pipeline(steps=[
        ('scaler', PowerTransformer())
    ])
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, num_feats),
        ('cat', categorical_transformer, cat_feats)
    ])
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('transformed_target_regr', TransformedTargetRegressor(
            regressor=regr,
            func=log_array,
            inverse_func=exp_array,
            check_inverse=True
        )
        )])
    return model


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str,
                        default='../config/velocity_pressure_calc_config.json')
    args = parser.parse_args()
    main(config_file=args.config)