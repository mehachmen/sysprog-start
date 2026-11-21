# Ядро агента (C)

Ядро собирается в динамическую библиотеку: `sentry_core.dll` в Windows, `libsentry_core.dylib` в macOS,
`libsentry_core.so` в Linux. Первая функция появляется на паре 2. Какие файлы и в какой главе появляются здесь — в [`agent/README.md`](../README.md).

| Файл | Что в нём |
|---|---|
| `core.h` | заголовок ядра: `struct core_info` (`pid`, `cpus`, `page_size`, `host`) с типами точного размера `int64_t` и `int32_t` и объявление `core_get_info` |
| `core_info.c` | функция `core_get_info`: вызывает функции системы и заполняет `struct core_info`; при ошибке возвращает её код |
| `show_info.c` | пробная программа: вызывает `core_get_info` и печатает поля структуры, её размер и адрес |
