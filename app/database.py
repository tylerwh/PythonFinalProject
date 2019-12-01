import csv
import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS list (id INTEGER PRIMARY KEY, store text, item text, price text)")
        self.conn.commit()

    
    def fetch(self):
        self.cur.execute("SELECT * FROM list")
        rows = self.cur.fetchall()
        return rows

    
    def insert(self, store, item, price):
        self.cur.execute(
            "INSERT INTO list VALUES (NULL, ?, ?, ?)", (store, item, price))
        self.conn.commit()

    
    def remove(self, id):
        self.cur.execute("DELETE FROM list WHERE id=?", (id,))
        self.conn.commit()

    
    def update(self, id, store, item, price):
        self.cur.execute(
            "UPDATE list SET store = ?, item = ?, price = ? WHERE id = ?", (store, item, price, id))
        self.conn.commit()

    
    def drop_table(self):
        self.cur.execute("DROP TABLE IF EXISTS list")
        self.conn.commit()
    
    
    def export_list_to_csv(self):
        print("Exporting data into CSV............")

        with open('current_list.csv', 'w+') as write_file:
            # Create csv_writer and set delimiter for each row
            csv_writer = csv.writer(write_file, delimiter='\t')

            # Iterate through each row in result query
            for row in self.cur.execute('SELECT store, item, price FROM list'):
                # csv_writer.writerow([i[0] for i in self.cur.description]) # This provides a description/header of each column
                csv_writer.writerows(self.cur)

            # Prints out the tuples without formatting
            # for row in self.cur.execute('SELECT * FROM list'):
                # write_file.write(str(row))
        print("Finished exporting")

    
    def __del__(self):
        self.conn.close()


# Below was used to test functionality
# db = Database('list.db')
# db.insert("Target", "Beard Balm", "15")
# db.insert("Target", "Mustache Wax", "20")
# db.insert("Target", "Beard Trimmer", "80")
# db.insert("Walmart", "Bacon", "6")
# db.insert("Walmart", "Ground Beef", "8")
# db.insert("Walmart", "Steak", "10")
# db.insert("Walmart", "Eggs", "1")
# for data in db.fetch():
#   print(str(data))
# db.update(3, "Target", "Beard Trimmer", "80")
# db.update(5, "Walmart", "Ground Beef", "8")
# db.update(6, "Walmart", "Steak", "10")
# db.update(7, "Walmart", "Eggs", "1")
# db.remove(7)
