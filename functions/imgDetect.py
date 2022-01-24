import pixellib
from pixellib.instance import instance_segmentation
from googletrans import Translator
from collections import Counter

def translate(text='0'):
    return(Translator().translate(text, src='en', dest='ru').text)

def data():
    objects_en = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 
    'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 
    'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 
    'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 
    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 
    'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 
    'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 
    'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 
    'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 
    'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 
    'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 
    'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 
    'scissors', 'teddy bear', 'hair drier', 'toothbrush']

    objects_ru = ['задний фон', 'человек', 'велосипед', 'машина', 
    'мотоцикл', 'самолет', 'автобус', 'тренироваться', 'грузовик', 
    'лодка', 'светофор', 'пожарный кран', 'знак СТОП', 'счетчик на стоянке', 
    'скамейка', 'птица', 'Кот', 'собака', 'лошадь', 'овца', 'корова', 'слон', 
    'нести', 'зебра', 'жирафа', 'рюкзак', 'зонтик', 'сумочка', 'галстук', 
    'чемодан', 'фрисби', 'лыжи', 'сноуборд', 'спортивный мяч', 'летающий змей', 
    'бейсбольная бита', 'бейсбольная перчатка', 'скейтборд', 'доска для серфинга', 
    'теннисная ракетка', 'бутылка', 'бокал для вина', 'чашка', 'вилка', 'нож', 
    'ложка', 'чаша', 'банан', 'яблоко', 'сэндвич', 'апельсин', 'брокколи', 'морковь', 
    'хот-дог', 'пицца', 'пончик', 'кекс', 'стул', 'диван', 'растение в горшке', 'кровать', 
    'обеденный стол', 'туалет', 'ТВ', 'ноутбук', 'мышь', 'дистанционный пульт', 'клавиатура', 
    'мобильный телефон', 'микроволновая печь', 'духовой шкаф', 'тостер', 'раковина', 
    'холодильник', 'книга', 'Часы', 'ваза', 'ножницы', 'плюшевый мишка', 'фен', 'зубная щетка']
    return(objects_en, objects_ru)

def img2txt():
    segment_image = instance_segmentation(infer_speed = 'rapid')
    segment_image.load_model('functions/mask_rcnn_coco.h5') 
    res = segment_image.segmentImage('functions/processing/img.png', 
        # output_image_name="new_objects.jpg",
        # show_bboxes=True,
        # extract_segmented_objects=True,
        # text_size=4, 
        # text_thickness=10,
        # box_thickness=6
        )
    objects_en, objects_ru = data()
    out = []
    for i in Counter(res[0]['class_ids'].tolist()).most_common(3):
        out.append(objects_ru[i[0]])
    out.sort()
    return((' ').join(out))

# print(img2txt())