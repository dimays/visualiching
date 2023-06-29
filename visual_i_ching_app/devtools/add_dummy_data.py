import os
import csv
import sqlite3
from visual_i_ching_app.models import User, UserCreditHistory, UserDetail, UserPayment, Reading


class TableData:
    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath
        self.table_name = self.get_table_name()
        self.columns = self.get_columns()
        self.insert_stmt = self.construct_insert_stmt()

    def get_table_name(self):
        return self.csv_filepath.split("/")[-1].split(".")[0]

    def get_columns(self):
        with open(self.csv_filepath, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            columns = csv_reader.fieldnames
        return columns

    def construct_insert_stmt(self):
        stmt = f"INSERT INTO {self.table_name} ("        
        for column in self.columns[:-1]:
            stmt += f"{column}, "        
        stmt += f"{self.columns[-1]}) VALUES ("
        for i in range(len(self.columns) - 1):
            stmt += "?, "        
        stmt += "?)"
        return stmt


def get_absolute_filepath(filepath):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(this_dir, filepath)

def bulk_insert_from_csv(filepath):
    abs_filepath = get_absolute_filepath(filepath)
    db_path = get_absolute_filepath('../../db.sqlite3')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    table_data = TableData(abs_filepath)

    with open(get_absolute_filepath(abs_filepath), 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            values = ()
            for col in table_data.columns:
                value = row[col]
                values = values + (value,)
            
            cursor.execute(table_data.insert_stmt, values)
        
    conn.commit()
    conn.close()
    return

def insert_core_data():
    data_files = os.listdir(get_absolute_filepath('bin/db'))
    for file in data_files:
        filepath = get_absolute_filepath(f'bin/db/{file}')
        bulk_insert_from_csv(filepath)
    return

def insert_dummy_users():
    pass

def insert_dummy_payments():
    pass

def insert_dummy_credit_histories():
    pass

def insert_dummy_readings():
    pass

def insert_dummy_data():
    insert_dummy_users()
    insert_dummy_payments()
    insert_dummy_credit_histories()
    insert_dummy_readings()
    return

def main():
    insert_core_data()
    insert_dummy_data()
    return


if __name__ == '__main__':
    main()