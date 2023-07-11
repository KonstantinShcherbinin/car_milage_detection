import re
import json
import base64
import pytesseract
from requests import post
import sys
sys.path.insert(0, '')

from myUtils.img_bgrgray_convertation import bgrtogray_convertation

class CarMileage:

    def __init__(
        self,
        img_path: str,
        config_file: str,
        low_threshold: int = 122
    ) -> None:
        self.img_path = img_path
        self.config_file = config_file
        self.low_threshold = low_threshold

    @staticmethod
    def _get_iam_token(iam_url, oauth_token):
        response = post(iam_url, json={"yandexPassportOauthToken": oauth_token})
        json_data = json.loads(response.text)
        if json_data is not None and 'iamToken' in json_data:
            return json_data['iamToken']
        return None

    @staticmethod
    def _request_analyze(vision_url, iam_token, folder_id, image_data):
        response = post(vision_url, headers={'Authorization': 'Bearer '+ iam_token}, json={
            'folderId': folder_id,
            'analyzeSpecs': [
                {
                    'content': image_data,
                    'features': [
                        {
                            'type': 'TEXT_DETECTION',
                            'textDetectionConfig': {'languageCodes': ['en', 'ru']}
                        }
                    ],
                }
            ]})
        return response.text

    def detect(self):
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config_params = json.load(f)
        ocr = config_params["pipeline"]["ocr_type"]
        oauth_token = config_params["yandex_vision"]["oauth_token"]
        folder_id = config_params["yandex_vision"]["folderId"]
        image = bgrtogray_convertation(
            self.img_path,
            self.low_threshold,
            upper_threshold=255
        )
        result_list = []
        if ocr == 1:
            result = re.findall(r'\d{4,}', pytesseract.image_to_string(image))
        elif ocr == 2:
            iam_url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
            vision_url = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'
            iam_token = CarMileage._get_iam_token(iam_url, oauth_token)
            with open(self.img_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            response_text = CarMileage._request_analyze(vision_url, iam_token, folder_id, image_data)
            result = re.findall(r'text": "\d{4,}', response_text)
        if len(result) > 0:
            for res in result:
                result_list.append(int(''.join(re.findall(r'\d{4,}', res))))
            return max(result_list)
        else:
            return 'NaN'