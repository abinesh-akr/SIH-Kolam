import cv2
import numpy as np
import pandas as pd

# NOTE: This version requires the opencv-contrib-python package for skeletonization.
# Ensure it's listed in your requirements.txt: pip install opencv-contrib-python

def extract_kolam_paths(img_array, canny_low=50, canny_high=150, epsilon=1.0):
    """
    Extracts Kolam paths from an image array and returns the paths and intermediate images.
    """
    if img_array is None:
        raise ValueError("Input image array cannot be None.")

    # Convert to grayscale if it's a color image
    if len(img_array.shape) == 3:
        img_gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img_array

    blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)

    # 1. Start with the accurate Canny edges.
    edges = cv2.Canny(blurred, canny_low, canny_high)

    # 2. Slightly dilate to close any tiny gaps in the Canny lines.
    kernel = np.ones((3, 3), np.uint8)
    dilated_canny = cv2.dilate(edges, kernel, iterations=1)

    # 3. Create a solid mask of the strokes by filling all contours.
    filled_mask = np.zeros_like(img_gray)
    contours, _ = cv2.findContours(dilated_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(filled_mask, contours, -1, (255), thickness=cv2.FILLED)
    
    # 4. Skeletonize the accurate, solid mask to get the perfect centerline.
    thinned = cv2.ximgproc.thinning(filled_mask)

    # 5. Find the final contours on the skeleton. These are our drawing paths.
    final_contours, _ = cv2.findContours(thinned, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    if not final_contours:
        return [], None, None, None

    # Sort paths to draw from the center outwards
    all_points = np.concatenate([cnt for cnt in final_contours])
    M_total = cv2.moments(all_points)
    if M_total["m00"] == 0:
        return [], edges, filled_mask, thinned
        
    center_x = int(M_total["m10"] / M_total["m00"])
    center_y = int(M_total["m01"] / M_total["m00"])
    
    paths_with_distances = []
    for cnt in final_contours:
        if cv2.contourArea(cnt) > 2:
            approx = cv2.approxPolyDP(cnt, epsilon, closed=False)
            path = [(int(p[0][0]), int(p[0][1])) for p in approx]
            
            M_path = cv2.moments(cnt)
            if M_path["m00"] == 0: continue
            path_cx = int(M_path["m10"] / M_path["m00"])
            path_cy = int(M_path["m01"] / M_path["m00"])
            
            distance = np.sqrt((path_cx - center_x)**2 + (path_cy - center_y)**2)
            paths_with_distances.append((distance, path))

    paths_with_distances.sort(key=lambda item: item[0])
    sorted_paths = [path for distance, path in paths_with_distances]
    
    return sorted_paths, edges, filled_mask, thinned

def save_paths_to_csv_bytes(paths):
    """Saves path data to an in-memory CSV bytes object for Streamlit download."""
    rows = []
    for i, p in enumerate(paths):
        for x, y in p:
            rows.append([x, y, i])
        rows.append([np.nan, np.nan, np.nan])
    df = pd.DataFrame(rows, columns=['x', 'y', 'path_id'])
    return df.to_csv(index=False).encode('utf-8')