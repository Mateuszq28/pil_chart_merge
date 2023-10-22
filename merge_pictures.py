from PIL import Image

image1 = Image.open('parabola_PDF.png')
image2 = Image.open('parabola_sampling.png')
image3 = Image.open('parabola_density_1.png')
image4 = Image.open('parabola_density_2.png')

image_size = image1.size
new_image = Image.new('RGB',(2*image_size[0], 2*image_size[1]), (250,250,250))
new_image.paste(image1,(0,0))
new_image.paste(image2,(image_size[0],0))
new_image.paste(image3,(0,image_size[1]))
new_image.paste(image4,(image_size[0],image_size[1]))
new_image.save("parabola4charts_scale.png","PNG")
new_image.show()