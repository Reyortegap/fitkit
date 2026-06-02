#!/usr/bin/env python3
"""Genera portadas (fotos) + mapa de músculos activados (volt highlight)."""
import os, sys, time
from gen import post, find_task_id, poll, download, KEY

# --- Fotos de portada (estilo fotográfico de marca, vertical) ---
COVERS = {
    "photos/cover-rutina.png":
        "Cinematic vertical editorial fitness photograph, a lean muscular athletic man "
        "performing a heavy barbell row in a dark moody concrete gym, dramatic side rim "
        "lighting, a neon volt green (#C6FF00) accent light glow behind him, high contrast, "
        "desaturated except the green accent, film grain, sweat, intense focus, premium magazine "
        "look, generous dark empty space at the top and bottom for title text, portrait orientation",
    "photos/cover-recetas.png":
        "Cinematic vertical editorial food photograph, high-protein muscle-building meal prep: "
        "grilled chicken, white rice, eggs and a protein shake on a dark moody surface, low-key "
        "dramatic lighting with a neon volt green (#C6FF00) accent glow, high contrast, desaturated "
        "except the green accent, premium fitness nutrition look, dark empty space at top and bottom "
        "for title text, portrait orientation",
    "photos/cover-plan.png":
        "Cinematic vertical editorial fitness photograph, a determined athletic man wrapping lifting "
        "straps around his wrists in a dark concrete gym, moody low-key lighting with a neon volt green "
        "(#C6FF00) accent glow, high contrast, desaturated except the green accent, film grain, premium, "
        "generous dark empty space at top and bottom for title text, portrait orientation",
}

# --- Mapa de músculos activados ---
MUS_TPL = (
    "Minimalist anatomy chart: a full-body muscular male figure, {view} view, standing straight with "
    "arms slightly away from the torso, flat editorial illustration on a solid dark charcoal black "
    "background. The whole body is rendered as a dark charcoal-gray muscular silhouette with subtle "
    "muscle definition lines. ONLY the {muscle} is highlighted in glowing bright neon lime green, "
    "clearly signalling it is the muscle being worked. High contrast, clean, centered composition. "
    "ABSOLUTELY NO text, no numbers, no letters, no hex codes, no labels, no watermark anywhere in the image."
)
MUSCLES = {
    "trapecio":    ("back",  "trapezius muscles (upper back and neck)"),
    "pecho":       ("front", "pectoral chest muscles"),
    "dorsales":    ("back",  "latissimus dorsi (lats, sides of the back)"),
    "hombros":     ("front", "deltoid shoulder muscles"),
    "biceps":      ("front", "biceps of both arms"),
    "triceps":     ("back",  "triceps of both arms"),
    "antebrazo":   ("front", "forearm muscles"),
    "abdominales": ("front", "rectus abdominis (six-pack abs)"),
    "oblicuos":    ("front", "oblique muscles on the sides of the abdomen"),
    "lumbar":      ("back",  "lower back erector spinae muscles"),
    "gluteos":     ("back",  "gluteal muscles (glutes)"),
    "cuadriceps":  ("front", "quadriceps thigh muscles"),
    "femoral":     ("back",  "hamstring muscles (back of thighs)"),
    "gemelos":     ("back",  "calf muscles"),
}

def run(jobs):
    base = os.path.dirname(os.path.abspath(__file__))
    submitted = []
    for out, prompt in jobs:
        full = os.path.join(base, out)
        if os.path.exists(full):
            print("skip", out); continue
        try:
            r = post(prompt); t = find_task_id(r)
            if t: submitted.append((full, t, out)); print("submit", out, t)
            else: print("NO TASKID", out, r)
        except Exception as e:
            print("submit FAIL", out, e)
        time.sleep(0.5)
    ok = fail = 0
    for full, t, out in submitted:
        try:
            img = poll(t, tries=80, wait=4); download(img, full); ok += 1; print("OK", out)
        except Exception as e:
            fail += 1; print("FAIL", out, e)
    print(f"\nDONE ok={ok} fail={fail}")

if __name__ == "__main__":
    if not KEY: sys.exit("NANO_KEY missing")
    jobs = list(COVERS.items())
    for name, (view, muscle) in MUSCLES.items():
        jobs.append((f"muscles/act-{name}.png", MUS_TPL.format(view=view, muscle=muscle)))
    run(jobs)
