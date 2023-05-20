import argparse
import cv2
import time
from pprint import pprint
from remo import NatureRemoAPI
from modules import constant as const
from modules.common import common as com
from modules.nature_remo.nature_remo import NatureRemo
from modules.mediapipe.hands import Hands

# FIXME  Change the button name in the code to match your environment.
ON_BUTTON_SIGNAL = 'on-100'
OFF_BUTTON_SIGNAL = 'off'
POWER_ON_STATE = 'on'
POWER_OFF_STATE = 'off'

DEBUG_FLAG = False


def main(
    config: dict,
):
    # Get configures.
    camera_id = config[const.CONF_CAMERA_ID]
    task_file_path = config[const.CONF_TASK_FILE_PATH]
    interval_time = config[const.CONF_INTERVAL_TIME]
    nr_access_token = config[const.CONF_NATURE_REMO][const.CONF_ACCESS_TOKEN]
    nr_target_nickname = config[const.CONF_NATURE_REMO][const.CONF_TARGET_NICKNAME]

    nremo = NatureRemo(nr_access_token)

    if DEBUG_FLAG:
        pprint("Your devices : {0}".format(nremo.devices))
        pprint("Your appliances : {0}".format(nremo.appliances))
        return

    target_device = nremo.search_appliance_by_nickname(
        nr_target_nickname)

    hand = Hands(task_file_path)

    cap = cv2.VideoCapture(camera_id)
    start_time = time.perf_counter() - interval_time
    while True:

        ret, frame = cap.read()

        recognition_result = hand.process(frame)

        if len(recognition_result.gestures) > 0:

            top_gesture = recognition_result.gestures[0][0]
            hand_landmarks = recognition_result.hand_landmarks[0]

            top_gesture_name = top_gesture.category_name

            # Judge gestures.
            if top_gesture_name == 'Thumb_Up':
                if time.perf_counter() - start_time > interval_time:
                    current_state = nremo.get_current_state(nr_target_nickname)
                    if current_state == POWER_OFF_STATE:
                        nremo.nr_api.send_light_infrared_signal(
                            target_device.id, ON_BUTTON_SIGNAL)
                        start_time = time.perf_counter()

            elif top_gesture_name == 'Thumb_Down':
                if time.perf_counter() - start_time > interval_time:
                    current_state = nremo.get_current_state(nr_target_nickname)
                    if current_state == POWER_ON_STATE:
                        nremo.nr_api.send_light_infrared_signal(
                            target_device.id, OFF_BUTTON_SIGNAL)
                        start_time = time.perf_counter()

            result = (top_gesture, hand_landmarks)
            res_img = hand.show(frame, result)
        else:
            res_img = frame

        cv2.imshow('frame', res_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Path to the config file.')
    args = parser.parse_args()

    config_path = args.config

    config = com.load_config(config_path)

    main(config)
