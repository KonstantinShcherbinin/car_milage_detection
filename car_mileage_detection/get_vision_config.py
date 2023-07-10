import json
import sys
sys.path.insert(0, '')
from myUtils.vision_base64 import encode_img

def get_config(
          image_path: str,
          config_path: str = 'config\\body.json'
):
    with open(config_path, 'r', encoding='utf-8') as f:
        params = json.load(f)
    params["analyze_specs"][0]["content"] = str(encode_img(image_path))
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(params, f, ensure_ascii=False, indent=4)