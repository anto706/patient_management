
from mysql import connector


class DbConnect:

    def get_connection(self):
        try:
            self.connection = connector.connect(
                host="localhost",
                user="root",
                password="root123#",
                database="hospital_db"
            )
            return self.connection

        except Exception as e:
            print(e)
            return None


class PatientManager(DbConnect):

    def get_object(self, id=None):
        try:
            self.connect = super().get_connection()
            self.cursor = self.connect.cursor()

            query = "SELECT * FROM patient WHERE id=%s"
            values = (id,)

            self.cursor.execute(query, values)

            records = self.cursor.fetchone()

            return records

        except Exception as e:
            print(e)

    def get(self):
        try:
            self.connect = super().get_connection()
            self.cursor = self.connect.cursor()

            query = "SELECT * FROM patient"
            self.cursor.execute(query)

            records = self.cursor.fetchall()
            return records

        except Exception as e:
            print(e)
            return []

    def post(self, **kwargs):
        try:
            self.connect = super().get_connection()
            self.cursor = self.connect.cursor()

            query = """
            INSERT INTO patient
            (name, age, gender, phone, disease)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = [kwargs.get(k) for k in
                      ["name", "age", "gender", "phone", "disease"]]

            self.cursor.execute(query, values)

            self.connect.commit()

            print("New patient added successfully")

        except Exception as e:
            print(e)


    def retrieve(self, id=None):
        try:
            record = self.get_object(id=id)

            if record is None:
                print("Patient not found")
            else:
                print(record)

        except Exception as e:
            print(e)


    def delete(self, id=None):
        try:
            record = self.get_object(id=id)

            if record is not None:

                query = "DELETE FROM patient WHERE id=%s"
                values = (id,)

                self.cursor.execute(query, values)

                self.connect.commit()

                print("Patient deleted successfully")

            else:
                print("Patient not found")

        except Exception as e:
            print(e)


    def put(self, id=None, **kwargs):
        try:
            record = self.get_object(id=id)

            if record is not None:

                allowed_fields = ["name", "age", "gender", "phone", "disease"]

                if not kwargs or not all(k in allowed_fields for k in kwargs):
                    print("Invalid or empty update fields")
                    return

                placeholder = ""

                for k in kwargs.keys():
                    placeholder += k + "=%s,"

                placeholder = placeholder.rstrip(",")

                query = f"UPDATE patient SET {placeholder} WHERE id=%s"

                values = list(kwargs.values())
                values.append(id)

                self.cursor.execute(query, values)

                self.connect.commit()

                print("Patient updated successfully")

            else:
                print("Patient not found")

        except Exception as e:
            print(e)


# Object creation
patient_instance = PatientManager()

# POST
# patient_instance.post(
#     name="Anto",
#     age=21,
#     gender="Male",
#     phone="9876543210",
#     disease="Fever"
# )

# GET
patient_instance.get()

# RETRIEVE
# patient_instance.retrieve(1)

# PUT
# patient_instance.put(1, name="Anto George", disease="Cold")

# DELETE
# patient_instance.delete(1)
