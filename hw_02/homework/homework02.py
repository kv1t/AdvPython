from time import perf_counter


class callstat:
    """
    Декоратор, подсчитывающий количество вызовов и 
    среднюю длительность вызова задекорированной функции.

    Пример использования:

    @callstat
    def add(a, b):
        return a + b

    r>>> add.call_count
    0
    r>>> add(1, 2)
    3
    r>>> add.call_count
    1

    Подсказки по реализации: функторы, @property
    Для измерения времени выполнения - perf_counter, см. импорт.

    """
    def __init__(self, fn):
        self.selfcallcount = 0
        self.selfcalltime = 0
        self.fn = fn


    def __call__(self, *args, **kwargs):
        self.selfcallcount += 1
        time = perf_counter()
        res = self.fn(*args, **kwargs)
        time = perf_counter() - time
        self.selfcalltime += time
        return res



    @property
    def call_count(self):
        return self.selfcallcount


    @property
    def call_time(self):
        return self.selfcalltime / self.selfcallcount

