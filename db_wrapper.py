import pyodbc
from people.passenger import Passenger
from flight_trip import FlightTrip
from aircraft.aircraft import Aircraft


class DbWrapper:

    # Opens a file called server_info.cfg and pulls connection info from there
    def __init__(self):
        try:
            file_lines = open("server_info.cfg", "r").readlines()
            self.ip = file_lines[0].strip("\n")
            self.uname = file_lines[1].strip("\n")
            self.password = file_lines[2].strip("\n")
            self.db_name = file_lines[3].strip("\n")

            self.connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};' +
                                             f'SERVER={self.ip};DATABASE={self.db_name};'
                                             f'UID={self.uname};PWD={self.password}')

            self.cursor = self.connection.cursor()
        except FileNotFoundError as err:
            print(err)
            print(f"server_info.config not found!")
            exit(1)

    """ Passenger Functions"""
    # Will be used to pull information from the database
    def load_all_passengers(self):
        dict_passengers = {}
        self.cursor.execute("SELECT * FROM passengers")
        temp_passenger_list = self.cursor.fetchall()

    # Generate passenger objects
        for val in temp_passenger_list:
            passenger = Passenger()
            passenger.make_from_db(val[0], val[1], val[2], val[3], val[4])
            dict_passengers[val[0]] = passenger

        return dict_passengers

    """ Flight functions """
    # Get all passengers on a flight using flight_order
    def get_flight_passengers(self, flight_id, passenger_list):
        self.cursor.execute(f"SELECT passenger_id FROM flight_order WHERE flight_id = {flight_id}")
        flight_passengers = []
        for entry in self.cursor.fetchall():
            flight_passengers.append(passenger_list[entry[0]])

        return flight_passengers

    # Load all FlightTrip objects
    def load_all_flights(self, passenger_dict):
        flight_dict = {}
        self.cursor.execute("SELECT * FROM flight_trip")
        temp_flight_list = self.cursor.fetchall()
        for val in temp_flight_list:
            flight = FlightTrip()
            flight.make_from_db(val[0], val[1], val[2], val[3], val[4], val[5], self.get_flight_passengers(val[0], passenger_dict))
            flight_dict[val[0]] = flight

        return flight_dict

    # add a single flight order to the flight_order table
    def add_single_flight_order(self, passenger, flight):
        self.cursor.execute(f"INSERT INTO flight_orders VALUES ({passenger.pid}, {flight.flight_id})")
        self.connection.commit()

    def load_all_aircraft(self):
        dict_aircraft = {}
        self.cursor.execute("SELECT * FROM aircraft")
        temp_passenger_list = self.cursor.fetchall()

        # Generate passenger objects
        for val in temp_passenger_list:
            aircraft = Aircraft()
            aircraft.make_from_db(val[0], val[1], val[2])
            dict_aircraft[val[0]] = aircraft

        return dict_aircraft

if __name__ == "__main__":
    db = DbWrapper()
    psg = db.load_all_passengers()
    db.load_all_flights(psg)
