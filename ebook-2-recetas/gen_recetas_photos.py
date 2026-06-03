#!/usr/bin/env python3
"""Regenera las 30 imágenes de receta como FOTOS REALES de comida (no ilustraciones)."""
import os, sys, time, io, urllib.request
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'brand', 'illustrations')))
from gen import post, find_task_id, poll, KEY, UA
from PIL import Image

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')

PHOTO = ("Appetizing professional food photograph of {dish}. Dark moody premium food photography on a "
         "dark slate surface, dramatic side lighting with a subtle neon lime green accent glow in the "
         "background, high contrast, shallow depth of field, fresh and delicious, fitness nutrition "
         "aesthetic, mouth-watering. NO text, no letters, no watermark.")

DISHES = {
 'b1':'avocado toast topped with poached eggs and serrano ham',
 'b2':'a bowl of oatmeal with banana slices, peanut butter and walnuts',
 'b3':'a stack of protein french toast drizzled with syrup',
 'b4':'a stack of banana oat pancakes with syrup',
 'b5':'a breakfast burrito cut in half showing eggs',
 'b6':'a thick smoothie bowl topped with fruit and granola',
 's1':'a tall classic vanilla protein shake in a glass',
 's2':'a chocolate protein shake in a glass',
 's3':'a green vegetable smoothie in a glass',
 's4':'an iced coffee protein shake in a glass',
 's5':'a berry protein smoothie in a glass with fresh berries',
 's6':'a vanilla nut protein shake in a glass with nuts',
 'l1':'a bowl of grilled chicken and white rice with vegetables',
 'l2':'a plate of creamy pasta carbonara',
 'l3':'a beef burrito cut in half',
 'l4':'a bowl of chickpea curry with rice',
 'l5':'a mexican burrito bowl with rice, beans and meat',
 'l6':'a grilled salmon fillet with roasted sweet potato',
 'd1':'a baked salmon fillet with lemon slices and herbs',
 'd2':'a slice of homemade lasagna on a plate',
 'd3':'a plate of chicken curry with rice',
 'd4':'a juicy steak with roasted potatoes',
 'd5':'a homemade burger with fries',
 'd6':'a homemade pizza with melted cheese',
 'n1':'a toast with peanut butter and banana slices',
 'n2':'a bowl of greek yogurt with granola and berries',
 'n3':'a cheese quesadilla cut into triangles',
 'n4':'a bowl of mixed nuts and almonds',
 'n5':'canned tuna with sliced avocado on a plate',
 'n6':'a chia seed pudding in a jar topped with fresh fruit',
}

def save_jpgish(url, out):
    d=urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':UA}), timeout=120).read()
    im=Image.open(io.BytesIO(d)).convert('RGB')
    w,h=im.size; s=min(w,h)  # center-crop a cuadrado para las cards
    im=im.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s))
    im.save(out)  # PNG opaco (mismo nombre que referencia el HTML)

def main():
    submitted=[]
    for iid,desc in DISHES.items():
        try:
            r=post(PHOTO.format(dish=desc)); t=find_task_id(r)
            if t: submitted.append((iid,t)); print('submit',iid,t)
            else: print('NO TASKID',iid)
        except Exception as e: print('FAIL submit',iid,e)
        time.sleep(0.4)
    ok=fail=0
    for iid,t in submitted:
        try:
            img=poll(t,tries=80,wait=4); save_jpgish(img, os.path.join(ASSETS,iid+'.png')); ok+=1; print('OK',iid)
        except Exception as e: fail+=1; print('FAIL',iid,e)
    print(f'\nDONE ok={ok} fail={fail} of {len(DISHES)}')

if __name__=='__main__':
    if not KEY: sys.exit('NANO_KEY missing')
    main()
