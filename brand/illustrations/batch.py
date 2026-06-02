#!/usr/bin/env python3
"""Genera la librería completa de ilustraciones FITKIT en lote."""
import os, sys, time
from gen import post, find_task_id, poll, download, STYLE, KEY

LIB = {
    "exercises": {
        "deadlift": "a muscular athletic man performing a barbell deadlift, full body, side view",
        "benchpress": "a muscular athletic man performing a barbell bench press lying on a bench, side view",
        "pullup": "a muscular athletic man doing a pull-up on a horizontal bar, front view, full body",
        "overheadpress": "a muscular athletic man performing a standing barbell overhead press, full body",
        "row": "a muscular athletic man performing a bent-over barbell row, side view, full body",
        "curl": "a muscular athletic man performing a standing dumbbell biceps curl, full body",
        "dips": "a muscular athletic man performing parallel bar dips, side view, full body",
        "lunge": "a muscular athletic man performing a forward lunge holding dumbbells, full body",
        "hipthrust": "a muscular athletic man performing a barbell hip thrust, side view",
        "legpress": "a muscular athletic man performing a leg press on a machine, side view",
    },
    "foods": {
        "egg": "two eggs, one whole and one cracked open",
        "oats": "a bowl of rolled oats",
        "rice": "a bowl of cooked white rice",
        "chicken": "a grilled chicken breast fillet",
        "tuna": "an open can of tuna fish",
        "banana": "a single banana",
        "peanutbutter": "a jar of peanut butter with a spoon",
        "milk": "a tall glass of milk",
        "salmon": "a raw salmon fillet",
        "broccoli": "a head of broccoli",
        "avocado": "an avocado cut in half with the pit",
        "almonds": "a small pile of almonds",
    },
    "meals": {
        "chickenrice": "a bowl of grilled chicken, white rice and vegetables, top view",
        "proteinshake": "a protein shaker bottle full of shake",
        "oatsfruit": "a bowl of oatmeal topped with banana slices and berries, top view",
        "pasta": "a plate of pasta with ground meat, top view",
    },
    "muscles": {
        "chest": "anatomical illustration of male chest pectoral muscles on a torso",
        "back": "anatomical illustration of male back muscles, rear view torso",
        "legs": "anatomical illustration of male leg quadriceps and hamstring muscles",
        "shoulders": "anatomical illustration of male shoulder deltoid muscles",
        "arms": "anatomical illustration of a flexed male arm showing biceps and triceps",
        "core": "anatomical illustration of male abdominal core six-pack muscles on a torso",
    },
}

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    jobs = []   # (out, subject)
    for cat, items in LIB.items():
        for name, subj in items.items():
            out = os.path.join(base, cat, name + ".png")
            if os.path.exists(out):
                print(f"skip {cat}/{name} (exists)")
                continue
            jobs.append((out, subj, f"{cat}/{name}"))

    # 1) submit all
    submitted = []
    for out, subj, label in jobs:
        try:
            res = post(STYLE + subj)
            tid = find_task_id(res)
            if tid:
                submitted.append((out, tid, label))
                print(f"submit {label} -> {tid}")
            else:
                print(f"NO TASKID {label}: {res}")
        except Exception as e:
            print(f"submit FAIL {label}: {e}")
        time.sleep(0.5)

    # 2) poll + download
    ok, fail = 0, 0
    for out, tid, label in submitted:
        try:
            img = poll(tid, tries=80, wait=4)
            if img:
                download(img, out)
                ok += 1
                print(f"OK  {label}")
            else:
                fail += 1
                print(f"NOIMG {label}")
        except Exception as e:
            fail += 1
            print(f"FAIL {label}: {e}")

    print(f"\nDONE ok={ok} fail={fail} of {len(jobs)}")

if __name__ == "__main__":
    if not KEY:
        sys.exit("NANO_KEY missing")
    main()
