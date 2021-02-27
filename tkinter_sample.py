import sys
import tkinter
from PIL import Image, ImageTk
import threading
import time
 
def show_image():
    # 外から触れるようにグローバル変数で定義
    global item, canvas
 
    root = tkinter.Tk()
    root.title('test')
    root.geometry("400x300")
    img = Image.open('img1.png')
    img = ImageTk.PhotoImage(img)
    canvas = tkinter.Canvas(bg = "black", width=400, height=300)
    canvas.place(x=100, y=50)
    item = canvas.create_image(30, 30, image=img, anchor=tkinter.NW)
    root.mainloop()
 
# スレッドを立ててtkinterの画像表示を開始する
thread1 = threading.Thread(target=show_image)
thread1.start()
 
# 切り替えたい画像を定義
img2 = Image.open('img2.png')
img2 = ImageTk.PhotoImage(img2)
time.sleep(3) #3秒毎に切り替え
 
# itemを差し替え
canvas.itemconfig(item,image=img2)
time.sleep(3)
 
# itemをもとに戻す
img = Image.open('img1.png')
img = ImageTk.PhotoImage(img)
canvas.itemconfig(item,image=img)