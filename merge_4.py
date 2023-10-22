from PIL import Image
import numpy as np

def main():
    start_num = 1
    num = 4
    cols = 2
    glob_margin = 5
    x_margin = glob_margin
    y_margin = glob_margin
    background = 255
    marin_background = 255

    save_unify_size = True


    img_names = [str(i)+".png" for i in range(start_num,start_num+num)]
    img_names = [str(4)+".png" for i in range(start_num,start_num+num)]
    imgs = [Image.open(name) for name in img_names]
    imgs_cut = [cut_img(im) for im in imgs]
    imgs = unify_size(imgs_cut, background)

    if save_unify_size:
        for i in range(len(imgs_cut)):
            name = "cut_" + img_names[i]
            imgs_cut[i].save(name,"PNG")
            name = "unify_" + img_names[i]
            imgs[i].save(name,"PNG")
    
    l = len(imgs)
    idx_list = list(range(l))
    full_rows = l // cols
    idx_mod = l % cols
    idx_2d = [idx_list[i:(i+cols)] for i in range(0,full_rows*cols,cols)]
    if idx_mod != 0:
        idx_2d += [idx_list[l-idx_mod:l]]

    print(idx_2d)
    rows2merge = []
    for row_2d in idx_2d:
        print(row_2d)
        imgs2merge = [imgs[i] for i in row_2d]
        row_img = merge_col(imgs2merge, margin=x_margin, bcg=background, bcg_margin=marin_background)
        rows2merge.append(row_img)
    merged_img = merge_row(rows2merge, margin=y_margin, bcg=background, bcg_margin=marin_background)
    merged_img.save("merged_image.png","PNG")

def cut_img(img):
    yadd = 600
    s = img.size
    x = s[0]
    y = s[1]
    x_start = find_line(img, start=[0,y//2], end=[x-1,y//2], line_orientation="vertical")[0]
    x_end = find_line(img, start=[x-1,y//2], end=[0,y//2], line_orientation="vertical")[0]
    y_start = find_line(img, start=[(x-yadd)//2+yadd,0], end=[(x-yadd)//2+yadd,y-1], line_orientation="horizontal")[1]
    y_end = find_line(img, start=[(x-yadd)//2+yadd,y-1], end=[(x-yadd)//2+yadd,0], line_orientation="horizontal")[1]
    ox_start = 115
    ox_end = 131
    oy_start = 60
    oy_end = 91
    img_arr = np.array(img)
    img_arr = img_arr[y_start-oy_start : y_end+oy_end, x_start-ox_start : x_end+ox_end]
    print(img_arr.shape)
    print(y_start)
    print(y_end)
    img = Image.fromarray(img_arr)
    return img


def find_line(img, start, end, line_orientation):
    img_arr = np.array(img)
    check_val = np.array([0,0,0,255])
    if line_orientation == "vertical":
        go_ax = 0
    else:
        go_ax = 1
    s = start[go_ax]
    e = end[go_ax]
    if s <= e:
        go_i = 1
    else:
        go_i = -1
    for go_pos in range(s, e, go_i):
        pos = start.copy()
        pos[go_ax] = go_pos
        counter = 0
        for delta in range(-20, 21, 1):
            x = pos[0]
            y = pos[1]
            if line_orientation == "vertical":
                y = pos[1] + delta
            else:
                x = pos[0] + delta
            # print("(x,y)", x, y)
            # print(img_arr[y,x])
            if not np.array_equal(img_arr[y,x], check_val):
                counter = 0
                break
            else:
                # print(img_arr[y,x])
                counter += 1
                if counter >= 41:
                    return [x,y]
    return None

def unify_size(imgs, bcg):
    max_x = max([im.size[0] for im in imgs])
    max_y = max([im.size[1] for im in imgs])
    out_imgs = []
    print(len(imgs))
    for im in imgs:
        print(len(imgs))
        if im.size[0] < max_x or im.size[1] < max_y:
            new_img = Image.new('RGB',(max_x, max_y), (bcg,bcg,bcg))
            paste_x = (max_x-im.size[0])//2
            paste_y = (max_y-im.size[1])//2
            new_img.paste(im, (paste_x, paste_y))
            out_imgs.append(new_img)
        else:
            out_imgs.append(im)
    return out_imgs

def merge_col(imgs, margin, bcg, bcg_margin):
    max_y = max([im.size[1] for im in imgs])
    sum_x = sum([im.size[0] for im in imgs])
    num = len(imgs)
    margin_num = (num-1)
    sum_margin = margin * margin_num
    out_x = sum_x+sum_margin
    out_y = max_y

    new_image = Image.new('RGB',(out_x, out_y), (bcg,bcg,bcg))
    marign_img = Image.new('RGB',(margin, out_y), (bcg_margin,bcg_margin,bcg_margin))

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

    return new_image


def merge_row(imgs, margin, bcg, bcg_margin):
    max_x = max([im.size[0] for im in imgs])
    sum_y = sum([im.size[1] for im in imgs])
    num = len(imgs)
    margin_num = (num-1)
    sum_margin = margin * margin_num
    out_y = sum_y+sum_margin
    out_x = max_x

    new_image = Image.new('RGB',(out_x, out_y), (bcg,bcg,bcg))
    marign_img = Image.new('RGB',(out_x, margin), (bcg_margin,bcg_margin,bcg_margin))

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

    return new_image


        







main()