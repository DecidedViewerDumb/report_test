import argparse
import os.path
import sys
from collections import defaultdict
from typing import List, Dict, Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Генерация отчетов на основе CSV-файлов с данными сотрудников"
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="+",
        help="Пути к CSV-файлам с данными сотрудников"
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Тип отчета, например 'payout'"
    )
    return parser.parse_args()


def read_employees_from_file(filepath: str) -> List[Dict[str, Optional[float]]]:
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")

    employees = []
    with open(filepath, encoding="utf-8") as f:
        header = f.readline().strip().split(",")
        columns = {name.strip(): n for n, name in enumerate(header)}

        column_keys = {'id', 'email', 'name', 'department', 'hours_worked'}

        # Проверка обязательных полей
        if not column_keys.issubset(columns.keys()):
            missing = column_keys - columns.keys()
            raise ValueError(f"Нехватает столбцов: {missing}")

        # Находим оставшийся столбец
        last_key = set(columns.keys()) - column_keys
        if len(last_key) != 1:
            raise ValueError(f"Не возможно определить столбец со ставкой, из-за лишних столбцов: {last_key}")
        rate_column = last_key.pop()

        for i in f:
            if not i.strip():
                continue
            tmp = i.strip().split(",")
            employee = {
                "name": tmp[columns["name"]],
                "department": tmp[columns["department"]],
                "hours": int(tmp[columns["hours_worked"]]),
                "rate": float(tmp[columns[rate_column]]),
            }
            employee["payout"] = employee["hours"] * employee["rate"]
            employees.append(employee)
    return employees


def generate_payout_report(employees: List[Dict[str, Optional[float]]]) -> None:
    departments = defaultdict(list)
    for i in employees:
        departments[i["department"]].append(i)

    max_name_len = max(len(i["name"]) for i in employees)

    # Заголовок
    name_col = "name".ljust(max_name_len)
    print(f"{' ' * 14}\t{name_col} \thours \trate \tpayout")

    for dept in sorted(departments):
        print(dept)
        total_hours = 0
        total_payout = 0
        len_name = 0
        for i in departments[dept]:
            len_name = len(i['name']) if len_name < len(i['name']) else len_name
            name = i["name"].ljust(max_name_len)
            hours = str(i["hours"])
            rate = str(int(i["rate"]))
            payout = f"${int(i['payout'])}"
            print(f"{'-' * 14}\t{name}\t{hours}\t{rate}\t{payout}")
            total_hours += i["hours"]
            total_payout += i["payout"]
        print(f"{' ' * 14}\t{' ' * len_name}\t{total_hours}\t\t${int(total_payout)}")


def main() -> None:
    args = parse_args()

    if args.report != "payout":
        print(f"Тип отчета '{args.report}' не поддерживается")
        sys.exit()

    all_employees = []
    for file in args.files:
        try:
            employees = read_employees_from_file(file)
            all_employees.extend(employees)
        except FileNotFoundError as err:
            print(err)
            sys.exit()
        except ValueError as err:
            print(f"Ошибка в файле {file}: {e}")
            sys.exit()

    sorted(all_employees, key=lambda x: x['department'])
    generate_payout_report(all_employees)


if __name__ == "__main__":
    main()
