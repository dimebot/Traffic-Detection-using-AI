from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont
import os     
client = vision.ImageAnnotatorClient.from_service_account_file('api-key.json')

while True:                            
    image_path = input("Enter the name of the image file (with extension): ")

    if not os.path.exists(image_path):
        print(f"The file '{image_path}' does not exist.")
        exit_option = input("Press 'q' to quit or any other key to try again: ")
        if exit_option.lower() == 'q':
            exit()
        else:
            continue

    with open(image_path, "rb") as image_file:
        content = image_file.read()



    image = vision.Image(content=content)
 
    response = client.object_localization(image=image)

    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    labels = ["Car", "Truck", "Bus", "Cat", "Dog", "Rat", "Mouse", "Bicycle", "Person", "Traffic light", "Stop sign", "Building", "Tree"]

    output_image_name = input("Enter the name of the output image (e.g., output_traffic.jpg): ")
    output_image_path = input("Enter the path where you want to save the output image (or type 'none' to save in the same directory): ")

    if output_image_path.lower() == 'none':
        output_image_path = os.path.dirname(image_path)
    else:
        if not os.path.exists(output_image_path):
            os.makedirs(output_image_path, exist_ok=True)

    output_image_path = os.path.join(output_image_path, output_image_name)

    for obj in response.localized_object_annotations:
        if obj.name in labels:
            if obj.name in ["Car", "Truck", "Bus", "Bicycle"]:
                color = "green"
            elif obj.name in ["Cat", "Dog", "Rat", "Mouse", "Person"]:
                color = "red"
            else:
                color = "blue"

        vertices = [(vertex.x * img.width, vertex.y * img.height) for vertex in obj.bounding_poly.normalized_vertices]
        draw.polygon(vertices, outline=color, width=6)

        x, y = vertices[0] 
        custom_font_path = "C:/Windows/Fonts/ARLRDBD.ttf" 
        custom_font = ImageFont.truetype(custom_font_path, size=25)
        label = obj.name
        if label in labels:
            draw.text((x, y), label, font=custom_font, fill=color)

    img.save(output_image_path)

    output_img = Image.open(output_image_path)
    output_img.show()
    exit()
