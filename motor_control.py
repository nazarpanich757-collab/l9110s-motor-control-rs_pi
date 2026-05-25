"""
Библиотека для управления моторами через драйвер L9110S.

Этот модуль предоставляет класс Motor для управления скоростью и направлением
каждого мотора по отдельности, а также функцию механизм-управления.

Пример использования:
    from motor_control import Motor

    motor_a = Motor(17, 18)
    motor_a.on(70)      # ехать вперёд на 70%
    motor_a.on(-50)     # ехать назад на 50%
    motor_a.off()       # остановить

Классы:
    Motor — управление одним мотором.

Функции:
    dead_zone(value) — обнуляет значения меньше порога.
"""


import RPi.GPIO as GPIO
import time

class Motor:
    """Управление произвольным мотором через драйвер L9110S.

    Этот класс настраивает два пина: DIR (направление) и PWM (скорость).
    Поддерживает скорость от -100 до 100: положительная — вперёд,
    отрицательная — назад, 0 — стоп.

    Параметры:
        DIR: номер GPIO-пина для направления.
        PWM: номер GPIO-пина для ШИМ (скорости).

    Пример:
        motor = Motor(17, 18)
        motor.on(50)
    """

    def __init__(self, DIR, PWM):
        self.DIR = DIR
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(PWM, GPIO.OUT)
        GPIO.output(DIR, GPIO.LOW)
        self.PWM = GPIO.PWM(PWM, 1000)
        self.PWM.start(0)
        self.off()

    def on(self, speed):
        if speed > 0:
            GPIO.output(self.DIR, GPIO.LOW)
            self.PWM.ChangeDutyCycle(speed)
        elif speed < 0:
            GPIO.output(self.DIR, GPIO.HIGH)
            inverted = 100 - abs(speed)
            duty = (inverted * 86) // 100
            self.PWM.ChangeDutyCycle(duty)
        else:
            self.PWM.ChangeDutyCycle(0)

    def off(self):
        GPIO.output(self.DIR, GPIO.LOW)
        self.PWM.ChangeDutyCycle(0)

    @staticmethod
    def matrix(motors, m):
        motors[0].on(m[0][0])
        motors[1].on(m[0][1])
        motors[2].on(m[1][0])
        motors[3].on(m[1][1])
