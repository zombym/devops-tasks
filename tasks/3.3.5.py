from collections import deque
import random
import re


def generate_proxy_string(max_value):
    return str([f"proxyhost{number}.slurm.io" for number in range(max_value)])


if __name__ == '__main__':
    msg = input()
    if msg is None:
        proxy_list = msg
    else:
        proxy_list = generate_proxy_string(random.randint(3, 50))
        print(proxy_list)
        proxy_list = deque(proxy_list.strip("[]").split(","))
        for i in range(0, len(proxy_list)):
            proxy_list[i] = proxy_list[i].replace("'", "").strip()

    for _ in range(0, 1000):
        print(f'Обращение при помощи прокси "{proxy_list[0]}"')
        number = int(re.split('[^\d+]', proxy_list[0])[9])
        if number % 3 == 0 or number % 8 == 0:
            proxy_list.popleft()
        else:
            print(f"Было осуществлено обращение к ресурсу при помощи прокси \"{proxy_list[0]}\"")
            first_value = proxy_list.popleft()
            proxy_list.append(first_value)

    print(f"Прокси осталось  {len(proxy_list)}")
