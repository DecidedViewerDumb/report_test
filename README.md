# Скрипт подсчёта зарплаты сотрудников

## Установка

Python 3.7+ должен быть установлен.
```bash
git clone https://github.com/yourusername/payroll-reporter.git
cd payroll-reporter
python -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate
pip install -r requirements.txt  # пока не нужен, если только stdlib
```

## Использование
```bash
python main.py data1.csv data2.csv --report payout
```

## Тесты
```bash
pytest
```

## Структура проекта
```bash
├── main.py               # основной скрипт
├── tests/
│   └── test_main.py      # тесты на Pytest
└── README.md             # этот файл
```

## Скриншоты:
### Отправка одного файла:
![Пример1](screenshots/sc_data1.png)
![Пример2](screenshots/sc_data2.png)
![Пример3](screenshots/sc_data3.png)
### Отправка двух файлов:
![Пример4](screenshots/sc_data1_data2.png)
![Пример5](screenshots/sc_data1_data3.png)
![Пример6](screenshots/sc_data2_data3.png)
### Отправка трех файлов:
![Пример7](screenshots/sc_data1_data2_data3.png)
### Отправка ошибочных файлов:
![Пример8](screenshots/sc_data_error.png)