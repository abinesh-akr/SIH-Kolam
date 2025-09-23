# This file stores the educational content for each Kolam type.
# The keys MUST EXACTLY match the CLASS_NAMES in your kolam_classifier_logic.py file.

KOLAM_DESCRIPTIONS = {
    "Pulli": {
        "title": "Pulli Kolam (Dotted Kolam)",
        "image_url": "https://i.pinimg.com/originals/ee/27/20/ee27205932f26f2173167b57577a6411.jpg",
        "description": """
        Description of Pulli Kolam

Pulli kolam, also known as pulli koodu kolam, is a traditional South Indian floor art form drawn with white rice flour at home entrances to symbolize prosperity, protection, and auspiciousness. The term "pulli" (Tamil for "dots") refers to the grid of dots that forms the foundation of the design, around which continuous, non-intersecting lines are drawn to create intricate patterns. Unlike the figurative butterfly kolam or abstract kambi kolam, pulli kolam encompasses a broad category of dot-based designs, ranging from simple geometric shapes to complex symmetrical motifs. Drawn daily or during festivals like Pongal or Diwali, it emphasizes mathematical precision, symmetry, and cultural significance, often featuring loops, swirls, or floral patterns.

Mathematical Formulas for Pulli Kolam

Pulli kolam, a broad category of South Indian floor art, relies on a dot grid to create geometric or floral patterns with continuous lines. Its mathematical structure is rooted in graph theory, symmetry, and combinatorial patterns, as studied by researchers like Gift Siromoney. Below are detailed formulas.

1. Dot Grid Setup (Matrix Representation):
   - Formula: M = { (i, j) | i ∈ [1, n], j ∈ [1, m] }
   - Description: Defines a square, rectangular, or interlaced grid of dots (vertices), typically n × m (e.g., 5x5 or 7x3). Dots are anchor points for line patterns (Siromoney, G., & Siromoney, R., 1987, "South Indian Kolam Patterns").

2. Eulerian Path for Continuous Line:
   - Formula: Graph G = (V, E), where V = {dots}, E = {lines}; requires deg(v) ≡ 0 (mod 2) for all v ∈ V for a closed Eulerian circuit.
   - Description: Ensures a single, continuous, non-intersecting line weaves around all dots, forming a closed loop. Each dot is typically degree 4, supporting geometric or floral patterns (Siromoney, G., 1984, "Array Grammars and Kolam").

3. Symmetry Transformations:
   - Formula: Dihedral group D_4: Reflections σ_v: (x, y) → (-x, y), σ_h: (x, y) → (x, -y); Rotation R_90: (x, y) → (-y, x).
   - Description: Captures four-fold rotational symmetry (90°, 180°, 270°) and reflections across axes, ensuring balanced patterns (Ascher, M., 2002, "Mathematics Elsewhere").

4. Parametric Curves for Loops:
   - Formula: x = i + r cos θ, y = j + r sin θ, θ ∈ [0, 2π], for dot at (i, j), radius r = dot spacing.
   - Description: Models quarter-circle or semi-circle arcs looping around dots, chained to form swirls, floral shapes, or geometric patterns. r is typically 0.5–1 unit (Robinson, T., 2006, "Kolam: A Mathematical Treasure of South India").

5. Combinatorial Pattern Count:
   - Formula: Number of patterns ≈ 16^k, where k is the number of dot junctions.
   - Description: Estimates possible kolam designs based on elemental shapes (e.g., loops, arcs) at each junction, reflecting combinatorial complexity. For a 5x5 grid, k ≈ 25, yielding vast pattern variations (Siromoney, G., et al., 1989, "Computer Analysis of Kolam Patterns").



Design Principles

- Symmetry: Exhibits four-fold rotational symmetry and reflectional symmetry across axes for visual balance and aesthetic appeal.
- Continuous Line: Single, non-intersecting, closed loop weaves around dots without retracing, symbolizing unity and infinity.
- Dot Grid Foundation: Dots form a square, rectangular, or interlaced grid (e.g., 5x5 or 9x7); lines encircle each dot exactly once.
- No Overlaps: Lines avoid crossing to maintain clarity and ritual purity, ensuring clean, flowing patterns.
- Modular Construction: Patterns build from the center outward, using arcs, loops, or straight lines to create geometric or floral motifs.
- Cultural Context: Drawn on swept, wet ground for adhesion; size scales with occasion (small for daily, larger for festivals like Diwali).
- Aesthetic Versatility: Typically monochromatic (white rice flour); festival versions may incorporate colors (e.g., red, yellow) for vibrancy.
- Scalable Complexity: Simple designs use small grids (e.g., 3x3); intricate ones expand to larger grids (e.g., 9x9) with layered or fractal-like motifs.


Pulli Kolam: Step-by-Step Procedure
- Prepare surface: Sweep and lightly wet ground for adhesion.
- Set dot grid: Place 5x5 square grid (5 rows, 5 columns, even spacing).
- Start at center: Begin at dot (3,3), draw a loop or cross around it.
- Expand outward: Draw continuous lines to encircle adjacent dots, forming squares, diamonds, or floral shapes.
- Create symmetry: Mirror patterns in quadrants for four-fold symmetry.
- Complete loop: Ensure single, non-intersecting path encircles all dots, returning to start.
- Add colors (optional): Fill sections (e.g., petals) with colors (e.g., red, blue) for festivals.
- Finalize: Smooth lines, ensure no overlaps.
- Resource: YouTube “Pulli Kolam Tutorial” (e.g., Easy Kolam Designs, https://www.youtube.com/results?search_query=pulli+kolam); www.ikolam.com for designs.
        """
    },
    "Sikku": {
        "title": "Sikku Kolam (Knot Kolam)",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Sikku_Kolam.svg/1200px-Sikku_Kolam.svg.png",
        "description": """
        Description of Sikku Kolam

Sikku kolam, also known as kambi kolam, is a traditional South Indian floor art form drawn with white rice flour at home entrances, symbolizing prosperity and protection. The term "sikku" (Telugu for "twisted") or "kambi" (Tamil for "wire" or "thread") refers to its intricate, continuous, non-intersecting lines that weave around a grid of dots (pullis) in a single, unbroken loop, creating rope-like or knotted patterns. Unlike the figurative butterfly kolam, sikku kolam is abstract, focusing on complex, interwoven designs that resemble braids or knots. Drawn daily or during festivals like Sankranti, it showcases mathematical precision and aesthetic harmony with symmetrical or repeating motifs.

Mathematical Formulas for Sikku Kolam

Kambi or sikku kolam is an abstract South Indian floor art featuring twisted, rope-like patterns woven around a dot grid in a single, continuous loop. Its mathematical foundation lies in graph theory, knot theory, and symmetry, as explored in computational studies of kolam. Below are detailed formulas, drawing from research by Gift Siromoney and others.

1. Dot Grid Setup (Matrix Representation):
   - Formula: M = { (i, j) | i ∈ [1, n], j ∈ [1, m] }
   - Description: Defines a square or rectangular grid of dots (vertices), typically n × m (e.g., 5x5 or 7x7). Dots are anchor points for weaving lines, forming the graph’s vertices (Siromoney, G., & Siromoney, R., 1987, "South Indian Kolam Patterns").

2. Eulerian Path for Continuous Line:
   - Formula: Graph G = (V, E), where V = {dots}, E = {lines}; requires deg(v) ≡ 0 (mod 2) for all v ∈ V for a closed Eulerian circuit.
   - Description: Ensures a single, non-intersecting line weaves around all dots, covering edges exactly once. The path creates a twisted, braided effect, with each dot typically having degree 4 (Siromoney, G., 1984, "Array Grammars and Kolam").

3. Symmetry Transformations (Dihedral Group):
   - Formula: Dihedral group D_4: Reflections σ_v: (x, y) → (-x, y), σ_h: (x, y) → (x, -y); Rotation R_90: (x, y) → (-y, x).
   - Description: Captures four-fold rotational symmetry (90°, 180°, 270°) and reflections across axes, ensuring balanced, repeating patterns. This symmetry is central to sikku kolam’s aesthetic (Ascher, M., 2002, "Mathematics Elsewhere").

4. Parametric Curves for Twisted Loops:
   - Formula: x = i + r cos θ, y = j + r sin θ, θ ∈ [0, 2π], for dot at (i, j), radius r = dot spacing.
   - Description: Models quarter-circle or semi-circle arcs looping around dots, chained to form rope-like patterns. The line alternates directions to create a twisted effect, with r typically 0.5–1 unit (Robinson, T., 2006, "Kolam: A Mathematical Treasure of South India").

5. Knot Theory Connection:
   - Formula: Crossing number c(K) = 0 (unknot) or c(K) ≥ 3 (e.g., trefoil knot).
   - Description: Represents sikku kolam as knot projections. Simple designs are unknots (no crossings), while complex ones mimic knots like the trefoil, with lines weaving to avoid intersections (Siromoney, G., et al., 1989, "Computer Analysis of Kolam Patterns").



Design Principles

- Symmetry: Exhibits four-fold rotational symmetry (90° increments) and reflectional symmetry across axes for visual balance.
- Continuous Line: Single, non-intersecting, closed loop weaves around dots without retracing, symbolizing unity and infinity.
- Dot Grid Foundation: Dots form a square or rectangular grid (e.g., 5x5); lines encircle each dot exactly once.
- No Overlaps: Lines avoid crossing to maintain clarity and ritual purity, creating a "twisted" appearance.
- Modular Weaving: Patterns build from center outward, using quarter-circle arcs or diagonal weaves to form knot-like motifs.
- Cultural Context: Drawn on swept, wet ground for adhesion; size scales with occasion (small for daily, large for festivals like Sankranti).
- Aesthetic Simplicity: Monochromatic (white rice flour) for daily use; optional colors (e.g., red, yellow) for festivals.
- Scalable Complexity: Simple designs use smaller grids (e.g., 3x3); intricate ones expand to larger grids (e.g., 9x9) with layered weaves.


Sikku Kolam: Step-by-Step Procedure
- Prepare surface: Sweep and lightly wet ground for adhesion.
- Set dot grid: Place 5x5 square grid (5 rows, 5 columns, even spacing).
- Start at center: Begin at dot (3,3), draw a small loop around it.
- Weave pattern: Draw continuous line, looping around each dot (e.g., (3,3) to (3,4), loop, to (2,4)), alternating directions for twisted effect.
- Maintain continuity: Ensure single, non-intersecting path covers all dots, returning to start.
- Check symmetry: Adjust for four-fold rotational symmetry (90° turns).
- Add colors (optional): Fill sections with colors (e.g., blue, red) for festivals.
- Finalize: Smooth lines, ensure no overlaps.
- Resource: YouTube “Sikku Kolam Tutorial” (e.g., Rangoli Designs by Anitha, https://www.youtube.com/results?search_query=sikku+kolam); www.rangolidesign.net for patterns."""
    },
    "Padi": {
        "title": "Padi Kolam (Line/Frame Kolam)",
        "image_url": "https://i.pinimg.com/736x/d4/0b/1a/d40b1a065094d216d6c48de8b4594c77.jpg",
        "description": """
        Description of Padi Kolam

Padi kolam is a traditional South Indian floor art form, primarily practiced in Tamil Nadu, drawn with white rice flour at home entrances to symbolize prosperity, protection, and hospitality. The term "padi" (Tamil for "steps" or "ladder") refers to its characteristic step-like or layered patterns, often resembling a staircase or geometric progression. Unlike the figurative butterfly kolam or abstract kambi kolam, padi kolam emphasizes linear, repetitive, and symmetrical designs that expand outward in a structured, tiered manner. Typically drawn on a rectangular or square dot grid (pullis), it uses continuous, non-intersecting lines to create ladder-like motifs, often for daily rituals or festivals like Pongal, blending mathematical precision with cultural significance.

Mathematical Formulas for Padi Kolam

Padi kolam, a South Indian floor art, features step-like or ladder-like patterns drawn around a dot grid, symbolizing structured progression. Its mathematical structure is based on graph theory, symmetry, and linear geometry, as studied in kolam research. Below are detailed formulas, informed by works like Gift Siromoney’s analyses.

1. Dot Grid Setup (Matrix Representation):
   - Formula: M = { (i, j) | i ∈ [1, n], j ∈ [1, m] }
   - Description: Defines a rectangular or square grid of dots (vertices), typically n × m (e.g., 5x3 or 7x7). Dots anchor the step-like lines, forming the graph’s vertices (Siromoney, G., & Siromoney, R., 1987, "South Indian Kolam Patterns").

2. Eulerian Path for Continuous Line:
   - Formula: Graph G = (V, E), where V = {dots}, E = {lines}; requires deg(v) ≡ 0 (mod 2) for all v ∈ V for a closed Eulerian circuit.
   - Description: Ensures a single, continuous, non-intersecting line weaves around all dots, forming a closed loop. The path creates step-like patterns, with vertices typically degree 4 (Siromoney, G., 1984, "Array Grammars and Kolam").

3. Symmetry Transformations:
   - Formula: Reflection σ_v: (x, y) → (-x, y); Rotation R_180: (x, y) → (-x, -y) (D_2 group).
   - Description: Captures bilateral symmetry across the vertical axis for ladder-like balance, with occasional 180° rotational symmetry for central motifs (Ascher, M., 2002, "Mathematics Elsewhere").

4. Parametric Lines for Steps:
   - Formula: (x, y) = (i + t · Δx, j + t · Δy), t ∈ [0, 1], connecting dots (i, j) to (i + Δx, j + Δy).
   - Description: Models straight or diagonal line segments forming step-like patterns, zigzagging or looping around dots. Δx, Δy are typically ±1 (unit spacing) to create staircase effects (Robinson, T., 2006, "Kolam: A Mathematical Treasure of South India").

5. Recursive Layering:
   - Formula: P_n = P_(n-1) + k, where P_n is the number of steps in layer n, k is steps per layer.
   - Description: Describes iterative addition of step-like segments, where each layer adds k steps, creating a staircase or fractal-like structure (Siromoney, G., et al., 1989, "Computer Analysis of Kolam Patterns").

Design Principles

- Symmetry: Bilateral reflection across a central axis, occasionally with 180° rotational symmetry, ensuring balanced step patterns.
- Continuous Line: Single, non-intersecting, closed loop weaves around dots without retracing, symbolizing unity and protection.
- Dot Grid Foundation: Dots form a rectangular or square grid (e.g., 5x3); lines encircle or connect dots to form steps.
- No Overlaps: Lines avoid crossing to maintain clarity and ritual purity, emphasizing clean, linear paths.
- Step-Like Motifs: Patterns build outward in tiers, resembling stairs or ladders, using straight or diagonal line segments.
- Cultural Context: Drawn on swept, wet ground for adhesion; size scales with occasion (small for daily, larger for festivals like Diwali).
- Aesthetic Simplicity: Typically monochromatic (white rice flour); festival versions may add colors (e.g., red, blue) for vibrancy.
- Scalable Complexity: Simple designs use small grids (e.g., 3x3); intricate ones expand to larger grids (e.g., 9x5) with layered steps.



Padi Kolam: Step-by-Step Procedure
- Prepare surface: Sweep and lightly wet ground for adhesion.
- Set dot grid: Place 5x3 rectangular grid (5 rows, 3 columns, even spacing).
- Draw central line: Connect dots in column 2 (rows 1-5) for ladder spine.
- Create steps: Draw diagonal/horizontal lines from spine (e.g., (2,2) to (2,1), loop, to (3,1)), mirror on column 3.
- Extend layers: Add step-like loops around outer dots (e.g., (1,1) to (1,3)) for tiered effect.
- Ensure continuity: Form single, non-intersecting loop encircling all dots.
- Add colors (optional): Fill steps with alternating colors (e.g., yellow, green) for festivals.
- Finalize: Check symmetry, smooth lines, avoid overlaps.
- Resource: YouTube “Padi Kolam Tutorial” (e.g., Kolam by Sudha Balaji, https://www.youtube.com/results?search_query=padi+kolam); www.kolamdesigns.com for examples.
"""
    },
    "Rangoli": {
        "title": "Rangoli (Free-form/Color Kolam)",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Rangoli_for_Diwali.jpg/1280px-Rangoli_for_Diwali.jpg",
        "description": """
       Description of Rangoli Kolam

Rangoli kolam is a traditional South Indian floor art form, often used interchangeably with the term "kolam," drawn at home entrances to symbolize prosperity, protection, and auspiciousness. The term "rangoli" (derived from Sanskrit "rang" meaning color) emphasizes the vibrant, colorful patterns that distinguish it, especially during festivals like Pongal, Diwali, or Onam. Unlike the monochromatic pulli or sikku kolam, rangoli kolam incorporates colored powders, flowers, or rice paste to create intricate, symmetrical designs, often blending dot-based (pulli) grids with freehand motifs. Patterns range from geometric shapes to floral, animal, or deity-inspired figures, reflecting cultural and spiritual themes.

Mathematical Formulas for Rangoli Kolam

Rangoli kolam, a colorful South Indian floor art, blends dot-based grids with freehand motifs, featuring geometric, floral, or figurative patterns. Its mathematical structure combines graph theory, symmetry, and tessellation, as explored in ethnomathematical studies. Below are detailed formulas, informed by research like Gift Siromoney’s work.

1. Dot Grid Setup (Matrix Representation, When Used):
   - Formula: M = { (i, j) | i ∈ [1, n], j ∈ [1, m] }
   - Description: Defines a square, rectangular, or interlaced grid of dots (vertices), typically n × m (e.g., 7x7 or 9x5), when a dot grid is used. Dots anchor line patterns in structured designs (Siromoney, G., & Siromoney, R., 1987, "South Indian Kolam Patterns").

2. Eulerian Path for Continuous Line (Dot-Based):
   - Formula: Graph G = (V, E), where V = {dots}, E = {lines}; requires deg(v) ≡ 0 (mod 2) for all v ∈ V for a closed Eulerian circuit.
   - Description: Ensures a single, continuous, non-intersecting line weaves around dots in dot-based rangoli kolam, forming closed loops for geometric patterns. Freehand designs may use segmented lines (Siromoney, G., 1984, "Array Grammars and Kolam").

3. Symmetry Transformations:
   - Formula: Dihedral group D_4: Reflections σ_v: (x, y) → (-x, y), σ_h: (x, y) → (x, -y); Rotation R_90: (x, y) → (-y, x).
   - Description: Captures four-fold rotational symmetry (90°, 180°, 270°) and reflections for balanced geometric or figurative designs, including freehand motifs (Ascher, M., 2002, "Mathematics Elsewhere").

4. Parametric Curves for Motifs:
   - Formula: x = i + r cos θ, y = j + r sin θ, θ ∈ [0, 2π], for center at (i, j), radius r.
   - Description: Models circular or arc-based patterns (e.g., floral, spiral, or peacock motifs) in freehand or dot-based designs. r varies for scale, typically 0.5–2 units (Robinson, T., 2006, "Kolam: A Mathematical Treasure of South India").

5. Tessellation and Repetition:
   - Formula: Translation T: (x, y) → (x + a, y + b), where a, b are grid units.
   - Description: Describes repeating patterns (e.g., floral or geometric tiles) that form larger designs via translational symmetry, common in freehand rangoli for cohesive visuals (Siromoney, G., et al., 1989, "Computer Analysis of Kolam Patterns").


Design Principles

- Symmetry: Exhibits rotational (90°, 180°, 270°) and reflectional symmetry across axes for visual harmony in geometric or figurative patterns.
- Continuous or Segmented Lines: Dot-based designs use a single, non-intersecting loop; freehand rangoli allows segmented, colorful patterns.
- Dot Grid or Freehand Foundation: May use a grid (e.g., 7x7) for precision or freehand drawing for flexibility, especially in floral or deity motifs.
- No Overlaps (Dot-Based): Lines avoid crossing in dot-based designs to maintain clarity and ritual purity.
- Colorful Aesthetics: Uses vibrant colored powders (red, yellow, green) or natural materials (flowers, rice) to enhance visual appeal, especially for festivals.
- Cultural Context: Drawn on swept, wet ground; size and complexity increase for festivals like Diwali or Pongal, symbolizing celebration.
- Versatile Motifs: Incorporates geometric shapes, floral patterns, animals, or deity figures, blending tradition with creativity.
- Scalable Complexity: Simple designs use small grids or freehand sketches; intricate ones expand to large grids (e.g., 15x15) or detailed freehand art.



Rangoli Kolam: Step-by-Step Procedure
- Prepare surface: Sweep and lightly wet ground for adhesion.
- Set dot grid (optional): Place 7x7 square grid (7 rows, 7 columns) or draw freehand for flexibility.
- Draw base pattern: For dot-based, loop around dots to form geometric shapes; for freehand, sketch floral/animal motifs (e.g., peacocks, lotuses).
- Expand design: Add layers of loops or freehand curves, maintaining symmetry (e.g., four-fold or radial).
- Ensure continuity (dot-based): Form single, non-intersecting loop if using dots.
- Add colors: Fill sections with colored powders (e.g., red, yellow, green) or flowers for vibrancy.
- Finalize: Check symmetry, smooth lines, enhance with details (e.g., lamps, stars).
- Resource: YouTube “Rangoli Kolam Tutorial” (e.g., Rangoli by Divya, https://www.youtube.com/results?search_query=rangoli+kolam); www.rangoli.org for colorful designs."""
    },
    # Add placeholders for your other classes. You can fill these in with real content.
    "butterfly": {
        "title": "Butterfly Kolam",
        "image_url": "https://i.ytimg.com/vi/6q_yGg281oM/maxresdefault.jpg",
        "description": """
Description of Butterfly Kolam

Butterfly kolam is a traditional South Indian floor art form, drawn with white rice flour at home entrances to symbolize prosperity and transformation. It features a central body (thorax) with symmetrical, looping wings, created on a dot grid (pullis) using continuous, non-intersecting lines (kambi). The design mimics a butterfly’s form, with curved loops forming wings, often adorned with floral or vein-like sub-motifs. Drawn daily or for festivals like Pongal, it blends ritual, aesthetics, and mathematical precision.

Mathematical Formulas for Butterfly Kolam

Butterfly kolam, a figurative South Indian floor art, represents a butterfly with a central body and symmetrical wings drawn around a dot grid. Its mathematical structure is rooted in graph theory, symmetry, and parametric curves, as analyzed in ethnomathematical studies. Below are detailed formulas, inspired by research such as Gift Siromoney’s work on kolam as picture languages.

1. Dot Grid Setup (Matrix Representation):
   - Formula: M = { (i, j) | i ∈ [1, n], j ∈ [1, m] }
   - Description: Defines a rectangular or tapering grid of dots (vertices), typically n × m (e.g., 8x8 or 9x2 tapering). Dots are coordinates for line placement. For a butterfly, a common grid is 6x4 or a tapering 9-1-9 (interlaced). This forms the basis for the graph structure (Siromoney, G., & Siromoney, R., 1987, "South Indian Kolam Patterns").

2. Eulerian Path for Continuous Loops:
   - Formula: Graph G = (V, E), where V = {dots}, E = {lines}; requires deg(v) ≡ 0 (mod 2) for all v ∈ V to ensure a closed Eulerian circuit.
   - Description: Ensures a single, continuous, non-intersecting line (kambi) covers all edges exactly once, forming loops around dots. For butterfly kolam, the path starts at the body (e.g., a vertical line) and branches into wing subgraphs, maintaining even-degree vertices (typically 4) (Siromoney, G., 1984, "Array Grammars and Kolam").

3. Bilateral Symmetry Transformation:
   - Formula: Reflection σ_v: (x, y) → (-x, y); Rotation R_180: (x, y) → (-x, -y).
   - Description: Captures the bilateral symmetry of wings across the vertical axis (thorax) and 180° rotational symmetry for balance. The dihedral group D_2 governs these transformations, ensuring left and right wings are mirror images (Ascher, M., 2002, "Mathematics Elsewhere").

4. Parametric Curves for Wing Loops:
   - Formula: x = i + r cos θ, y = j + r sin θ, θ ∈ [kπ/2, (k+1)π/2], k = 0, 1, 2, 3, for dot at (i, j), radius r = dot spacing.
   - Description: Models quarter-circle arcs that loop around each dot, chained to form wing shapes. For example, upper wings loop around dots in a fan-like pattern, with r typically 0.5–1 unit (dot spacing). Multiple loops per wing create layered effects (Robinson, T., 2006, "Kolam: A Mathematical Treasure of South India").

5. Fractal Scaling for Sub-Motifs:
   - Formula: F_n = F_(n-1) + F_(n-2), where F_n is the number of loops or motifs in layer n.
   - Description: Governs self-similar sub-motifs (e.g., floral or vein-like patterns in wings), following a Fibonacci-like sequence. This recursive structure adds complexity, resembling natural spirals in butterfly wings (Siromoney, G., et al., 1989, "Computer Analysis of Kolam Patterns").
Design Principles

- Symmetry: Bilateral reflection across the central axis; often 180° rotational symmetry for balance.
- Continuous Lines: Single, non-intersecting, closed loops encircle dots without retracing, symbolizing infinity.
- Dot Grid Foundation: Dots form a matrix (parallel or tapering); lines hug each dot once.
- No Overlaps: Lines avoid crossing to maintain clarity and ritual purity.
- Modular Construction: Build from the center (body) outward (wings) using quarter-circle or quarter-square arcs.
- Cultural Context: Drawn on swept, wet ground for adhesion; size scales with occasion (small daily, large for festivals).
- Aesthetic Flexibility: Freehand elements (e.g., antennae) and optional colors for festivals enhance visual appeal.
- Scalable Complexity: Simple designs use fewer dots; intricate ones layer fractal motifs for depth.


Butterfly Kolam: Step-by-Step Procedure
- Prepare surface: Sweep and lightly wet ground for rice flour adhesion.
- Set dot grid: Place 6x4 rectangular grid (6 rows, 4 columns, 1-inch spacing).
- Draw central body: Connect dots vertically in column 2 (rows 1-6) for thorax; add freehand antennae at top.
- Form upper wings: Loop continuously around dots in rows 1-3, columns 1-2 (left) and 3-4 (right), creating fan-like shapes.
- Form lower wings: Loop around dots in rows 4-6, columns 1-2 (left) and 3-4 (right), mirroring upper wings.
- Ensure continuity: Draw a single, non-intersecting line encircling all dots once.
- Add colors (optional): Fill wings with colored powders (e.g., red, yellow) for festivals.
- Finalize: Check symmetry, smooth curves, avoid overlaps.
- Resource: YouTube “Butterfly Kolam Tutorial” (e.g., Kolam Designs by Sudha, https://www.youtube.com/results?search_query=butterfly+kolam); www.ikolam.com for patterns.       
"""
    },
    "kambi": {
        "title": "Kambi Kolam (Line/Wire Kolam)",
        "image_url": "https://i.ytimg.com/vi/bQx-4b71dnM/maxresdefault.jpg",
        "description": """
Description of Kambi Kolam

Kambi kolam, also known as sikku kolam, is a traditional South Indian floor art form drawn with white rice flour at home entrances, symbolizing prosperity and protection. The term "kambi" (Tamil for "wire" or "thread") or "sikku" (Telugu for "twisted") refers to its intricate, continuous, non-intersecting lines that weave around a grid of dots (pullis) in a single, unbroken loop. Unlike the figurative butterfly kolam, kambi kolam is abstract, emphasizing complex, rope-like patterns that resemble knots or braids. Drawn daily or during festivals like Pongal, it showcases mathematical precision and aesthetic harmony, often with symmetrical or repeating motifs.

Related Mathematical Formulas with Descriptions

Mathematical Formulas for Kambi Kolam

Kambi or sikku kolam is an abstract South Indian floor art featuring twisted, rope-like patterns woven around a dot grid in a single, continuous loop. Its mathematical foundation lies in graph theory, knot theory, and symmetry, as explored in computational studies of kolam. Below are detailed formulas, drawing from research by Gift Siromoney and others.

1. Dot Grid Setup (Matrix Representation):
   - Formula: M = { (i, j) | i ∈ [1, n], j ∈ [1, m] }
   - Description: Defines a square or rectangular grid of dots (vertices), typically n × m (e.g., 5x5 or 7x7). Dots are anchor points for weaving lines, forming the graph’s vertices (Siromoney, G., & Siromoney, R., 1987, "South Indian Kolam Patterns").

2. Eulerian Path for Continuous Line:
   - Formula: Graph G = (V, E), where V = {dots}, E = {lines}; requires deg(v) ≡ 0 (mod 2) for all v ∈ V for a closed Eulerian circuit.
   - Description: Ensures a single, non-intersecting line weaves around all dots, covering edges exactly once. The path creates a twisted, braided effect, with each dot typically having degree 4 (Siromoney, G., 1984, "Array Grammars and Kolam").

3. Symmetry Transformations (Dihedral Group):
   - Formula: Dihedral group D_4: Reflections σ_v: (x, y) → (-x, y), σ_h: (x, y) → (x, -y); Rotation R_90: (x, y) → (-y, x).
   - Description: Captures four-fold rotational symmetry (90°, 180°, 270°) and reflections across axes, ensuring balanced, repeating patterns. This symmetry is central to sikku kolam’s aesthetic (Ascher, M., 2002, "Mathematics Elsewhere").

4. Parametric Curves for Twisted Loops:
   - Formula: x = i + r cos θ, y = j + r sin θ, θ ∈ [0, 2π], for dot at (i, j), radius r = dot spacing.
   - Description: Models quarter-circle or semi-circle arcs looping around dots, chained to form rope-like patterns. The line alternates directions to create a twisted effect, with r typically 0.5–1 unit (Robinson, T., 2006, "Kolam: A Mathematical Treasure of South India").

5. Knot Theory Connection:
   - Formula: Crossing number c(K) = 0 (unknot) or c(K) ≥ 3 (e.g., trefoil knot).
   - Description: Represents sikku kolam as knot projections. Simple designs are unknots (no crossings), while complex ones mimic knots like the trefoil, with lines weaving to avoid intersections (Siromoney, G., et al., 1989, "Computer Analysis of Kolam Patterns").



Design Principles

- Symmetry: Exhibits four-fold rotational symmetry (90° increments) and reflectional symmetry across axes for visual balance.
- Continuous Line: Single, non-intersecting, closed loop weaves around dots without retracing, symbolizing unity and infinity.
- Dot Grid Foundation: Dots form a square or rectangular grid (e.g., 5x5); lines encircle each dot exactly once.
- No Overlaps: Lines avoid crossing to maintain clarity and ritual purity, creating a "twisted" appearance.
- Modular Weaving: Patterns build from center outward, using quarter-circle arcs or diagonal weaves to form knot-like motifs.
- Cultural Context: Drawn on swept, wet ground for adhesion; size scales with occasion (small for daily, large for festivals like Sankranti).
- Aesthetic Simplicity: Monochromatic (white rice flour) for daily use; optional colors (e.g., red, yellow) for festivals.
- Scalable Complexity: Simple designs use smaller grids (e.g., 3x3); intricate ones expand to larger grids (e.g., 9x9) with layered weaves.



Kambi Kolam: Step-by-Step Procedure
- Prepare surface: Sweep and lightly wet ground for adhesion.
- Set dot grid: Place 5x5 square grid (5 rows, 5 columns, even spacing).
- Start at center: Begin at dot (3,3), draw a small loop around it.
- Weave pattern: Draw continuous line, looping around each dot (e.g., (3,3) to (3,4), loop, to (2,4)), alternating directions for twisted effect.
- Maintain continuity: Ensure single, non-intersecting path covers all dots, returning to start.
- Check symmetry: Adjust for four-fold rotational symmetry (90° turns).
- Add colors (optional): Fill sections with colors (e.g., blue, red) for festivals.
- Finalize: Smooth lines, ensure no overlaps.
- Resource: YouTube “Sikku Kolam Tutorial” (e.g., Rangoli Designs by Anitha, https://www.youtube.com/results?search_query=sikku+kolam); www.rangolidesign.net for patterns.        
"""
    }
}

def get_description(kolam_type):
    """Safely retrieves the description data for a given kolam type."""
    return KOLAM_DESCRIPTIONS.get(kolam_type, None)