#!/usr/bin/env python
import RPi.GPIO as GPIO
import os
import pygame
import pygame.freetype

import sys
import subprocess
import time
import _thread

sys.path.append("home/pi/go/bin/")
photo_folder = "/home/pi/fotobox_bilder"
qr_path = "/home/pi/fotobox/qr_small.png"
qr_image = None

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # input
GPIO.setup(18, GPIO.OUT)  # LED
GPIO.setup(17, GPIO.OUT)  # green led

WIDTH = 1680
HEIGHT = 1050


def io_remote():
    # switch on ready
    GPIO.output(17, 1)
    # wait for button press
    GPIO.wait_for_edge(22, GPIO.RISING, bouncetime=100)
    # switch of green light
    GPIO.output(17, 0)


def get_file_name():
    # name mit Timestamp versehen
    ts = time.gmtime()
    readable_ts = time.strftime("%H_%M_%S", ts)
    photo_name = "/bhwp_2020_" + readable_ts + ".jpg"
    return photo_folder + photo_name


def load_image(img_path):
    return pygame.image.load(img_path).convert()


def signal_hook(running=True):
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runnig = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()


def display_image(screen, img):
    try:
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        screen.blit(img, (0, 0))
    except:
        pass
    pygame.display.flip()
    pygame.display.update()


def display_qr(screen, qr):
    screen.blit(qr, (1330, 700))
    pygame.display.flip()
    pygame.display.update()


def display_text(screen, text, color=(20, 240, 100), size=70):
    font = pygame.freetype.Font(
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf", size
    )
    text_renderd, text_rect = font.render(text, color)
    screen_rect = screen.get_rect()
    text_rect.centerx = screen_rect.centerx
    screen.blit(text_renderd, (50, 50))
    pygame.display.update()


def sync_photo(photo_path):
    # hochladen des bildes
    print("Uploading file..")
    print(os.path.isfile(photo_path))
    subprocess.run(
        ["rclone", "copy", "{}".format(photo_path), "fotobox_remote:fotobox"]
    )
    print("photo uploaded!")


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 0)
_thread.start_new_thread(signal_hook, ())
if not qr_image:
    qr_img = load_image(qr_path)

while 1:
    print("Starting...")
    GPIO.output(18, 0)
    while 1:
        display_qr(screen, qr_img)
        io_remote()
        try:
            display_image(screen, img)
        except NameError:
            pass
        display_text(screen, "Geschafft! Erstmal chillen...", color=(10, 50, 255))
        # shoot picture
        photo_path = get_file_name()
        print(photo_path)
        # Capture photo
        try:
            subprocess.run(
                [
                    "gphoto2",
                    "--capture-image-and-download",
                    "--camera='Canon EOS 350D (normal mode)'",
                    "--filename={}".format(photo_path),
                    "--force-overwrite",
                ]
            )
        except:
            continue
        try:
            img = load_image(photo_path)
            display_image(screen, img)
            display_text(
                screen, "Zuerst das Vergnügen, dann der Upload in die cloud...", size=50
            )
        except:
            pass

        try:
            if os.path.isfile(photo_path):
                sync_photo(photo_path)
        except:
            print("not uplloaded")

        display_image(screen, img)
        display_text(screen, "Kamera is breit!", color=(20, 230, 20))
        print("Return to main process")

# gdrive about --service-account fotobox-265418-e52db5a765c2.json
# gdrive  --service-account fotobox-265418-e52db5a765c2.json  share ~/fotobox_bilder

# gdrive  --service-account fotobox-265418-e52db5a765c2.json  sync list
