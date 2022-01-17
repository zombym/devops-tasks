import re


class MetricAgent:

    def __init__(self, target_ip: str, access_key: str, scrape_period: int, send_period: int):
        self.target_ip = target_ip
        self.access_key = access_key
        self.__scrape_period = scrape_period
        self.__send_period = send_period
        self.__scrape_count = 0

    @property
    def scrape_period(self):
        return self.__scrape_period

    @property
    def send_period(self):
        return self.__send_period

    @scrape_period.setter
    def scrape_period(self, str):
        self.__scrape_period = self.__time_to_sec(str)

    @send_period.setter
    def send_period(self, str):
        self.__send_period = self.__time_to_sec(str)

    def get_event(self):
        self.__scrape_count += 1
        print(f"события сервера {self.target_ip} собраны. Следующий сбор через {self.scrape_period} секунд")

    def send_event(self):
        print(f"события сервера {self.target_ip} собраны отправлены на сервер сбора метрик. Следующиая отправка через {self.send_period} секунд")

    def clear_cache(self):
        print(f"кеш агента был очищен")
        self.__scrape_count = 0

    def get_events_count(self):
        print(f"С сервера {self.target_ip} собрано {self.__scrape_count} событий")

    def __time_to_sec(self, str):
        if "-" in str:
            raise ValueError
        new_value = 0
        str_dig = re.split("\D", str)[:-1]
        str_let = re.split("\d+", str)[1:]
        for i in range(0, len(str_dig)):
            if str_let[i] == "h":
                new_value += int(str_dig[i]) * 3600
            if str_let[i] == "m":
                new_value += int(str_dig[i]) * 60
            if str_let[i] == "s":
                new_value += int(str_dig[i])
        return new_value


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

    print(f"scrape_period {test1.scrape_period}")
    test1.scrape_period = "1h0m15s"
    print(f"scrape_period {test1.scrape_period}")

    print(f"send_period {test1.send_period}")
    test1.send_period = "0h0m15s"
    print(f"send_period {test1.send_period}")


if __name__ == '__main__':

    main()
