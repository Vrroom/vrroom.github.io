from PIL import Image

files = ["videoframe_1234.png", "videoframe_1617.png", "videoframe_2170.png"]

# Define cut boundaries
left_cut_x = 380
left_cut_top_y = 128
left_cut_bottom_y = 132

for filename in files:
    image = Image.open(filename)

    # Crop the left-top region
    left_top = image.crop((0, 0, left_cut_x, left_cut_top_y))

    # Crop the left-bottom region
    left_bottom = image.crop((0, left_cut_bottom_y, left_cut_x, image.height))

    # Crop the right region
    right_region = image.crop((left_cut_x + 10, 0, image.width, image.height))

    # Save them (or process further)
    left_top.save(f"{filename}_left_top.png")
    left_bottom.save(f"{filename}_left_bottom.png")
    right_region.save(f"{filename}_right_region.png")

