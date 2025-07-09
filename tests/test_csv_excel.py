from unittest.mock import patch

from src.read_csv_excel import read_csv, read_excel


@patch('pandas.read_csv')
def test_read_csv(mock_read_csv):
    """Тест функции чтения CSV файла."""
    operations = [
        {
            'id': 4699552.0,
            'state': 'EXECUTED',
            'date': '2022-03-23T08:29:37Z',
            'amount': 23423.0,
            'currency_name': 'Peso',
            'currency_code': 'PHP',
            'from': 'Discover 7269000803370165',
            'to': 'American Express 1963030970727681',
            'description': 'Перевод с карты на карту'
        }
    ]
    mock_read_csv.return_value.to_dict.return_value = operations
    result = read_csv('')
    assert result == operations


@patch('pandas.read_excel')
def test_read_excel(mock_read_excel):
    """Тест функции чтения Excel файла."""
    operations = [
        {
            'id': 4699552.0,
            'state': 'EXECUTED',
            'date': '2022-03-23T08:29:37Z',
            'amount': 23423.0,
            'currency_name': 'Peso',
            'currency_code': 'PHP',
            'from': 'Discover 7269000803370165',
            'to': 'American Express 1963030970727681',
            'description': 'Перевод с карты на карту'
        }
    ]
    mock_read_excel.return_value.to_dict.return_value = operations
    result = read_excel('')
    assert result == operations
