import os
import time
import pygame

BASE_DIR = os.path.dirname(__file__)
FILES = [
    "eat.mp3",
    "death.mp3",
    "level_up.mp3",
]

print("Initializing mixer...")
pygame.mixer.init()
print("Mixer init params:", pygame.mixer.get_init())

for name in FILES:
    path = os.path.join(BASE_DIR, name)
    try:
        sound = pygame.mixer.Sound(path)
    except Exception as exc:
        print(f"{name}: failed to load -> {exc}")
        continue
    length = sound.get_length()
    volume = sound.get_volume()
    print(f"{name}: length={length:.3f}s volume={volume:.2f}")
    channel = sound.play()
    if channel is None:
        print(f"{name}: no channel returned from play()")
        continue
    print(f"{name}: channel busy immediately? {channel.get_busy()}")
    time.sleep(min(1.0, sound.get_length() + 0.1))

pygame.mixer.quit()
print("Done.")
