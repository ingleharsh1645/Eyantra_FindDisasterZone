import cv2
import numpy as np
import argparse
import os
import string

def process_arena_image(image_path):
    # Absolute path resolve
    image_path = os.path.abspath(image_path)
    
    # Step 0: Image Load Karo
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image from path: {image_path}")
        return

    # Step 1: ArUco Markers Detect Karo (IDs: 80, 85, 90, 95)
    try:
        # OpenCV 4.7+ API
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, _ = detector.detectMarkers(image)
    except Exception:
        # Fallback for older OpenCV versions
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)

    if ids is None or len(ids) < 4:
        print("Error: Could not detect all 4 ArUco markers!")
        return

    ids = ids.flatten()
    marker_dict = {}
    for i, marker_id in enumerate(ids):
        marker_dict[marker_id] = corners[i][0]

    required_ids = [80, 85, 90, 95]
    for rid in required_ids:
        if rid not in marker_dict:
            print(f"Error: Missing required marker ID {rid}")
            return

    # Step 2: Perspective Transform (900x900 Square Canvas)
    src_pts = np.float32([
        marker_dict[80][2],  # Top-Left inner corner
        marker_dict[85][3],  # Top-Right inner corner
        marker_dict[90][0],  # Bottom-Right inner corner
        marker_dict[95][1]   # Bottom-Left inner corner
    ])

    dst_pts = np.float32([
        [0, 0],
        [900, 0],
        [900, 900],
        [0, 900]
    ])

    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    rectified_image = cv2.warpPerspective(image, matrix, (900, 900))

    # Steps 3 & 4: 121 Grid Intersections Coordinate System Setup
    step = 900 // 12  # 75 pixels per cell
    cols = list(string.ascii_uppercase[:11])  # 'A' to 'K'
    rows = range(1, 12)                       # 1 to 11

    intersections = {}
    for col_idx, col_name in enumerate(cols, start=1):
        for row_idx in rows:
            x = col_idx * step
            y = row_idx * step
            intersections[f"{col_name}{row_idx}"] = (x, y)

    def get_nearest_intersection(cx, cy):
        best_name = ""
        min_dist = float('inf')
        for name, (ix, iy) in intersections.items():
            dist = np.sqrt((cx - ix)**2 + (cy - iy)**2)
            if dist < min_dist:
                min_dist = dist
                best_name = name
        return best_name

    # Step 5 & 6: Color Masking & Survivor Centroid Find Karo
    hsv = cv2.cvtColor(rectified_image, cv2.COLOR_BGR2HSV)

    # Red Color Mask (Critical Survivors)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # Yellow Color Mask (Stable Survivors)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    critical_survivors = []
    stable_survivors = []

    # Process Critical Survivors (Red)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_red:
        if cv2.contourArea(cnt) > 30:  # Noise filtering
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                loc = get_nearest_intersection(cx, cy)
                if loc not in critical_survivors:
                    critical_survivors.append(loc)

    # Process Stable Survivors (Yellow)
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_yellow:
        if cv2.contourArea(cnt) > 30:  # Noise filtering
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                loc = get_nearest_intersection(cx, cy)
                if loc not in stable_survivors:
                    stable_survivors.append(loc)

    # Step 7: Results Text File Write Karo
    base_path, _ = os.path.splitext(image_path)
    output_txt_path = f"{base_path}_results.txt"

    detected_ids_str = f"[{', '.join(map(str, sorted(ids.tolist())))}]"
    critical_str = ", ".join(critical_survivors)
    stable_str = ", ".join(stable_survivors)

    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(f"Detected marker IDs: {detected_ids_str}\n\n")
        f.write(f"Critical Survivors: {critical_str}\n")
        f.write(f"Stable Survivors: {stable_str}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Task 1A e-Yantra Survivor Detection")
    parser.add_argument("--image", required=True, help="Path to input arena image")
    args = parser.parse_args()

    process_arena_image(args.image)
    