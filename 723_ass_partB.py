import csv
import sqlite3
import random

filename = "C:/Users/段/PycharmProjects/723_project/airlines.csv"

# connect database
conn = sqlite3.connect("airlines.db")
cursor = conn.cursor()

# create the bookings table for storing user booking information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        booking_ref TEXT PRIMARY KEY,
        passport TEXT,
        first_name TEXT,
        last_name TEXT,
        seat_row INTEGER,
        seat_col TEXT
    )
''')
conn.commit()

# generates an 8-digit reference number
def generate_booking_reference():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # lowercase letters not included
    while True:
        ref = ""
        for _ in range(8):
            ref += random.choice(chars)
        # check that the reference number is not unique
        cursor.execute("SELECT 1 FROM bookings WHERE booking_ref = ?", (ref,))
        if not cursor.fetchone():
            return ref

# read CSV file and translate.
def load_seat_map(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]
    return header, rows

# save the current seat map back into the CSV file
def save_seat_map(filename, header, rows):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

# display the current seat status visually in the terminal
def display_seat_map(header, rows):
    print("\nCurrent seat status:")
    print("Row " + " ".join(header[1:]))
    for row in rows:
        row_display = f"{row[0]:>3} "
        for seat in row[1:]:
            if seat in ['X', 'S']:  # walkway or storage area
                row_display += f"{seat} "
            elif len(seat) == 8:    # if it is occupied by a reference number, it is considered to be booked
                row_display += "* "
            else:
                row_display += "F "
        print(row_display)
    print()

# convert seat code (like "43B") into matrix index position (row, column)
def find_seat_position(seat_input, column_names, seat_table):
    if len(seat_input) < 2:
        return None

    row_part = seat_input[:-1]
    col_letter = seat_input[-1].upper()

    if not row_part.isdigit():
        return None
    row_number = int(row_part)

    if row_number < 1 or row_number > len(seat_table):
        return None
    if col_letter not in column_names:
        return None

    row_index = row_number - 1
    col_index = column_names.index(col_letter)
    return row_index, col_index

# only an 8-digit reference number is considered booked
def check_if_seat_is_free(seat_table, column_names):
    seat_code = input("Enter seat like 54F: ").strip()
    position = find_seat_position(seat_code, column_names, seat_table)

    if not position:
        print("That seat code is invalid. Try something like 54F.")
        return

    row_index, col_index = position
    seat_value = seat_table[row_index][col_index]

    if seat_value in ["X", "S"]:
        print(f"Seat {seat_code} is not an actual seat (it's an aisle or storage).")
    elif len(seat_value) == 8:
        print(f"Seat {seat_code} is already booked.")
    else:
        print(f"Seat {seat_code} is free and available.")

# check whether a seat is available
def book_seat(rows, header):
    seat = input("Enter seat code to book (e.g. 54F): ").strip()
    pos = find_seat_position(seat, header, rows)
    if not pos:
        print("Invalid seat code.")
        return

    row_index, col_index = pos
    current_value = rows[row_index][col_index]

    if len(current_value) == 8:     # the reference number has been used
        print("This seat is already booked.")
        return
    if current_value in ["X", "S"]:
        print("This seat is not for people to sit on.")
        return

    # enter passenger information
    passport = input("Enter passport number: ").strip()
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    booking_ref = generate_booking_reference()

    #update the seating map
    rows[row_index][col_index] = booking_ref

    # record passenger data into a database
    cursor.execute('''
        INSERT INTO bookings (booking_ref, passport, first_name, last_name, seat_row, seat_col)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (booking_ref, passport, first_name, last_name, row_index + 1, header[col_index]))
    conn.commit()

    print(f"Seat {seat} has been successfully booked.")
    print(f"Booking Reference: {booking_ref}")

# release seat
def free_seat(rows, header):
    seat = input("Enter seat code to release (e.g. 54F): ").strip()
    pos = find_seat_position(seat, header, rows)
    if not pos:
        print("Invalid seat code.")
        return

    row_index, col_index = pos
    current_value = rows[row_index][col_index]

    if current_value in ["F", "X", "S"] or len(current_value) != 8:
        print("This seat hasn't been reserved in advance.")
        return

    # delete the user's information from the database
    cursor.execute("DELETE FROM bookings WHERE booking_ref = ?", (current_value,))
    conn.commit()

    rows[row_index][col_index] = f"{row_index + 1}{header[col_index]}"
    print(f"Seat {seat} has been released.")

# main interface
def main():
    header, rows = load_seat_map(filename)

    while True:
        print("\n--- Apache Airlines Seat Booking System ---")
        print("1. Check seat availability")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Display seat map")
        print("5. Exit")

        choice = input("Select an option (1-5): ")
        if choice == "1":
            check_if_seat_is_free(rows, header)
        elif choice == "2":
            book_seat(rows, header)
            save_seat_map(filename, header, rows)
        elif choice == "3":
            free_seat(rows, header)
            save_seat_map(filename, header, rows)
        elif choice == "4":
            display_seat_map(header, rows)
        elif choice == "5":
            print("Thank you!")
            conn.close()
            break
        else:
            print("Invalid input. Please select a number between 1 and 5.")

if __name__ == "__main__":
    main()
