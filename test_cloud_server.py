import pytest
from pymodm import connect, MongoModel, fields
from cloud_server import NewPatient
from setup_test_db import init_test_db

init_test_db()


@pytest.mark.parametrize('info, expected',
                         [([1000, "Canyon", [70], ['2020-6-23 1:34:20'],
                            ['test string'], ['test string']], 1000),
                          ([2000, "Aidan", [65], ['2020-6-23 1:35:20'],
                            ['test string'], ['test string']], 2000)])
def test_add_patient_to_db(info, expected):
    from cloud_server import add_patient_to_db
    answer = add_patient_to_db(info)
    NewPatient.objects.raw({"_id": info[0]}).first().delete()
    assert answer == expected


@pytest.mark.parametrize('patient_id, expected',
                         [("1000", True),
                          ("2000", True),
                          ("1234", False)])
def test_check_patient_exists(patient_id, expected):
    from cloud_server import check_patient_exists
    answer = check_patient_exists(patient_id)
    assert answer == expected
