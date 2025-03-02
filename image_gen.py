from PIL import Image
import random
import numpy as np
from samila import GenerativeImage, Projection
import matplotlib 
from io import BytesIO
matplotlib.use('Agg')

def generateArt(input_image, save_path):
    
    image_blob = input_image.read()
    
    
    image = Image.open(BytesIO(image_blob)).convert('L')

    width, height = image.size

    pixel_values = []

    for i in range(6):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        pixel_value = image.getpixel( (x,y) )
        pixel_values.append(pixel_value)

    pixel_values = [pixel/np.mean(pixel_values) for pixel in pixel_values] 

    print(f"These are the pixel values : {pixel_values}")

    def equation(x,y):
        
        
        return random.uniform(-1,1) * pixel_values[3]*x**2  - pixel_values[5]*np.sin(y**2) + abs(y-x)

    def equation_2(X,Y):
        return pixel_values[0]*X + pixel_values[1]*Y + np.sin(X*Y)


    g = GenerativeImage(equation, equation_2)

    colors = ["cyan", "turquoise", "violet", "yellow", "silver"]
    index = random.randint(0, 4)
    g.generate(seed=int(pixel_values[4]*10000))

    index_for_projection = random.randint(0,1)

    if index_for_projection == 0:

        g.plot(color=colors[index],bgcolor="black", projection=Projection.POLAR, size=(8,8), linewidth=2)
        g.save_image(save_path)

    else:
        g.plot(color=colors[index],bgcolor="black", size=(8,8), linewidth=2)
        g.save_image(save_path)
        