import pyodbc
import people.passenger
import run


class DbWrapper:

    # Opens a file called server_info.cfg and pulls connection info from there
    def __init__(self):
        file_lines = open("server_info.cfg", "r").readlines()
        self.ip = file_lines[0].strip("\n")
        self.uname = file_lines[1].strip("\n")
        self.password = file_lines[2].strip("\n")
        self.DbName = file_lines[3].strip("\n")

        self.connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};' +
                                         f'SERVER={self.ip};DATABASE={self.DbName};'
                                         f'UID={self.uname};PWD={self.password}')

        self.cursor = self.connection.cursor()

    # Will be used to pull information from the database
    def load_fresh_from_db(self):
        run.list_passengers = []
        run.list_flights = []
        self.cursor.execute("SELECT * FROM passengers")
        temp_passenger_list = self.cursor.fetchall()
        for passenger in temp_passenger_list:
            passenger

    # Will be used to store information in the database
    def save_to_db(self, table, passenger_list, flights_list, primary_key=0):
        for passenger in passenger_list:
            if passenger.first_name is not None:
                first_name = passenger.first_name
                last_name = passenger.last_name
                tax_number = passenger.tax_number
                passport_number = passenger.passport_number

                self.cursor.execute(
                    f"INSERT INTO {table} ('first_name', 'last_name', 'tax_number', 'passport_number')"
                    + f"VALUES ({first_name}, {last_name}, {tax_number}, {passport_number});")


if __name__ == "__main__":
    db = DbWrapper()
    db.load_fresh_from_db()