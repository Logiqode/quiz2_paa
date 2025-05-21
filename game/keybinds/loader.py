import json
import pygame

def load_keybinds(path="data/keybinds.json"):
    with open(path, "r") as f:
        raw_binds = json.load(f)

    keymap = {
        "SPACE": pygame.K_SPACE,
        "ESCAPE": pygame.K_ESCAPE,
        # add more as needed
    }

    return {action: keymap[key.upper()] for action, key in raw_binds.items()}
