# Kolam_Generator.py
import streamlit as st
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import cv2
import io
from skimage.metrics import structural_similarity as ssim
from skimage import filters
import math
import random

# -----------------------------
# Dependencies note:
# pip install pillow numpy opencv-python scikit-image streamlit
# -----------------------------

st.set_page_config(page_title="🎨 AI Kolam Studio (CPU)", page_icon="🌸", layout="wide")
st.markdown("<h1 style='text-align:center;'>🎨 Kolam Generator (CPU)</h1>", unsafe_allow_html=True)

# -----------------------------
# Kolam generator (procedural, CPU-friendly)
# -----------------------------
def catmull_rom_spline(P0, P1, P2, P3, nPoints=20):
    """Return points for Catmull-Rom spline segment between P1 and P2."""
    alpha = 0.5
    def tj(ti, Pi, Pj):
        xi, yi = Pi
        xj, yj = Pj
        return (( (xj - xi)**2 + (yj - yi)**2 )**0.5 )**alpha + ti
    t0 = 0.0
    t1 = tj(t0, P0, P1)
    t2 = tj(t1, P1, P2)
    t3 = tj(t2, P2, P3)
    t = np.linspace(t1, t2, nPoints)
    t = t.reshape(len(t),1)
    A1 = (t1 - t)/(t1 - t0)*np.array(P0) + (t - t0)/(t1 - t0)*np.array(P1)
    A2 = (t2 - t)/(t2 - t1)*np.array(P1) + (t - t1)/(t2 - t1)*np.array(P2)
    A3 = (t3 - t)/(t3 - t2)*np.array(P2) + (t - t2)/(t3 - t2)*np.array(P3)
    B1 = (t2 - t)/(t2 - t0)*A1 + (t - t0)/(t2 - t0)*A2
    B2 = (t3 - t)/(t3 - t1)*A2 + (t - t1)/(t3 - t1)*A3
    C = (t2 - t)/(t2 - t1)*B1 + (t - t1)/(t2 - t1)*B2
    return C.tolist()

def points_to_curve(points, samples_per_segment=24):
    if len(points) < 4:
        return points
    curve = []
    # For closed curve, wrap points
    pts = points
    n = len(pts)
    for i in range(n):
        P0 = pts[(i - 1) % n]
        P1 = pts[i % n]
        P2 = pts[(i + 1) % n]
        P3 = pts[(i + 2) % n]
        seg = catmull_rom_spline(P0, P1, P2, P3, nPoints=samples_per_segment)
        curve.extend(seg)
    return curve

def generate_dot_grid(center, step, layers):
    """Generate a stepped dot grid counts like 1-3-5-... around center"""
    cx, cy = center
    grid = []
    for layer in range(layers):
        count = 1 + 2*layer  # 1,3,5,...
        radius = step * layer
        ring = []
        for i in range(count):
            theta = 2 * math.pi * i / count
            x = cx + radius * math.cos(theta)
            y = cy + radius * math.sin(theta)
            ring.append((x, y))
        grid.append(ring)
    return grid

