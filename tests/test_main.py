import pytest
from main import read_employees_from_file, generate_payout_report


@pytest.fixture
def valid_csv():
    return """id,email,name,department,hours_worked,salary
    1,a@example.com,Alice Johnson,Marketing,160,50
    2,b@example.com,Bob Smith,Design,150,40
    3,c@example.com,Carol Williams,Design,170,60
    """


# Базовое чтение файла
def test_read_employees(tmp_path, valid_csv):
    test_file = tmp_path / "data1.csv"
    test_file.write_text(valid_csv)
    employees = read_employees_from_file(str(test_file))

    assert len(employees) == 3
    assert employees[0]["name"] == "Alice Johnson"
    assert employees[1]["payout"] == 150 * 40
    assert employees[2]["department"] == "Design"


# Проверка на нехватку столбцов
def test_missing_required_column(tmp_path):
    csv_data = """id,email,name,hours_worked,salary
    1,a@example.com,Alice Johnson,160,50
    """
    test_file = tmp_path / "bad.csv"
    test_file.write_text(csv_data)
    with pytest.raises(ValueError, match="Нехватает столбцов"):
        read_employees_from_file(str(test_file))


# Проверка на неизвестную колонку, которой не должно быть
def test_multiple_unknown_columns(tmp_path):
    csv_data = """id,email,name,department,hours_worked,salary,bonus
    1,a@example.com,Alice Johnson,Marketing,160,50,500
    """
    test_file = tmp_path / "data1.csv"
    test_file.write_text(csv_data)
    with pytest.raises(ValueError, match="Не возможно определить столбец со ставкой"):
        read_employees_from_file(str(test_file))


# Перехватывает вывод с помощью capsys в консоль и проверяет итоговый вывод
def test_generate_payout_report_output(capsys):
    employees = [
        {"name": "Bob Smith", "department": "Design", "hours": 150, "rate": 40, "payout": 6000},
        {"name": "Carol Williams", "department": "Design", "hours": 170, "rate": 60, "payout": 10200},
        {"name": "Alice Johnson", "department": "Marketing", "hours": 160, "rate": 50, "payout": 8000},
    ]
    generate_payout_report(employees)
    captured = capsys.readouterr()
    assert "Design" in captured.out
    assert "$10200" in captured.out
    assert "Marketing" in captured.out
    assert "$8000" in captured.out
    assert "Carol Williams" in captured.out
