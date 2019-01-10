from PIL import Image
from tkinter import Tk, Label, Button, Entry, END
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import threading
import os


app = Tk()
app.title('一键做画册')
app.geometry('1024x768')


l1 = Label(app, text='选择照片目录：')
l1.place(x=10, y=10)
e1 = Entry(app, width=50)
e1.place(x=100, y=10)
b1 = Button(app, text='点击选择', command=lambda: thread_it(chose_dir))
b1.place(x=470, y=10)
b2 = Button(app, text='生成画册', fg='red', command=lambda: thread_it(main))
b2.place(x=10, y=275)
t1 = ScrolledText(app, width=60, height=50, bg='#F0F0F0')
t1.place(x=570, y=10)

# 配置界面
l2 = Label(app, text='设置画册尺寸（像素）')
l2.place(x=10, y=200)
l3 = Label(app, text='宽度：')
l3.place(x=200, y=200)
e2 = Entry(app, width=10)
e2.place(x=250, y=200)
l4 = Label(app, text='高度：')
l4.place(x=350, y=200)
e3 = Entry(app, width=10)
e3.place(x=400, y=200)
b3 = Button(app, text='预设1:33X28竖版', command=lambda: thread_it(yushe1))
b3.place(x=10, y=150)
l5 = Label(app, text='设置留白边距（%百分比）')
l5.place(x=10, y=225)
l6 = Label(app, text='左右：')
l6.place(x=200, y=225)
e4 = Entry(app, width=10)
e4.place(x=250, y=225)
l7 = Label(app, text='上下：')
l7.place(x=350, y=225)
e5 = Entry(app, width=10)
e5.place(x=400, y=225)


def yushe1():
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e2.insert(END, 6685)
    e3.insert(END, 3969)
    e4.insert(END, 8)
    e5.insert(END, 8)


def resize_img(img_file_name, file_path):
    width = int(e2.get())
    height = int(e3.get())
    pad_w = int(e4.get()) * 0.01
    pad_h = int(e5.get()) * 0.01
    img_path = os.path.join(file_path, img_file_name)
    im = Image.open(img_path)
    w = im.size[0]
    h = im.size[1]
    if w > h:
        cheng = 0.5 - pad_w
        w1 = int(width*cheng)
        rate = w1/w
        h1 = int(h*rate)
    else:
        cheng = 1 - pad_h*2
        h1 = int(height * cheng)
        rate = h1 / h
        w1 = int(w * rate)
    small_name = '%s_small.jpg' % img_file_name.split('.')[0]
    save_path = os.path.join(file_path, 'small', small_name)
    if '封面' in img_file_name:
        w1 = int(w1*0.7)
        h1 = int(h1*0.7)
    im.resize((w1, h1), Image.ANTIALIAS).save(save_path, quality=100)
    t1.insert(END, '【%s】缩放成功\n' % img_file_name)


def join_img(file_path, left_img, right_img, page):
    im0 = Image.open(os.path.join(file_path, 'bg.jpg'))
    w0 = im0.size[0]
    h0 = im0.size[1]
    if left_img:
        im1 = Image.open(os.path.join(file_path, 'small', left_img))
        w1 = im1.size[0]
        h1 = im1.size[1]
        box1 = [int(0.25 * w0 - 0.5 * w1), int(0.5 * h0 - 0.5 * h1)]
        im0.paste(im1, box1)
    if right_img:
        im2 = Image.open(os.path.join(file_path, 'small', right_img))
        w2 = im2.size[0]
        h2 = im2.size[1]
        box2 = [int(0.75 * w0 - 0.5 * w2), int(0.5 * h0 - 0.5 * h2)]
        im0.paste(im2, box2)
    im0.save(os.path.join(file_path, '画册', page), quality=100)


def main():
    e_list = [e2, e3, e4, e5]
    for e in e_list:
        try:
            int(e.get())
        except:
            messagebox.showinfo(message='请先配置画册参数。参数只能输入整数，不要带单位。')
            return
    width = int(e2.get())
    height = int(e3.get())
    t1.delete(0.0, END)
    file_path = e1.get()
    if file_path == '':
        messagebox.showinfo(message='请先选择照片目录')
        return
    image = Image.new('RGB', (width, height), (255, 255, 255))
    image.save(os.path.join(file_path, 'bg.jpg'), 'jpeg')
    t1.insert(END, '创建白底背景图成功\n')
    small_path = os.path.join(file_path, 'small')
    page_path = os.path.join(file_path, '画册')
    if not os.path.exists(small_path):
        os.mkdir(small_path)
    if not os.path.exists(page_path):
        os.mkdir(page_path)
    imgs = os.listdir(file_path)
    imgs.remove('bg.jpg')
    for img in imgs:
        if '.jpg' in img or '.JPG' in img:
            resize_img(img, file_path)

    imgs = os.listdir(small_path)
    # 输出封面，然后从列表移除
    for img in imgs:
        if '封面' in img:
            join_img(file_path, left_img=None, right_img=img, page='封面.jpg')
            t1.insert(END, '封面.jpg输出成功\n')
            imgs.remove(img)

    n = 0
    for i in range(0, len(imgs), 2):
        n = n + 1
        page = imgs[i:i+2]
        save_img = '%s.jpg' % n
        if len(page) == 2:
            join_img(file_path, page[0], page[1], save_img)
        else:
            join_img(file_path, left_img=page[0], right_img=None, page=save_img)
        t1.insert(END, '画册%s输出成功\n' % save_img)
    t1.insert(END, '生成完毕，请检查。')


def chose_dir():
    filename = tkinter.filedialog.askdirectory()
    e1.delete(0, END)
    e1.insert(END, filename)


def thread_it(func):
    # 将函数打包进线程'''
    t = threading.Thread(target=func)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()


app.mainloop()
