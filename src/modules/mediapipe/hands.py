import cv2
import copy
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


class Hands:
    def __init__(
        self,
        task_path: str,
    ):
        """Initializer.

        Args:
            task_path (str): Path to the task file.
        """
        base_options = python.BaseOptions(
            model_asset_path=task_path)
        options = vision.GestureRecognizerOptions(base_options=base_options)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def process(
        self,
        image,
    ):
        """Recognize gestures from the image.

        Args:
            image (numpy.ndarray): Image to recognize.

        Returns:
            results (GestureRecognizerResult): Recognition results.
        """
        im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = mp.Image(
            image_format=mp.ImageFormat.SRGB, data=np.asarray(im_rgb))
        results = self.recognizer.recognize(image)
        return results

    def show(
        self,
        image,
        results,
    ):
        """Show the recognition results on the image.

        Args:
            image (numpy.ndarray): Image to show.
            results (tuple): Recognition results.

        Returns:
            res_img (numpy.ndarray): Image with the recognition results.
        """
        gestures = results[0]
        multi_hand_landmarks = results[1]

        res_img = copy.deepcopy(image)
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in multi_hand_landmarks
        ])

        mp_drawing.draw_landmarks(
            res_img,
            hand_landmarks_proto,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

        title = f"{gestures.category_name} ({gestures.score:.2f})"
        cv2.putText(res_img, title, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2, cv2.LINE_AA)

        return res_img
