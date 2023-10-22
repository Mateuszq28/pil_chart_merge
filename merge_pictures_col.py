from PIL import Image

start_idx = 0
num = 2
x_margin = 5
background = 255
marin_background = 255

img_names = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png"]
# img_names = ["out_row_1.png", "out_row_2.png", "out_row_3.png", "out_row_4.png", "out_row_5.png", "out_row_6.png"]
img_names = img_names[start_idx:start_idx+num]
imgs = []
sizes = []
for name in img_names:
    img_load = Image.open(name)
    imgs.append(img_load)
    sizes.append(img_load.size)


max_y = max([val[1] for val in sizes])
sum_x = sum([val[0] for val in sizes])
margin_num = (num-1)
sum_margin = x_margin * margin_num
out_x = sum_x+sum_margin
out_y = max_y


new_image = Image.new('RGB',(out_x, out_y), (background,background,background))
marign_img = Image.new('RGB',(x_margin, out_y), (marin_background,marin_background,marin_background))


paste_imgs = []
margin_counter = 0
for i in range(len(imgs)):
    paste_imgs.append(imgs[i])
    if margin_counter < margin_num:
        paste_imgs.append(marign_img)
        margin_counter += 1


x_paste = 0
y_paste = 0
for p_img in paste_imgs:
    new_image.paste(p_img, (x_paste, y_paste))
    x_paste += p_img.size[0]


new_image.save("out_col.png","PNG")
new_image.show()