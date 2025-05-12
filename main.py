import argparse


def parse_args():
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


def main():
    args = parse_args()
    print(f"Принятые файлы: {args.files}")
    print(f"Тип отчета: {args.report}")
    print("(Заглушка: отчет пока не формируется)")


if __name__ == "__main__":
    main()
