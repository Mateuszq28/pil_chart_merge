from PIL import Image

start_idx = 0
num = 2
y_margin = 5
background = 255
marin_background = 255

img_names = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png"]
img_names = ["out_col_1.png", "out_col_2.png", "out_col_3.png", "out_col_4.png", "out_col_5.png", "out_col_6.png"]
img_names = img_names[start_idx:start_idx+num]
imgs = []
sizes = []
for name in img_names:
    img_load = Image.open(name)
    imgs.append(img_load)
    sizes.append(img_load.size)


max_x = max([val[0] for val in sizes])
sum_y = sum([val[1] for val in sizes])
margin_num = (num-1)
sum_margin = y_margin * margin_num
out_y = sum_y+sum_margin
out_x = max_x


new_image = Image.new('RGB',(out_x, out_y), (background,background,background))
marign_img = Image.new('RGB',(out_x, y_margin), (marin_background,marin_background,marin_background))


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
    y_paste += p_img.size[1]


new_image.save("out_row.png","PNG")
new_image.show()