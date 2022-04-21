import time
import vlc
import RPi.GPIO as GPIO
import random
import os


def flicker(led, length):
    for x in range(0, length):
        led.ChangeDutyCycle(random.randrange(0, 100))
        time.sleep(1 / 1100)


def get_audio():
    audio_files_path = "./audio"
    audio_list = next(os.walk(audio_files_path), (None, None, []))[2]
    return os.path.join(audio_files_path, audio_list[random.randrange(0, len(audio_list) - 1)])


led_pin = 22
pir_sensor = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)
led = GPIO.PWM(led_pin, 1000)
led.start(0)

GPIO.setup(pir_sensor, GPIO.IN)
current_state = 0

print("starting!")

try:
    while True:
        time.sleep(0.1)
        current_state = GPIO.input(pir_sensor)
        if current_state == 1:
            flicker(led, 2)
            print("Playing audio!")
            mp = vlc.MediaPlayer()
            x = vlc.Media(get_audio())
            mp.set_media(x)
            time.sleep(0.1)
            mp.play()
            mp.audio_set_volume(20)
            mp.set_pause(0)
            time.sleep(1)
            value = mp.get_length()
            print(f"song length is {value / 1000} seconds")
            mp.play()
            flicker(led, int(value))
            led.ChangeDutyCycle(0)
            mp.release()

except KeyboardInterrupt:
    GPIO.cleanup()
    pass
finally:
    GPIO.cleanup()