def generate_kolam_image(img_size=800, grid_layers=5, complexity=0.6, palette=None, stroke_width=6):
    """
    Generate a kolam-like design:
      - img_size: output square size
      - grid_layers: number of concentric dot-rings (1 -> 1,3)
      - complexity: [0..1] how many connecting paths / detail
      - palette: dict with 'bg' and 'stroke'
    """
    if palette is None:
        palette = {"bg": (28, 28, 28), "stroke": (255, 255, 255)}
    w = h = img_size
    base = Image.new("RGB", (w, h), palette["bg"])
    draw = ImageDraw.Draw(base)

    cx, cy = w // 2, h // 2
    step = img_size // (2 * (grid_layers + 1))
    dot_grid = generate_dot_grid((cx, cy), step, grid_layers)

    # draw subtle textured background
    bg_noise = Image.effect_noise((w, h), 12).convert("L").filter(ImageFilter.GaussianBlur(1))
    base.paste(Image.merge("RGB", [bg_noise.point(lambda p: palette["bg"][0])]*3), (0,0), bg_noise.point(lambda p: p//10))

    # create mask for lines (so we can blur/anti-alias nicely)
    mask = Image.new("L", (w, h), 0)
    mdraw = ImageDraw.Draw(mask)

    # generate curves: for each ring produce a loop by sampling points
    loops = []

    # Outer-most loop: connect ring points to make large curves
    for ri, ring in enumerate(dot_grid):
        # skip rings with <3 points (first ring could be single dot)
        if len(ring) < 3:
            continue
        # choose control points along ring with slight random radial jitter controlled by complexity
        jitter = (1 - complexity) * 0.15 + complexity * 0.35
        pts = []
        for (x, y) in ring:
            # shift radially a little to produce graceful loops
            dx = x - cx
            dy = y - cy
            r = math.hypot(dx, dy)
            angle = math.atan2(dy, dx)
            r2 = r * (1 + (random.uniform(-jitter, jitter) * (0.8 - ri*0.05)))
            x2 = cx + r2 * math.cos(angle)
            y2 = cy + r2 * math.sin(angle)
            pts.append((x2, y2))
        curve = points_to_curve(pts, samples_per_segment=28)
        loops.append((curve, max(1, int(stroke_width * (1 - ri * 0.08)))))  # vary width slowly

    # add connecting radiating loops: create additional small loops between rings based on complexity
    extra = int(round(len(loops) * (complexity * 2)))
    for e in range(extra):
        # choose two rings and interpolate
        if len(dot_grid) < 2:
            break
        r1 = random.randrange(1, len(dot_grid))
        count = len(dot_grid[r1])
        pts = []
        for i in range(count):
            p1 = dot_grid[r1][i]
            p2 = dot_grid[max(0, r1-1)][i % max(1, len(dot_grid[max(0, r1-1)]))]
            # midpoints with jitter
            mx = (p1[0] + p2[0]) / 2 + random.uniform(-step*0.2, step*0.2) * complexity
            my = (p1[1] + p2[1]) / 2 + random.uniform(-step*0.2, step*0.2) * complexity
            pts.append((mx, my))
        curve = points_to_curve(pts, samples_per_segment=18)
        loops.append((curve, max(1, int(stroke_width * 0.6))))

    # draw loops into mask
    for (curve, wth) in loops:
        # convert curve to int tuples
        poly = [(int(round(x)), int(round(y))) for (x, y) in curve]
        # draw polyline (closed)
        if len(poly) > 2:
            mdraw.line(poly + [poly[0]], fill=255, width=wth, joint="curve")

    # slight morphological close to make lines continuous
    m_np = np.array(mask)
    kernel = np.ones((3,3), np.uint8)
    m_np = cv2.morphologyEx(m_np, cv2.MORPH_CLOSE, kernel, iterations=1)
    mask = Image.fromarray(m_np)

    # apply a small gaussian to anti-alias and make it 'hand-drawn'
    mask = mask.filter(ImageFilter.GaussianBlur(radius=1.2))

    # draw final strokes onto base using mask
    stroke_img = Image.new("RGB", (w, h), (0,0,0))
    sdraw = ImageDraw.Draw(stroke_img)
    # paint white/stroke color where mask > 0
    stroke_color = palette["stroke"]
    s_np = np.array(mask)
    stroke_img_np = np.zeros((h, w, 3), dtype=np.uint8)
    stroke_img_np[s_np > 10] = stroke_color
    stroke_img = Image.fromarray(stroke_img_np)

    # blend stroke onto base with preserve of background
    final = Image.composite(stroke_img, base, mask)

    # optionally draw dots for authenticity (small white points on the grid)
    dot_layer = Image.new("RGBA", (w, h), (255,255,255,0))
    dd = ImageDraw.Draw(dot_layer)
    for ring in dot_grid:
        for (x,y) in ring:
            r = max(1, int(step * 0.06))
            dd.ellipse([x-r, y-r, x+r, y+r], fill=stroke_color + (255,))
    final = Image.alpha_composite(final.convert("RGBA"), dot_layer).convert("RGB")

    # final smoothing/toning
    final = final.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
    return final

# -----------------------------
# KOLAM ACCURACY ANALYZER (kept from your original file - minimal)
# -----------------------------
class KolamAnalyzer:
    def __init__(self):
        self.weights = {
            'symmetry': 0.45,
            'continuous_lines': 0.35,
            'dot_presence': 0.20
        }

    def preprocess_image(self, image):
        if isinstance(image, Image.Image):
            img_array = np.array(image.convert('L'))
        else:
            img_array = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = filters.gaussian(img_array, sigma=1.0)
        binary = blurred < filters.threshold_otsu(blurred)
        return (binary.astype(np.uint8) * 255)

    def check_symmetry(self, image):
        processed = self.preprocess_image(image)
        h, w = processed.shape
        left_half = processed[:, :w//2]
        right_half = np.fliplr(processed[:, w//2:])
        min_width = min(left_half.shape[1], right_half.shape[1])
        left_half = left_half[:, :min_width]
        right_half = right_half[:, :min_width]
        try:
            vertical_score = ssim(left_half, right_half)
        except ValueError:
            vertical_score = 0.0

        top_half = processed[:h//2, :]
        bottom_half = np.flipud(processed[h//2:, :])
        min_height = min(top_half.shape[0], bottom_half.shape[0])
        top_half = top_half[:min_height, :]
        bottom_half = bottom_half[:min_height, :]
        try:
            horizontal_score = ssim(top_half, bottom_half)
        except ValueError:
            horizontal_score = 0.0

        return (vertical_score + horizontal_score) / 2

    def check_continuous_lines(self, image):
        processed = self.preprocess_image(image)
        kernel = np.ones((3, 3), np.uint8)
        processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return 0.0
        total_length = sum(cv2.arcLength(c, True) for c in contours)
        avg_length = total_length / len(contours)
        diag = np.sqrt(processed.shape[0] ** 2 + processed.shape[1] ** 2)
        return min(1.0, max(avg_length / (diag * 0.6), 0.0))

    def detect_dots(self, image):
        processed = self.preprocess_image(image)
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 5
        params.maxArea = 200
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(processed)
        return len(keypoints)

    def calculate_overall_accuracy(self, image):
        scores = {}
        scores['symmetry'] = self.check_symmetry(image)
        scores['continuous_lines'] = self.check_continuous_lines(image)
        dot_count = self.detect_dots(image)
        scores['dot_presence'] = min(dot_count / 20, 1.0)
        overall_score = sum(scores[k] * self.weights[k] for k in scores)
        return max(0.0, min(overall_score, 1.0)), scores

# -----------------------------
# Streamlit UI (kept similar)
# -----------------------------
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = KolamAnalyzer()
if "gallery" not in st.session_state:
    st.session_state.gallery = []

# Sidebar
st.sidebar.header("🎨 Kolam Design Studio (CPU)")
col1, col2 = st.sidebar.columns(2)
with col1:
    kolam_type = st.selectbox("Kolam Style", ["Sikku Kolam", "Pulli Kolam", "Rangoli", "Geometric Kolam"], index=1)
    state = st.selectbox("Regional Style", ["Tamil Nadu", "Karnataka", "Andhra Pradesh", "Kerala", "Telangana"])
with col2:
    complexity = st.slider("Complexity", 0.1, 1.0, 0.6)
    grid_layers = st.slider("Grid Layers (1 = small)", 2, 8, 5)

color_palettes = {
    "Traditional White": {"bg": (20,20,20), "stroke": (255,255,255)},
    "Vibrant Festival": {"bg": (34,18,12), "stroke": (255,165,90)},
    "Pastel Dream": {"bg": (250,250,250), "stroke": (130,90,200)}
}
color_scheme = st.sidebar.selectbox("Color Theme", list(color_palettes.keys()))
occasion = st.sidebar.selectbox("Occasion", ["Daily Practice", "Diwali", "Pongal", "Wedding"])
custom_elements = st.sidebar.text_area("Custom Elements", placeholder="peacock motifs, temple arches...", height=80)

if st.sidebar.button("✨ Generate Kolam", use_container_width=True):
    with st.spinner("🎭 Creating kolam on CPU..."):
        try:
            palette = color_palettes[color_scheme]
            image = generate_kolam_image(img_size=900, grid_layers=grid_layers, complexity=float(complexity), palette=palette, stroke_width=8)

            overall_score, detailed_scores = st.session_state.analyzer.calculate_overall_accuracy(image)
            st.session_state.gallery.append((image, state, overall_score, detailed_scores))

            col1, col2 = st.columns([2, 1])
            with col1:
                st.image(image, use_column_width=True, caption=f"✨ {kolam_type} Kolam — {state}")
                buffer = io.BytesIO()
                image.save(buffer, format="PNG")
                st.download_button(label="⬇ Download Kolam", data=buffer.getvalue(), file_name=f"{kolam_type}_{state}.png", mime="image/png")
            with col2:
                st.subheader("📊 Kolam Accuracy Analysis")
                accuracy_percentage = overall_score * 100
                st.markdown(f"### {'🟢' if accuracy_percentage>70 else '🟡'} Overall Score: {accuracy_percentage:.1f}%")
                st.progress(overall_score)
                st.write(f"🔄 Symmetry: {detailed_scores['symmetry']*100:.1f}%")
                st.write(f"➰ Continuous Lines: {detailed_scores['continuous_lines']*100:.1f}%")
                st.write(f"⚫ Dot Presence: {detailed_scores['dot_presence']*100:.1f}%")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Gallery
if st.session_state.gallery:
    st.markdown("### 🖼 Previous Kolams")
    cols = st.columns(3)
    for idx, (img, state_name, acc, _) in enumerate(sorted(st.session_state.gallery, key=lambda x: x[2], reverse=True)):
        with cols[idx % 3]:
            st.image(img, caption=f"{state_name} ({acc*100:.1f}%)", use_column_width=True)
