if __name__ == '__main__':
    branch_name = input()
    test_result = int(input())
    coverage_change = float(input())
    approve_count = int(input())

    result_text = ["не пройдены", "пройдены"]
    is_test_result_ok = test_result == 1
    is_first_condition_ok = test_result == 1 and coverage_change > 5
    is_second_condition_ok = test_result == 1 and 0 < coverage_change <= 5 and approve_count > 3

if branch_name.capitalize() in ("Development", "Staging"):
    if is_test_result_ok and (is_first_condition_ok or is_second_condition_ok):
        print(f"Внимание! Код из {branch_name} отправлен в релиз!")
    else:
        print(f"Код из {branch_name} с результатами тесты: {result_text[is_test_result_ok]}, coverage: {coverage_change}, approve: {approve_count} в релиз не попадает. ")
else:
    print(f"В ветке {branch_name} непроверенный код, пропускаем")
