import re


class MetricAgent:

    def __init__(self, target_ip: str, access_key: str, scrape_period: int, send_period: int):
        self.target_ip = target_ip
        self.access_key = access_key
        self.__scrape_period = scrape_period
        self._send_period = send_period
        self.__scrape_count = 0

    @property
    def scrape_period(self):
        return self.__scrape_period

    @property
    def send_period(self):
        return self._send_period

    @scrape_period.setter
    def scrape_period(self, string):
        self.__scrape_period = self.__time_to_sec(string)

    @send_period.setter
    def send_period(self, string):
        self._send_period = self.__time_to_sec(string)

    def get_event(self):
        self.__scrape_count += 1
        print(f"события сервера {self.target_ip} собраны. Следующий сбор через {self.scrape_period} секунд")

    def send_event(self):
        print(f"события сервера {self.target_ip} собраны отправлены на сервер сбора метрик. Следующиая отправка через {self._send_period} секунд")

    def clear_cache(self):
        print("кеш агента был очищен")
        self.__scrape_count = 0

    def get_events_count(self):
        print(f"С сервера {self.target_ip} собрано {self.__scrape_count} событий")

    def __time_to_sec(self, string):
        if "-" in string:
            raise ValueError
        new_value = 0
        str_dig = re.split("\D", string)[:-1]
        str_let = re.split("\d+", string)[1:]
        for i in range(0, len(str_dig)):
            if str_let[i] == "h":
                new_value += int(str_dig[i]) * 3600
            if str_let[i] == "m":
                new_value += int(str_dig[i]) * 60
            if str_let[i] == "s":
                new_value += int(str_dig[i])
        return new_value


class PrometheusAgent(MetricAgent):
    def __init__(self, target_ip: str, access_key: str, scrape_period: int, send_period: int):
        super().__init__(target_ip, access_key, scrape_period, send_period)
        self._send_period = None

    def send_event(self):
        print(f"события сервера {self.target_ip} собраны отправлены по запросу от Prometheus")

    @MetricAgent.send_period.setter
    def send_period(self, atr):
        print("Prometheus не позволяет управлять периодом отправки событий")
        self._send_period = None


class CarbonAgent(MetricAgent):
    def __init__(self, target_ip: str, access_key: str, carbon_server: str, scrape_period: int, send_period: int):
        super().__init__(target_ip, access_key, scrape_period, send_period)
        self.carbon_server = carbon_server

    def send_event(self):
        print(f"события сервера {self.target_ip} собраны отправлены в Carbon. Следующая отправка через {self.send_period} секунд")


def main():
    print("hello")

    prometheus = PrometheusAgent("192.168.1.1", "key", 1, 0)
    test1 = MetricAgent("192.168.1.1", "key", 1, 10)
    regular_agent = MetricAgent("192.168.1.1", "key", 1, 10)

    prometheus.clear_cache()
    prometheus.send_event()
    prometheus.get_events_count()
    prometheus.get_event()
    prometheus.get_events_count()
    prometheus.clear_cache()
    prometheus.get_events_count()

    print(f"scrape_period {test1.scrape_period}")
    test1.scrape_period = "1h0m15s"
    print(f"scrape_period {test1.scrape_period}")

    print(f"send_period {test1.send_period}")
    test1.send_period = "0h0m25s"
    print(f"send_period {test1.send_period}")

    print(f"base send_period {prometheus.send_period}")
    prometheus.send_period = 2
    regular_agent.send_period = "1h0m15s"
    print(f"!!!!send_period {prometheus.send_period}")


if __name__ == '__main__':

    main()
