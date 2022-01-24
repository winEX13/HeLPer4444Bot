from PIL import Image, ImageDraw, ImageFont #dynamic import
import os
import imageio as iio
import random
import re
import requests
import random
# gif='objects.gif'
# img = Image.open(gif)
# img.save(gif+".png",'png', optimize=True, quality=70)
# print(os.listdir('C:/Users/winEX/Рабочий стол/чат-бот/Main bot/functions'))
# Image.open('C:/Users/winEX/Рабочий стол/чат-бот/Main bot/functions/objects.gif').convert('RGB').save('image.jpg')
# im = iio.get_reader('objects.gif', r)
# print(im)
# im = iio.get_reader('objects.gif', 'r')
# print(im.shape)
# bi = random.choice(iio.read('objects.gif'))
# print(bi)
# File out = new File('functions/objects.jpg')
# iio.write(bi, 'jpg', 'objects.jpg')
# from PIL import Image
# im = Image.open('objects.gif')
# print("Number of frames: "+str(im.n_frames))

with open('site.txt', 'r', encoding='UTF-8') as f:
	article_text = f.read()

jpg_l = []

while isinstance(re.search('(?P<url>https?://[^\s]+.webp)', article_text), re.Match):
    # print (re.search('(?P<url>https?://[^\s]+.jpg)', article_text).group('url'))
    # print (type(re.search('(?P<url>https?://[^\s]+.jpg)', article_text)))
    if isinstance(re.search('(?P<url>https?://[^\s]+.webp)', article_text), re.Match):
    	jpg_l.append(str(re.search('(?P<url>https?://[^\s]+.webp)', article_text).group('url')))
    article_text = article_text.replace((re.search('(?P<url>https?://[^\s]+.webp)', article_text).group('url')), '')
# print(jpg_l)

# for i in range(len(jpg_l)):
# 	p = requests.get(jpg_l[i])
# 	out = open(f'jpgs\{str(i)}.jpg', 'wb')
# 	out.write(p.content)
# 	out.close()
for i in range(1, 47, 1):
	p = requests.get(f'https://tlgrm.ru/_/stickers/a6f/1ae/a6f1ae15-7c57-3212-8269-f1a0231ad8c2/192/{i}.webp')
	out = open(f'jpgs\{str(i)}.jpg', 'wb')
	out.write(p.content)
	out.close()