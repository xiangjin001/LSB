import random
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

def hide(image, message, seed):
    random.seed(seed)
    width, height = image.size
    #message_length = len(message)
    
    #message_bits = ''.join(format(ord(i), '08b') for i in message)

    message_length_bits = format(len(message), '016b')
    #message = str(message_length) + ':' + message
    message_bits = message_length_bits + ''.join(format(ord(i), '08b') for i in message)

    pixels = image.load()
    index = 0
    for i in range(width):
        for j in range(height):
            if index < len(message_bits):
                r, g, b, a = pixels[i,j]
                if message_bits[index] == '0':
                    b = b & ~1
                else:
                    b = b | 1
                pixels[i,j] = (r,g,b,a)
                index += 1
            else:
                break

def getmessage(image, seed):
    random.seed(seed)
    width,height = image.size
    pixels = image.load()
    message_bits = ''
    for i in range(width):
        for j in range(height):
            r,g,b,a = pixels[i,j]
            message_bits += str(b & 1)
    message_length_bits = ''
    index = 0
    while True:
        char_bits = message_bits[index:index+8]
        char = chr(int(char_bits,2))
        if char == ':':
            break
        message_length_bits += char_bits
        index += 8
    message_length_bits = message_bits[:16]
    message_length = int(message_length_bits, 2)
    message_bits = message_bits[16:16+message_length*8]
    message = ''
    for i in range(0,len(message_bits),8):
        message += chr(int(message_bits[i:i+8],2))
    return message

    


def select_image():
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png')])
    if file_path:
        image_entry.delete(0, tk.END)
        image_entry.insert(0, file_path)

def hide_message():
    image_path = image_entry.get()
    message = message_entry.get()
    seed = int(seed_entry.get())
    image = Image.open(image_path)
    hide(image, message, seed)
    image.save(image_path)
    result_label.config(text='信息已隐藏')

def extract_message():
    image_path = image_entry.get()
    seed = int(seed_entry.get())
    image = Image.open(image_path)
    message = getmessage(image, seed)
    extracted_message_text.delete('1.0', tk.END)
    extracted_message_text.insert(tk.END, message)

root = tk.Tk()
root.title('信息隐藏')

image_label = tk.Label(root, text='图片路径:')
image_label.grid(row=0, column=0)#控件放在第0行第0列

image_entry = tk.Entry(root,width=60)
image_entry.grid(row=0, column=1)

select_button = tk.Button(root, text='选择图片', command=select_image)
select_button.grid(row=0, column=2)



message_label = tk.Label(root, text='信息:')
message_label.grid(row=1, column=0)

message_entry = tk.Entry(root,width=60)
message_entry.grid(row=1, column=1)

seed_label = tk.Label(root, text='种子值:')
seed_label.grid(row=2, column=0)

seed_entry = tk.Entry(root,width=60)
seed_entry.grid(row=2, column=1)

hide_button = tk.Button(root, text='隐藏信息', command=hide_message)
hide_button.grid(row=3, column=0)

extract_button = tk.Button(root, text='提取信息', command=extract_message)

extract_button.grid(row=3, column=1)

result_label = tk.Label(root)
result_label.grid(row=4, columnspan=3)

extracted_message_label = tk.Label(root, text='提取到的信息:')
extracted_message_label.grid(row=5, column=0)

extracted_message_text = tk.Text(root, height=10, width=60)
extracted_message_text.grid(row=5, column=1, columnspan=2)

root.mainloop()

root = tk.Tk()
root.title('显示图片')

image = Image.open('image.png')
photo = ImageTk.PhotoImage(image)

image_label = tk.Label(root, image=photo)
image_label.pack()

root.mainloop()