from PIL import Image, ImageDraw
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

# Gradient colors
hex_colors = ["#FBC5DC", "#E7CCFF", "#CFD3FF", "#A1F0F7", "#A7F4D0"]
rgb_colors = [hex_to_rgb(c) for c in hex_colors]
unfilled_color = hex_to_rgb("#EEF6F9")

# Bar settings
bar_width = 400
bar_height = 100
radius = bar_height // 2
padding = 100

# Load pointer image
pointer_path = "/storage/emulated/0/za.png"
pointer_img = Image.open(pointer_path).convert("RGBA")
pointer_w, pointer_h = pointer_img.size

# Generate a single progress bar image
def generate_bar(progress_percent):
    canvas_width = bar_width + padding * 2
    canvas_height = max(bar_height, pointer_h + 20)
    canvas = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(canvas)

    bar_y = (canvas_height - bar_height) // 2
    bar_x_start = padding
    draw.rounded_rectangle([(bar_x_start, bar_y),
                            (bar_x_start + bar_width, bar_y + bar_height)],
                           radius=radius, fill=unfilled_color)

    progress_px = int((progress_percent / 100) * bar_width)
    gradient = Image.new("RGBA", (progress_px, bar_height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(gradient)

    segments = len(rgb_colors) - 1
    segment_width = bar_width // segments

    for i in range(segments):
        start = rgb_colors[i]
        end = rgb_colors[i + 1]
        for x in range(segment_width):
            ratio = x / segment_width
            r = int(start[0] * (1 - ratio) + end[0] * ratio)
            g = int(start[1] * (1 - ratio) + end[1] * ratio)
            b = int(start[2] * (1 - ratio) + end[2] * ratio)
            actual_x = i * segment_width + x
            if actual_x < progress_px:
                gdraw.line([(actual_x, 0), (actual_x, bar_height)], fill=(r, g, b))

    mask = Image.new("L", (progress_px, bar_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (progress_px, bar_height)], radius=radius, fill=255)
    canvas.paste(gradient, (bar_x_start, bar_y), mask)

    pointer_x = bar_x_start + progress_px - pointer_w // 2
    pointer_y = (canvas_height - pointer_h) // 2
    canvas.paste(pointer_img, (pointer_x, pointer_y), pointer_img)

    return canvas

# Resize helper
def shrink(img, ratio=0.65):
    return img.resize((int(img.width * ratio), int(img.height * ratio)), resample=Image.LANCZOS)

# === Main function to generate progress image ===
def generate_progress_image(max_bars=2, percents=[67, 100], user_id=None):
    bg_path = "/storage/emulated/0/templatepack.png"
    bg = Image.open(bg_path).convert("RGBA")

    if max_bars > 2 or max_bars < 1 or len(percents) != max_bars:
        print("❌ Error: max_bars must be 1 or 2, and percents must match.")
        return

    # Fixed bar positions
    positions = [(740, 300), (1100, 835)]
    for i in range(max_bars):
        bar_img = shrink(generate_bar(percents[i]))
        cx, cy = positions[i]
        bar_x = cx - bar_img.width // 2
        bar_y = cy - bar_img.height // 2
        bg.paste(bar_img, (bar_x, bar_y), bar_img)
        print(f"📍 Bar {i+1} ({percents[i]}%) pasted at center: ({cx}, {cy})")

    # Save
    output_path =f"packpil1_{user_id}.png"
    bg.save(output_path)
    
generate_progress_image(max_bars=2, percents=[26, 89]) 
