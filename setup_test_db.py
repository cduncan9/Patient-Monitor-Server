from pymodm import connect, MongoModel, fields


class NewPatient(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    patient_name = fields.CharField()
    heart_rate = fields.ListField()
    timestamp = fields.ListField()
    ecg_images = fields.ListField()
    medical_images = fields.ListField()


def add_to_db_test():
    patient_test = NewPatient(patient_id=1000,
                              patient_name="Canyon",
                              heart_rate=[70],
                              timestamp=['2020-6-23 1:34:20'],
                              ecg_images=['test string'],
                              medical_images=['test string'])
    patient_test1 = NewPatient(patient_id=2000,
                               patient_name="Aidan",
                               heart_rate=[70],
                               timestamp=['2020-6-23 1:35:20'],
                               ecg_images=['test string'],
                               medical_images=['test string'])
    save_patient_test1 = patient_test1.save()
    save_patient_test = patient_test.save()
    print(save_patient_test)
    print(save_patient_test1)


def init_test_db():
    print("Connecting to database...")
    connect("mongodb+srv://cduncan9:BME547@cluster0.conjj.mongodb.net/"
            "testdatabase?retryWrites=true&w=majority")
    print("Database connected.")


if __name__ == '__main__':
    init_test_db()
    add_to_db_test()
