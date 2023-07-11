import argparse
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\shers\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

from car_mileage_detection.car_mileage import CarMileage


def main(
    img_path: str,
    config_file: str
) -> int:
    low_threshold = 120
    car = CarMileage(img_path, config_file, low_threshold)
    mileage = car.detect()
    if mileage == 'NaN':
        low_threshold = 170
        while mileage == 'NaN' and low_threshold >= 80:
            car = CarMileage(img_path, config_file, low_threshold)
            mileage = car.detect()
            low_threshold -= 10
            #print('attempt')
    return mileage


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', type=str,
                        default='data\\original\\autoservice_priem_305_1436523_10.jpg')
    parser.add_argument('--config', type=str,
                        default='config\\detection_config.json')
    args = parser.parse_args()
    print(main(img_path=args.img_path, config_file=args.config))