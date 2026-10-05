"""
Small helpers shared by the workshop notebooks.

    from workshop import open_camera, close_camera

    cap = open_camera()
    try:
        while True:
            ret, frame = cap.read()
            ...
    finally:
        close_camera(cap)   # always runs, even if your code crashes
"""

import platform

import cv2

# Change this if you have more than one camera (e.g. 1 for an external USB webcam)
CAMERA_INDEX = 0


def open_camera(index=None, width=640, height=480):
    """Open a webcam and return the cv2.VideoCapture object.

    On Windows we use the DirectShow backend, which opens much faster and more
    reliably than OpenCV's default. 640x480 keeps everything fast on a laptop CPU.
    """
    index = CAMERA_INDEX if index is None else index
    backend = cv2.CAP_DSHOW if platform.system() == "Windows" else cv2.CAP_ANY

    cap = cv2.VideoCapture(index, backend)
    if not cap.isOpened():
        hints = {
            "Darwin": "System Settings > Privacy & Security > Camera: allow VS Code, then restart VS Code.",
            "Windows": "Settings > Privacy & security > Camera: turn on 'Let desktop apps access your camera'.",
        }
        raise RuntimeError(
            f"Could not open webcam {index}.\n"
            f"  - {hints.get(platform.system(), 'Check the camera is connected.')}\n"
            "  - Close other apps using the camera (Zoom, Teams, another notebook...).\n"
            "  - If a previous cell crashed, restart the kernel to release the camera.\n"
            "  - Got more than one camera? Try open_camera(1)."
        )

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap


def close_camera(cap):
    """Release the webcam and close all OpenCV windows."""
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)  # macOS needs an extra event pump before the windows actually close
