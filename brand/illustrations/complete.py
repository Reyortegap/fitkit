#!/usr/bin/env python3
"""Completa la librería FITKIT: 8 portadas + ilustraciones (suplementos, casa, mujer, recuperación)."""
import os, sys, time
from gen import post, find_task_id, poll, download, STYLE, KEY

# --- Portadas (fotográficas, verticales, estilo de marca) ---
PHOTO_BASE = ("Cinematic vertical editorial photograph, dark moody concrete gym aesthetic, low-key "
              "dramatic lighting with a neon lime green accent glow, high contrast, desaturated except "
              "the green accent, film grain, premium fitness brand look, generous dark empty space at top "
              "and bottom for title text, portrait orientation. NO text, no letters, no watermark. Subject: ")
COVERS = {
    "photos/cover-mujeres.png":       PHOTO_BASE + "a fit athletic woman training her lower body with a barbell, strong glutes and legs, confident",
    "photos/cover-recomposicion.png": PHOTO_BASE + "a lean defined muscular man flexing showing low body fat and muscle definition, body recomposition",
    "photos/cover-suplementos.png":   PHOTO_BASE + "a protein powder tub, a creatine jar and supplement capsules arranged on a dark surface",
    "photos/cover-metabolismo.png":   PHOTO_BASE + "a lean athletic shirtless man with visible abs standing, metabolism and energy theme",
    "photos/cover-casa.png":          PHOTO_BASE + "a muscular man doing a push-up on the floor of a dark minimalist apartment living room, home workout",
    "photos/cover-presupuesto.png":   PHOTO_BASE + "cheap high-protein groceries: eggs, rice, oats, bananas and milk on a dark surface, budget nutrition",
    "photos/cover-recuperacion.png":  PHOTO_BASE + "a muscular man stretching and resting after training in a dark gym, recovery theme",
    "photos/cover-mente.png":         PHOTO_BASE + "a focused intense muscular man portrait, eyes closed in concentration, mental strength and discipline",
}

# --- Ilustraciones duotono (usan STYLE) ---
ILLOS = {
    # suplementos
    "supplements/creatine.png":   "a jar of creatine monohydrate powder with a scoop",
    "supplements/whey.png":       "a large tub of whey protein powder",
    "supplements/omega3.png":     "fish oil omega-3 softgel capsules",
    "supplements/vitamind.png":   "a bottle of vitamin D pills with a small sun symbol",
    "supplements/preworkout.png": "a pre-workout shaker bottle with a scoop of powder",
    # ejercicios en casa (peso corporal)
    "home/pushup.png":            "a muscular athletic man performing a push-up on the floor, side view, full body",
    "home/bodyweightsquat.png":   "a muscular athletic man performing a bodyweight squat, side view, full body",
    "home/plank.png":             "a muscular athletic man holding a plank position, side view, full body",
    "home/pikepushup.png":        "a muscular athletic man performing a pike push-up, side view, full body",
    "home/chairdips.png":         "a muscular athletic man performing tricep dips on a chair, side view, full body",
    # mujer
    "female/fem-squat.png":       "a fit athletic woman performing a barbell back squat, full body, side view",
    "female/fem-hipthrust.png":   "a fit athletic woman performing a barbell hip thrust, side view, full body",
    "female/fem-fullbody.png":    "a full-body fit athletic woman figure standing, front view, athletic physique",
    "female/fem-glutes.png":      "minimalist anatomy chart of a female body rear view with the gluteal muscles highlighted in bright neon lime green, the rest dark charcoal silhouette, no text",
    # recuperación / conceptos
    "recovery/sleep.png":         "a person sleeping peacefully in bed, rest and muscle recovery",
    "recovery/stretching.png":    "a muscular athletic man doing a standing stretch, full body, side view",
    "recovery/foamroll.png":      "a muscular athletic man using a foam roller on his leg on the floor",
}

def run():
    base = os.path.dirname(os.path.abspath(__file__))
    jobs = []
    for out, p in COVERS.items():
        jobs.append((out, p))
    for out, subj in ILLOS.items():
        jobs.append((out, STYLE + subj))

    submitted = []
    for out, prompt in jobs:
        full = os.path.join(base, out)
        if os.path.exists(full):
            print("skip", out); continue
        try:
            r = post(prompt); t = find_task_id(r)
            if t: submitted.append((full, t, out)); print("submit", out, t)
            else: print("NO TASKID", out, str(r)[:160])
        except Exception as e:
            print("submit FAIL", out, e)
        time.sleep(0.5)

    ok = fail = 0
    for full, t, out in submitted:
        try:
            img = poll(t, tries=80, wait=4); download(img, full); ok += 1; print("OK", out)
        except Exception as e:
            fail += 1; print("FAIL", out, e)
    print(f"\nDONE ok={ok} fail={fail} of {len(jobs)}")

if __name__ == "__main__":
    if not KEY: sys.exit("NANO_KEY missing")
    run()
