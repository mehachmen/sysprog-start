import json, socket, sys, time, http.client
from urllib.parse import urlparse

def now():
    return time.strftime("%H:%M:%S")

def check(svc):
    u = urlparse(svc["url"])
    host, port = u.hostname, u.port or 80
    path = u.path or "/"
    t = svc.get("timeout_seconds", 1)
    start = time.time()
    # шаг 1: просто TCP-соединение
    try:
        s = socket.create_connection((host, port), timeout=t)
        s.close()
    except ConnectionRefusedError:
        return "DOWN", "порт закрыт (connection refused)", start
    except socket.timeout:
        return "DOWN", "тайм-аут при соединении", start
    except OSError as e:
        return "DOWN", "ошибка сети: %s" % e, start
    # шаг 2: сам HTTP-запрос
    try:
        c = http.client.HTTPConnection(host, port, timeout=t)
        c.request("GET", path)
        r = c.getresponse()
        r.read()
        c.close()
    except socket.timeout:
        return "HANG", "порт открыт, но ответа нет за %s с (тайм-аут чтения)" % t, start
    except Exception as e:
        return "HANG", "порт открыт, HTTP не получился: %s" % e, start
    if 200 <= r.status < 300:
        return "OK", "HTTP %d" % r.status, start
    return "BAD", "HTTP %d (сервис отвечает, но с ошибкой)" % r.status, start

def main():
    cfg = sys.argv[1] if len(sys.argv) > 1 else "services.json"
    services = json.load(open(cfg, encoding="utf-8"))["services"]
    log = open("check.log", "a", encoding="utf-8")
    bad = 0
    for s in services:
        st, msg, start = check(s)
        took = time.time() - start
        line = "%s  %-10s %-5s %s  [%.2f с]" % (now(), s["name"], st, msg, took)
        print(line)
        log.write(line + "\n")
        if st != "OK":
            bad += 1
    log.close()
    sys.exit(1 if bad else 0)

main()
