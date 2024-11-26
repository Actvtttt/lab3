from PIL import Image, ImageEnhance
import math

#открываем изображения
img1 = Image.open("image1.jpg").convert("RGB")
img2 = Image.open("image2.jpg").convert("RGB")

#функция для изменения насыщенности
def modify_saturation(img, amp, freq, phase):
    w, h = img.size
    pix = img.load()
    
    #преобразование RGB в HSV
    def rgb_to_hsv(r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx, mn = max(r, g, b), min(r, g, b)
        diff = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / diff) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / diff) + 240) % 360
        s = 0 if mx == 0 else (diff / mx)
        v = mx
        return h, s, v
    
    #преобразование HSV в RGB
    def hsv_to_rgb(h, s, v):
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        elif 300 <= h < 360:
            r, g, b = c, 0, x
        r, g, b = (r + m) * 255, (g + m) * 255, (b + m) * 255
        return int(r), int(g), int(b)

    #изменяем насыщенность
    for y in range(h):
        for x in range(w):
            r, g, b = pix[x, y]
            h, s, v = rgb_to_hsv(r, g, b)
            
            #синусоидальное изменение
            sin_wave = amp * math.sin(2 * math.pi * freq * x + phase)
            s = max(0, min(1, s + sin_wave / 255.0))
            
            #возвращаем RGB
            pix[x, y] = hsv_to_rgb(h, s, v)

    return img

#применяем изменения
amp = 50
freq = 0.1
phase = 0

img1_mod = modify_saturation(img1, amp, freq, phase)
img2_mod = modify_saturation(img2, amp, freq, phase)

#объединяем изображения
alpha = 0.5
img_combined = Image.blend(img1_mod, img2_mod, alpha)

#сохраняем результаты
img1_mod.save("img1_mod.jpg")
img2_mod.save("img2_mod.jpg")
img_combined.save("img_combined.jpg")
