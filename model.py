from PIL import Image
import numpy as np

def predict_image(image):
    image = image.resize((224, 224))
    img_array = np.array(image)

    brightness = img_array.mean()

    confidence = int((brightness % 100) + 50)

    if brightness < 80:
        result = "Abnormal Scan Detected"
    elif brightness < 150:
        result = "Mild Issue Detected"
    else:
        result = "Normal Scan"

    return result, confidence