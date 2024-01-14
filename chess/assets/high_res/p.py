from PIL import Image

# Load the original image
original_image = Image.open('chess/assets/high_res/original.png')

# Define the size of each sub-image
sub_image_width = 300
sub_image_height = 400

# Define the margin size
margin_size = 50

# Calculate the number of rows and columns
num_rows = original_image.height // sub_image_height
num_cols = original_image.width // sub_image_width

# Iterate through the rows and columns to crop and save each sub-image
for row in range(num_rows):
    for col in range(num_cols):
        left = col * sub_image_width
        upper = row * sub_image_height + margin_size
        right = left + sub_image_width
        lower = upper + sub_image_height - 2 * margin_size

        # Crop the sub-image with a margin at the top and bottom
        sub_image = original_image.crop((left, upper, right, lower))

        # Save the sub-image
        sub_image.save(f'sub_image_{row}_{col}.png')

print('Sub-images with margins saved successfully!')
