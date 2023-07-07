import cv2


def bgrtogray_binarization(
        img_path: str,
        low_threshold: int = 122,
        upper_treshold: int = 255
):
    cardashboard_img = cv2.imread(img_path)
    cardashboard_img = cv2.cvtColor(cardashboard_img, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(
        cardashboard_img,
        low_threshold,
        upper_treshold,
        cv2.THRESH_BINARY
    )
    return cv2.bitwise_not(blackAndWhiteImage)