import math
from PIL import Image

class WallpaperGenerator:
    def __init__(self, image_path, hex_size=10, mode="hex"):
        """
        image_path: path to input PNG/JPG or file-like object
        hex_size: size of hexagons
        mode: 'hex' or 'triangle'
        """
        self.img = Image.open(image_path).convert("RGB")
        self.hex_size = hex_size
        self.mode = mode
        self.svg_lines = []
        self.width, self.height = self.img.size

    # Hexagon geometry (pointy-top)
    def hex_points(self, cx, cy):
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.radians(angle_deg)
            x = cx + self.hex_size * math.cos(angle_rad)
            y = cy + self.hex_size * math.sin(angle_rad)
            points.append((x, y))
        return points

    # Triangle geometry (two triangles per hex cell)
    def triangle_points(self, cx, cy):
        h = math.sqrt(3) * self.hex_size / 2
        tri1 = [(cx, cy-h), (cx-self.hex_size, cy+h), (cx+self.hex_size, cy+h)]
        tri2 = [(cx, cy+h), (cx-self.hex_size, cy-h), (cx+self.hex_size, cy-h)]
        return [tri1, tri2]

    # Average color of pixels inside hex/triangle area
    def average_color(self, cx, cy):
        total_r = total_g = total_b = count = 0
        step = max(1, self.hex_size // 3)
        for x in range(int(cx - self.hex_size), int(cx + self.hex_size), step):
            for y in range(int(cy - self.hex_size), int(cy + self.hex_size), step):
                if 0 <= x < self.width and 0 <= y < self.height:
                    r, g, b = self.img.getpixel((x, y))
                    total_r += r
                    total_g += g
                    total_b += b
                    count += 1
        if count == 0:
            return (0, 0, 0)
        return (total_r // count, total_g // count, total_b // count)

    # Generate SVG content
    def generate_svg(self):
        self.svg_lines = []
        hex_height = math.sqrt(3) * self.hex_size
        vert_spacing = hex_height * 0.75
        horiz_spacing = 1.5 * self.hex_size

        y = 0
        row = 0
        while y < self.height + hex_height:
            x_offset = self.hex_size * 0.75 if row % 2 else 0
            x = 0
            while x < self.width + self.hex_size:
                cx = x + x_offset
                cy = y
                color = self.average_color(cx, cy)

                if self.mode == "hex":
                    pts = self.hex_points(cx, cy)
                    pts_str = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
                    self.svg_lines.append(f'<polygon points="{pts_str}" fill="rgb{color}" stroke="none"/>\n')
                elif self.mode == "triangle":
                    for tri in self.triangle_points(cx, cy):
                        pts_str = " ".join(f"{px:.1f},{py:.1f}" for px, py in tri)
                        self.svg_lines.append(f'<polygon points="{pts_str}" fill="rgb{color}" stroke="none"/>\n')

                x += horiz_spacing
            y += vert_spacing
            row += 1

        svg_header = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" preserveAspectRatio="xMidYMid slice">\n'
        svg_footer = '</svg>\n'
        return svg_header + "".join(self.svg_lines) + svg_footer

    # Save SVG to file
    def save(self, filename):
        svg_content = self.generate_svg()
        with open(filename, "w") as f:
            f.write(svg_content)
        print(f"✅ SVG saved as {filename}")
