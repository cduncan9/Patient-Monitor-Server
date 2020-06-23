import pytest
from pymodm import connect, MongoModel, fields



@pytest.mark.parametrize('patient_id, expected',
                         [("1000", True),
                          ("2000", True),
                          ("1234", False)])
def test_check_patient_exists(patient_id, expected):
    from cloud_server import check_patient_exists
    answer = check_patient_exists(patient_id)
    assert answer == expected


if __name__ == '__main__':
    init_test_db()
