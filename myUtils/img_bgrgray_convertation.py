import cv2


def bgrtogray_convertation(
        img_path: str,
        low_threshold: int = 122,
        upper_threshold: int = 255
):
    cardashboard_img = cv2.imread(img_path)
    cardashboard_img = cv2.cvtColor(cardashboard_img, cv2.COLOR_BGR2GRAY)
    (_, blackAndWhiteImage) = cv2.threshold(
        cardashboard_img,
        low_threshold,
        upper_threshold,
        cv2.THRESH_BINARY
    )
    return blackAndWhiteImage