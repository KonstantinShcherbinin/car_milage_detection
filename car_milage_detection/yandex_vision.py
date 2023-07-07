import os
import re
from requests import post
import json
import argparse
import base64

#from myUtils.vision_base64 import encode_img

"""
Протухает через 12 часов не использования
yc iam create-token >> /home/web/token.txt


"""

def detection(input_path):
    url = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'
    img_encoded = encode_img(input_path)
    #headers = {'Authorization': 'Bearer ' f'{iam_token}'}
    headers = {'Authorization': 'Bearer' 't1.9euelZrNlsfHmciVm4yPjYuLnMnNne3rnpWazJfOjIyXnpyNlJfIkpmezcbl9PcDa2Fa-e97Mz663fT3QxlfWvnvezM-us3n9euelZrIjZOOlYvGicrGm8nHz5OXlO_8xeuelZrIjZOOlYvGicrGm8nHz5OXlA.1m0BbYqErPAIlCf80A4s7PWR0XZ9kERST3tbSK0StyhhbJ02wHMdvah1n1ejGYGB9_YVcE9HlIhSsXeNSJ9qBw'}
    data = {
        "analyzeSpecs": [
            {
                "content": f'{img_encoded}',
                "features": [
                    {
                        "type": "TEXT_DETECTION",
                        "textDetectionConfig": {
                            "language_codes": ["*"]
                        }
                    }
                ],
                "mimeType": "JPEG"
            }
        ],
        "folderId": "b1gmsb4q0i5t61l8k3pm"
    }
    #print(encode_img(img_path))
    resp = post(url, headers=headers, json=data)
    return resp


# Функция возвращает IAM-токен для аккаунта на Яндексе.
def get_iam_token(iam_url, oauth_token):
    response = post(iam_url, json={"yandexPassportOauthToken": oauth_token})
    json_data = json.loads(response.text)
    if json_data is not None and 'iamToken' in json_data:
        return json_data['iamToken']
    return None


# Функция отправляет на сервер запрос на распознавание изображения и возвращает ответ сервера.
def request_analyze(vision_url, iam_token, folder_id, image_data):
    response = post(vision_url, headers={'Authorization': 'Bearer '+iam_token}, json={
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


def main(folder_id, oauth_token, img_path):
    iam_url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    vision_url = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'
    iam_token = get_iam_token(iam_url, oauth_token)
    with open(img_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    response_text = request_analyze(vision_url, iam_token, folder_id, image_data)
    print(re.findall(r'text": "\d{4,}', response_text))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--folder_id', type=str, default='b1gmsb4q0i5t61l8k3pm'
    )
    parser.add_argument(
        '--oauth_token', type=str,
        default='y0_AgAEA7qjzo7AAATuwQAAAADnErYl2tu26CyRSmiuVvhqDVzKUaUl5-A'
    )
    parser.add_argument(
        '--image_path', type=str,
        default='C:\\Users\\shers\\car_milage_detection\\data\\original\\autoservice_priem_305_1436523_10.jpg'
    )
    args = parser.parse_args()

    main(
        folder_id=args.folder_id,
        oauth_token=args.oauth_token,
        img_path=args.image_path
    )
