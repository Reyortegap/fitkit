#!/usr/bin/env python3
"""Genera ilustraciones específicas de las 30 recetas + mapea capítulos."""
import os, sys, time, io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'brand', 'illustrations')))
from gen import post, find_task_id, poll, STYLE, KEY, UA
import urllib.request
from PIL import Image

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
BG = (10, 11, 13)

DISHES = {
 'b1':'avocado toast topped with poached eggs and serrano ham, top view',
 'b2':'a bowl of oatmeal with banana slices, peanut butter and walnuts, top view',
 'b3':'protein french toast stack drizzled with syrup, top view',
 'b4':'a stack of banana oat pancakes with syrup, top view',
 'b5':'a breakfast burrito cut in half showing eggs, top view',
 'b6':'a thick smoothie bowl topped with fruit and granola, top view',
 's1':'a tall classic protein shake in a glass',
 's2':'a chocolate protein shake in a glass',
 's3':'a green vegetable smoothie in a glass',
 's4':'an iced coffee protein shake in a glass',
 's5':'a berry protein smoothie in a glass with berries',
 's6':'a vanilla nut protein shake in a glass',
 'l1':'a bowl of grilled chicken and white rice with vegetables, top view',
 'l2':'a plate of pasta carbonara, top view',
 'l3':'a beef burrito cut in half, top view',
 'l4':'a bowl of chickpea curry with rice, top view',
 'l5':'a mexican burrito bowl with rice, beans and meat, top view',
 'l6':'a grilled salmon fillet with sweet potato, top view',
 'd1':'a baked salmon fillet with lemon slices, top view',
 'd2':'a slice of lasagna on a plate, top view',
 'd3':'a plate of chicken curry with rice, top view',
 'd4':'a steak with roasted potatoes on a plate, top view',
 'd5':'a homemade burger with fries',
 'd6':'a homemade protein pizza, top view',
 'n1':'a toast with peanut butter and banana slices, top view',
 'n2':'a bowl of greek yogurt with granola and berries, top view',
 'n3':'a cheese quesadilla cut into triangles, top view',
 'n4':'a bowl of mixed nuts and almonds, top view',
 'n5':'canned tuna with sliced avocado on a plate, top view',
 'n6':'a chia seed pudding in a jar topped with fruit',
}
# capítulos -> reutilizar ilustraciones existentes de la librería
LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'brand', 'illustrations')
CHAPTERS = {
 'ch1':'meals/chickenrice.png','ch2':'foods/chicken.png','ch3':'foods/egg.png',
 'ch4':'meals/oatsfruit.png','ch5':'meals/proteinshake.png','ch6':'foods/broccoli.png',
}

def save_square_jpg(img_url, out):
    req=urllib.request.Request(img_url, headers={'User-Agent':UA})
    data=urllib.request.urlopen(req, timeout=120).read()
    im=Image.open(io.BytesIO(data)).convert('RGB'); w,h=im.size
    if w!=h:
        s=max(w,h); c=Image.new('RGB',(s,s),BG); c.paste(im,((s-w)//2,(s-h)//2)); im=c
    im.save(out,'JPEG',quality=90)

def main():
    # chapters (copy from library)
    for cid,src in CHAPTERS.items():
        sp=os.path.join(LIB,src); out=os.path.join(ASSETS,cid+'.jpg')
        if os.path.exists(sp):
            Image.open(sp).convert('RGB').save(out,'JPEG',quality=90); print('chapter',cid,'<-',src)
    # submit all dishes
    submitted=[]
    for iid,desc in DISHES.items():
        out=os.path.join(ASSETS,iid+'.jpg')
        try:
            r=post(STYLE+desc); t=find_task_id(r)
            if t: submitted.append((out,t,iid)); print('submit',iid,t)
            else: print('NO TASKID',iid)
        except Exception as e: print('submit FAIL',iid,e)
        time.sleep(0.4)
    ok=fail=0
    for out,t,iid in submitted:
        try:
            img=poll(t,tries=80,wait=4); save_square_jpg(img,out); ok+=1; print('OK',iid)
        except Exception as e: fail+=1; print('FAIL',iid,e)
    print(f'\nDONE ok={ok} fail={fail} of {len(DISHES)}')

if __name__=='__main__':
    if not KEY: sys.exit('NANO_KEY missing')
    main()
