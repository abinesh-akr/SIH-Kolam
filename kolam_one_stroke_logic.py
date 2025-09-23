import pandas as pd
import numpy as np
import os
import random

def get_random_image(dot_count):
    """Gets a random image path and its 1-based index from the correct folder."""
    folder_name = f"Kolam{dot_count}-Images"
    if not os.path.exists(folder_name):
        return None, None, f"Error: Folder '{folder_name}' not found."
    
    try:
        images = sorted([img for img in os.listdir(folder_name) if img.lower().endswith(('.png', '.jpg', '.jpeg'))])
        if not images:
            return None, None, f"Error: No images found in '{folder_name}'."

        # Pick a random index (0-based) and get the filename
        random_index_0based = random.randint(0, len(images) - 1)
        image_name = images[random_index_0based]
        image_path = os.path.join(folder_name, image_name)
        
        # Return the path and the 1-based index for CSV column calculation
        return image_path, random_index_0based + 1, None
    except Exception as e:
        return None, None, f"An error occurred: {e}"

def load_one_stroke_path(dot_count, image_index_1based):
    """Loads a specific column pair from the master CSV for a given dot count."""
    csv_path = os.path.join("KolamCSVfiles", f"kolam{dot_count}.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Calculate 0-based column indices. For 1st image, cols are 0,1. For 10th, cols are 18,19.
    col_x_index = (image_index_1based - 1) * 2
    col_y_index = col_x_index + 1
    
    try:
        df = pd.read_csv(csv_path, header=None, usecols=[col_x_index, col_y_index])
        print(df)
        
        # Process the points, removing any NaN rows
        x = df.iloc[1:, 0].values.flatten()
        y = df.iloc[1:, 1].values.flatten()
        pts = [(float(px), float(py)) for px, py in zip(x, y) ]
        return pts
    except Exception as e:
        raise ValueError(f"Error reading columns for image {image_index_1based} from {csv_path}. Details: {e}")

def generate_diamond_dots(max_dots=29, spacing=40):
    """Generate diamond dot layout with adjustable spacing."""
    rows = list(range(1, max_dots + 1, 2)) + list(range(max_dots - 2, 0, -2))
    coords = []
    y = (len(rows) // 2) * spacing
    for count in rows:
        x_start = -((count - 1) / 2) * spacing
        for j in range(count):
            coords.append((x_start + j * spacing, y))
        y -= spacing

    xs = [x for x, y in coords]
    ys = [y for x, y in coords]
    bbox = (min(xs) -20, min(ys)-20, max(xs)+20, max(ys)+20)
    return coords, bbox

def normalize_path(points, dot_bbox):
    """Normalizes the kolam path to fit within the dot bounding box."""
    pts = np.array(points)
    minx, miny = pts.min(0)
    maxx, maxy = pts.max(0)

    dot_minx, dot_miny, dot_maxx, dot_maxy = dot_bbox

    scale_x = (dot_maxx - dot_minx) / (maxx - minx + 1e-6)
    scale_y = (dot_maxy - dot_miny) / (maxy - miny + 1e-6)
    s = min(scale_x, scale_y) * 0.95 # Add a small margin

    xs = (pts[:, 0] - (minx + maxx) / 2) * s
    ys = (pts[:, 1] - (miny + maxy) / 2) * s
    return list(zip(xs, -ys))