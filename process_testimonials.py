#!/usr/bin/env python3
"""Process WhatsApp testimonial screenshots: crop headers/PII, fix brand name, save."""
from PIL import Image, ImageDraw, ImageFont
import os

SRC = "/private/tmp/claude-501/-Users-user-Library-Application-Support-Claude-scratch-workspaces-8b7bec4c-8bf8-4a64-a645-be0b6cb85882-58216e41-72eb-40af-b204-59762b024032-scratch-2026-10-28-bb7792/0815562e-f234-4ab2-abe6-02cf97b1864f/images/"
OUT = "/Users/user/Library/Application Support/Claude/scratch-workspaces/8b7bec4c-8bf8-4a64-a645-be0b6cb85882/58216e41-72eb-40af-b204-59762b024032/scratch-2026-10-28-bb7792/images/testimonials/"
os.makedirs(OUT, exist_ok=True)

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

def fit_text_size(draw, text, max_width, start_size=28, min_size=14):
    size = start_size
    while size > min_size:
        font = ImageFont.truetype(FONT_PATH, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            return font, w
        size -= 1
    return ImageFont.truetype(FONT_PATH, min_size), draw.textbbox((0, 0), text, font=ImageFont.truetype(FONT_PATH, min_size))[2]

def patch_brand_name(im, rect, bg_color, text_color, new_text, text_x_offset=4):
    """Cover rect with bg_color, draw new_text starting near the left edge, vertically centered."""
    x0, y0, x1, y1 = rect
    draw = ImageDraw.Draw(im)
    draw.rectangle(rect, fill=bg_color)
    avail_w = (x1 - x0) - text_x_offset
    font, tw = fit_text_size(draw, new_text, avail_w, start_size=min(30, y1 - y0))
    bbox = draw.textbbox((0, 0), new_text, font=font)
    th = bbox[3] - bbox[1]
    ty = y0 + ((y1 - y0) - th) // 2 - bbox[1]
    draw.text((x0 + text_x_offset, ty), new_text, font=font, fill=text_color)
    return im

def save_final(im, name, target_w=520):
    w, h = im.size
    if w != target_w:
        new_h = int(h * (target_w / w))
        im = im.resize((target_w, new_h), Image.LANCZOS)
    im.convert("RGB").save(os.path.join(OUT, name), "JPEG", quality=88)
    print(f"Saved {name}: {im.size}")

# ---- 1: image 17 -> review-1.jpg (brand fix) ----
im = Image.open(SRC + "17.webp").convert("RGB")
# patch "4kDream" -> "TruWave TV" (verified bounds via pixel grid: word spans x~213-428)
patch_brand_name(im, (210, 233, 515, 276), (0, 76, 67), (255, 255, 255), "TruWave TV family")
crop = im.crop((0, 150, 592, 1050))
save_final(crop, "review-1.jpg")

# ---- 2: image 18 -> review-2.jpg ----
im = Image.open(SRC + "18.png").convert("RGB")
crop = im.crop((0, 75, 507, 455))
save_final(crop, "review-2.jpg")

# ---- 3: image 20 -> review-3.jpg ----
im = Image.open(SRC + "20.png").convert("RGB")
crop = im.crop((0, 68, 507, 700))
save_final(crop, "review-3.jpg")

# ---- 4: image 23 -> review-4.jpg ----
im = Image.open(SRC + "23.png").convert("RGB")
crop = im.crop((0, 65, 507, 495))
save_final(crop, "review-4.jpg")

# ---- 5: image 24 -> review-5.jpg (brand fix, start crop after name-revealing line) ----
im = Image.open(SRC + "24.png").convert("RGB")
# patch "4k Dream" -> "TruWave TV" (verified bounds: word spans x~183-312, line y~278-308)
patch_brand_name(im, (217, 278, 390, 310), (217, 253, 211), (59, 74, 84), "TruWave TV family")
crop = im.crop((0, 277, 507, 700))
save_final(crop, "review-5.jpg")

# ---- 6: image 25 -> review-6.jpg ----
im = Image.open(SRC + "25.png").convert("RGB")
crop = im.crop((0, 55, 435, 715))
save_final(crop, "review-6.jpg")

# ---- 7: image 26 -> review-7.jpg (stitch out inline quote block) ----
im = Image.open(SRC + "26.png").convert("RGB")
top = im.crop((0, 68, 441, 522))      # header removed, up to just after "they are changing..."
bottom = im.crop((0, 615, 441, 755))  # after quote block, "with pleasure" onward
stitched = Image.new("RGB", (441, top.height + bottom.height), (0, 0, 0))
stitched.paste(top, (0, 0))
stitched.paste(bottom, (0, top.height))
save_final(stitched, "review-7.jpg")

print("All done.")
