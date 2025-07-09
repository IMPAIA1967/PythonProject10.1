from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_empty_data() -> None:
    """Тест фильтрации пустого списка"""
    assert filter_by_state([]) == []


def test_sort_with_same_dates() -> None:
    """Тест сортировки при одинаковых датах"""
    test_data: List[Dict[str, Any]] = [
        {"id": 1, "date": "2023-01-01T00:00:00"},
        {"id": 2, "date": "2023-01-01T00:00:00"},  # Та же дата
    ]
    result = sort_by_date(test_data)
    # Проверяем что оба элемента присутствуют (порядок может быть любой)
    assert {item["id"] for item in result} == {1, 2}


def test_sort_empty_data() -> None:
    """Тест сортировки пустого списка"""
    assert sort_by_date([]) == []


def test_sort_invalid_dates() -> None:
    """Тест сортировки с некорректными датами"""
    test_data: List[Dict[str, Any]] = [
        {"id": 1, "date": "invalid_date"},
        {"id": 2, "date": "2023-01-01T00:00:00"},
    ]
    result = sort_by_date(test_data)
    # Некорректная дата должна быть в начале при reverse=True
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


SAMPLE_DATA: List[Dict[str, Any]] = [
    {"id": 1, "state": "EXECUTED", "date": "2023-01-01T00:00:00"},
    {"id": 2, "state": "CANCELED", "date": "2023-01-02T00:00:00"},
    {"id": 3, "state": "EXECUTED", "date": "2023-01-03T00:00:00"},
    {"id": 4, "state": "PENDING", "date": "2023-01-04T00:00:00"},
    {"id": 5, "state": "EXECUTED", "date": "2023-01-03T00:00:00"},
]


@pytest.mark.parametrize("state, expected_ids", [
    ("EXECUTED", [1, 3, 5]),
    ("CANCELED", [2]),
    ("PENDING", [4]),
    ("UNKNOWN", []),
    ("", []),
])
def test_filter_by_state(state: str, expected_ids: List[int]) -> None:
    """Тестирование фильтрации по статусу"""
    result = filter_by_state(SAMPLE_DATA, state)
    assert [item["id"] for item in result] == expected_ids


def test_main_data_processing() -> None:
    """Тестирование обработки данных из main"""
    test_data: List[Dict[str, Any]] = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    # Проверяем фильтрацию
    filtered = filter_by_state(test_data)
    assert len(filtered) == 2
    assert all(item["state"] == "EXECUTED" for item in filtered)

    # Проверяем сортировку
    sorted_data = sort_by_date(test_data)
    assert sorted_data[0]["id"] == 41428829  # Самая новая дата first
    assert sorted_data[-1]["id"] == 939719570  # Самая старая last


def test_sort_single_item() -> None:
    """Тест сортировки списка с одним элементом"""
    test_data: List[Dict[str, Any]] = [{"id": 1, "date": "2023-01-01T00:00:00"}]
    assert sort_by_date(test_data) == test_data


def test_filter_by_state_empty() -> None:
    """Тест фильтрации с пустым значением state"""
    assert filter_by_state(SAMPLE_DATA, "") == []


def test_filter_by_state_unknown() -> None:
    """Тест фильтрации с несуществующим значением state"""
    assert filter_by_state(SAMPLE_DATA, "UNKNOWN") == []
