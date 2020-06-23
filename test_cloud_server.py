import pytest
from pymodm import connect, MongoModel, fields
from cloud_server import NewPatient
from setup_test_db import init_test_db

init_test_db()


@pytest.mark.parametrize('patient_id, expected',
                         [("1000", True),
                          ("2000", True),
                          ("1234", False)])
def test_check_patient_exists(patient_id, expected):
    from cloud_server import check_patient_exists
    answer = check_patient_exists(patient_id)
    assert answer == expected


@pytest.mark.parametrize('patient_id, expected',
                         [("1000", True),
                          ("2000", True),
                          ("1234", False)])
def test_check_patient_exists(patient_id, expected):
    from cloud_server import check_patient_exists
    answer = check_patient_exists(patient_id)
    assert answer == expected
