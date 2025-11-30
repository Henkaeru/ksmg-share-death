import cv2
import numpy as np
import mss
import time
import threading

class ImageDetector:
    def __init__(self, templates, callback, fps=10, match_threshold=100, distance_threshold=42):
        """
        templates: dict{name: filepath}
        callback: function(name) -> called when template detected
        fps: detection frequency
        match_threshold: minimum good matches to trigger
        distance_threshold: max ORB distance for good matches
        """
        self.templates = templates
        self.callback = callback
        self.fps = fps
        self.match_threshold = match_threshold
        self.distance_threshold = distance_threshold

        self.orb = cv2.ORB_create(nfeatures=500)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        self.template_data = {}
        for name, path in templates.items():
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if img is None:
                raise FileNotFoundError(f"Template not found: {path}")

            if img.shape[2] == 4:
                img_bgr = cv2.cvtColor(img[:, :, :3], cv2.COLOR_RGB2BGR)
            else:
                img_bgr = img

            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            kp, des = self.orb.detectAndCompute(gray, None)
            self.template_data[name] = {"img": img_bgr, "gray": gray, "kp": kp, "des": des}

    def _detection_loop(self):
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            screen_w, screen_h = monitor['width'], monitor['height']

            # Top-right quarter
            crop_x = screen_w // 2
            crop_y = 0
            crop_w = screen_w - crop_x
            crop_h = screen_h // 2

            while True:
                start_time = time.time()
                sct_img = sct.grab({
                    "left": crop_x,
                    "top": crop_y,
                    "width": crop_w,
                    "height": crop_h
                })
                screenshot = np.array(sct_img)[:, :, :3]
                screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
                gray_screenshot = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)

                for name, data in self.template_data.items():
                    if data["des"] is None:
                        continue

                    kp1, des1 = data["kp"], data["des"]
                    kp2, des2 = self.orb.detectAndCompute(gray_screenshot, None)
                    if des2 is None or len(des2) < 2:
                        continue

                    matches = self.bf.match(des1, des2)
                    good_matches = [m for m in matches if m.distance < self.distance_threshold]

                    if len(good_matches) >= self.match_threshold:
                        self.callback(name)
                        time.sleep(1)  # pause after detection

                # Maintain fps
                elapsed = time.time() - start_time
                time.sleep(max(1/self.fps - elapsed, 0))

    def start(self):
        t = threading.Thread(target=self._detection_loop, daemon=True)
        t.start()
