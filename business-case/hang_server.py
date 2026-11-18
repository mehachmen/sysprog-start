# принимает соединение и молчит порт открыт, а ответа нет
import socket, time
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 8768)); s.listen(5)
keep = []
while True:
    c, _ = s.accept(); keep.append(c)
