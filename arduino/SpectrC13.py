import csv
import pyfirmata
from threading import Thread
import cv2
from time import sleep
import keyboard as kb

port = 'COM5'
board = pyfirmata.Arduino(port)
print("112")
it = pyfirmata.util.Iterator(board)
it.start()
print("Ардуина подключилась")


# Функция открытия окна с видео перехваченного с камеры
def GetVidio():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#    cap = cv2.VideoCapture("http://192.168.1.1:8080/video")
    while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        width = cap.get(4)
        height = cap.get(3)
#        cv2.circle(frame, (round(height/2), round(width/2)), 2, (0, 255, 0), 0)
        cv2.circle(frame, (round(337), round(264)), 1, (0, 255, 0), 0)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


Thread(target=GetVidio).start()

# поворот фотоприёмника равен 16/9 поворота призмы!!
# Для смещения призмы и фотоприемника постоянные
n = 200
m = 1
tb = 0.0005
n3 = 0
fi = 0
dangl = 0.0006592  # последнее уточнение!!!!!


p1 = board.get_pin('d:13:o')  # верхний транслятор (12, 13)
p2 = board.get_pin('d:12:o')  # p1, p2 - y-трансляция стола
p3 = board.get_pin('d:9:o')  # нижний транслятор (9, 10)
p4 = board.get_pin('d:10:o')  # p1, p2 - y-трансляция стола
a2 = board.get_pin('d:11:i')  # концевик №1 и 2
a3 = board.get_pin('d:8:i')  # концевик №3 и 4

p7 = board.get_pin('d:5:o')
p8 = board.get_pin('d:4:o')  # p7, p8 - вращение стола
p9 = board.get_pin('d:3:o')
p10 = board.get_pin('d:2:o')  # p9, p10 - вращение фотоприемника

a4 = board.get_pin('a:5:i')  # фотоприемник №3
a0 = board.get_pin('a:4:i')  # фотоприемник №1   'a:0:i' подвижный
a5 = board.get_pin('a:3:i')  # фотоприемник №4
a1 = board.get_pin('a:2:i')  # фотоприемник №2   'a:1:i' опорный


def rotate(direction, manual=0, *steps):
    if manual != 0:
        n, m = steps[0], steps[-1]
    else:
        n, m = 9, 16
    for i in range(n):
        p8.write(direction)
        p7.write(1)
        sleep(tb)
        p7.write(0)
    print("rotate prism")
    for j in range(m):
        p10.write(direction)
        p9.write(1)
        sleep(tb)
        p9.write(0)
    print("rotate phot")


kb.add_hotkey("1", lambda: rotate(0, 1, 1, 0))
kb.add_hotkey("alt + 1", lambda: rotate(0, 1, 500, 0))
kb.add_hotkey("2", lambda: rotate(1, 1, 1, 0))
kb.add_hotkey("alt + 2", lambda: rotate(1, 1, 500, 0))
kb.add_hotkey("3", lambda: rotate(0, 1, 0, 1))
kb.add_hotkey("alt + 3", lambda: rotate(0, 1, 0, 500))
kb.add_hotkey("4", lambda: rotate(1, 1, 0, 1))
kb.add_hotkey("alt + 4", lambda: rotate(1, 1, 0, 500))
while True:
    kb.wait("ctrl + c")
    break
