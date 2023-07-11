import tempfile
from pathlib import Path
from PIL import Image
import streamlit as st
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\shers\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

from car_mileage_detection.car_mileage import CarMileage


st.title('Распознавание пробега автомобиля по фотографии приборной панели')
file = st.file_uploader('Выберите jpg файл', accept_multiple_files=False, type=['jpg'])
if file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        fp = Path(tmp_file.name)
        fp.write_bytes(file.getvalue())
        st.image(Image.open(fp), caption='')
        def main(
            img_path: str = 'C:\\Users\\shers\\car_mileage_detection\\data\\original\\autoservice_priem_305_1138747_7.jpg',
            config_file: str = 'C:\\Users\\shers\\car_mileage_detection\\config\\detection_config.json'
        ) -> int:
            img_path = ''.join(['C:\\Users\\shers\\car_mileage_detection\\data\\original\\', img_path])
            low_threshold = 120
            car = CarMileage(img_path, config_file, low_threshold)
            mileage = car.detect()
            if mileage == 'NaN':
                low_threshold = 170
                while mileage == 'NaN' and low_threshold >= 80:
                    car = CarMileage(img_path, config_file, low_threshold)
                    mileage = car.detect()
                    low_threshold -= 10
            return mileage
        st.markdown(f"## Показания одометра: {main(file.name)} км")