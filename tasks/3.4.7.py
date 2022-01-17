class MetricAgent:

    def __init__(self, target_ip: str, access_key: str, scrape_period: int, send_period: int):
        self.target_ip = target_ip
        self.access_key = access_key
        self.scrape_period = scrape_period
        self.send_period = send_period
        self.scrape_count = 0

    def get_event(self):
        self.scrape_count =+ 1
        print(f"события сервера {self.target_ip} собраны. Следующий сбор через {self.scrape_period} секунд")

    def send_event(self):
        print(f"события сервера {self.target_ip} собраны отправлены на сервер сбора метрик. Следующиая отправка через {self.send_period} секунд")

    def clear_cache(self):
        print(f"кеш агента был очищен")
        self.scrape_count = 0

    def get_events_count(self):
        print(f"С сервера {self.target_ip} собрано {self.scrape_count} событий")


def main():
    print("hello")
    test1 = MetricAgent("192.168.1.1", "key", 1, 10)
    test1.clear_cache()
    test1.send_event()
    test1.get_events_count()
    test1.get_event()
    test1.get_events_count()
    test1.clear_cache()
    test1.get_events_count()


if __name__ == '__main__':

    main()
