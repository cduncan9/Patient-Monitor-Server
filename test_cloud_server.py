import pytest
from pymodm import connect, MongoModel, fields
from cloud_server import NewPatient
from cloud_server import init_db

init_db()


@pytest.mark.parametrize('info, expected',
                         [([1000, "Canyon", [70], ['2020-6-23 1:34:20'],
                            ['test string'], ['test string']], 1000),
                          ([2000, "Aidan", [65], ['2020-6-21 1:35:20',
                                                  '2020-6-22 1:35:20',
                                                  '2020-6-23 1:35:20'],
                            ['test string 1', 'test string 2',
                             'test string 3'],
                            ['test string']], 2000),
                          ([4000, "Johnathan", [55], ['2020-6-23 1:24:20'],
                            ['test string'], ['test string']], 4000)])
def test_add_patient_to_db(info, expected):
    from cloud_server import add_patient_to_db
    answer = add_patient_to_db(info)
    assert answer == expected


@pytest.mark.parametrize('patient_id, expected',
                         [(1000, True),
                          (2000, True),
                          (3000, False)])
def test_check_patient_exists(patient_id, expected):
    from cloud_server import check_patient_exists
    from cloud_server import add_patient_to_db
    answer = check_patient_exists(patient_id)
    assert answer == expected


@pytest.mark.parametrize('expected',
                         [[1000, 2000, 4000]])
def test_get_patient_list(expected):
    from cloud_server import retrieve_patient_id_list
    answer = retrieve_patient_id_list()
    assert answer == expected


@pytest.mark.parametrize("pat_id, expected",
                         [("1", 1),
                          ("50000", 50000),
                          (2, 2),
                          ('chocolate', False)])
def test_verify_patient_id(pat_id, expected):
    from cloud_server import verify_patient_id
    answer = verify_patient_id(pat_id)
    assert answer == expected


@pytest.mark.parametrize("patient_id, expected",
                         [(2000, ['2020-6-21 1:35:20',
                                  '2020-6-22 1:35:20',
                                  '2020-6-23 1:35:20']),
                          (1000, ['2020-6-23 1:34:20'])])
def test_retrieve_timestamps(patient_id, expected):
    from cloud_server import retrieve_timestamps
    answer = retrieve_timestamps(patient_id)
    assert answer == expected


@pytest.mark.parametrize("patient_id, time, expected",
                         [(2000, '2020-6-22 1:35:20',
                           True),
                          (1000, '2020-6-27 1:35:20',
                           False)])
def test_verify_timestamp_exists(patient_id, time, expected):
    from cloud_server import verify_timestamp_exists
    answer = verify_timestamp_exists(patient_id, time)
    assert answer == expected


@pytest.mark.parametrize("patient_id, timestamp, expected",
                         [(1000, '2020-6-23 1:34:20',
                           'test string'),
                          (2000, '2020-6-21 1:35:20',
                           'test string 1')])
def test_get_ecg_string(patient_id, timestamp, expected):
    from cloud_server import get_ecg_string
    answer = get_ecg_string(patient_id, timestamp)
    assert answer == expected


@pytest.mark.parametrize("list_in, expected",
                         [([[2, 1]], [1]),
                          ([[400, 1], [300, 2], [500, 3]], [1, 2, 3]),
                          ([[1, 20], [3, 50], [5, 50]], [20, 50, 50]),
                          ([[1, "hello"]], ["hello"])])
def test_get_ecg_string(list_in, expected):
    from cloud_server import get_file_names
    answer = get_file_names(list_in)
    assert answer == expected


@pytest.mark.parametrize("list_in, key, expected",
                         [([[2, 1]], 1, 2),
                          ([[400, 1], [300, 2], [500, 3]], 2, 300),
                          ([[1, 20], [3, 50], [5, 50]], 20, 1),
                          ([[1, "hello"]], "hello", 1)])
def test_get_ecg_string(list_in, key, expected):
    from cloud_server import find_key
    answer = find_key(list_in, key)
    assert answer == expected


@pytest.mark.parametrize("patient_id, expected",
                         [(1000, [1000, "Canyon", 70, '2020-6-23 1:34:20',
                                  'test string']),
                          (2000, [2000, "Aidan", 65, '2020-6-23 1:35:20',
                                  'test string 3'])])
def test_get_latest_data(patient_id, expected):
    from cloud_server import get_latest_data
    answer = get_latest_data(patient_id)
    assert answer == expected
