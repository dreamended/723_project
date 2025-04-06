import csv

filename = "C:/Users/段/PycharmProjects/723_project/airlines.csv"

# read CSV file and translate.
def load_seat_map(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)   # the first row displays labels, such as A, B, C, X, etc.
        rows = [row for row in reader]  # each row represents a row of seats.
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
    print("Row " + " ".join(header[1:]))    # print column headers (excluding the first blank space)

    for row in rows:
        row_display = f"{row[0]:>3} "

        for seat in row[1:]:
            if seat in ['X', 'S', 'R']:
                row_display += f"{seat} "   # display reserved seats / aisle / storage area.
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

# check if a seat is available
def check_if_seat_is_free(seat_table, column_names):

    seat_code = input("Enter seat like 54F: ").strip()
    position = find_seat_position(seat_code, column_names, seat_table)

    if not position:
        print("That seat code is invalid. Try something like 54F.")
        return

    row_index, col_index = position
    seat_value = seat_table[row_index][col_index]

    if seat_value == "R":
        print(f"Seat {seat_code} is already booked.")
    elif seat_value in ["X", "S"]:
        print(f"Seat {seat_code} is not an actual seat (it's an aisle or storage).")
    else:
        print(f"Seat {seat_code} is free and available.")

# book a seat
def book_seat(rows, header):
    seat = input("Enter seat code to book (e.g. 54F): ").strip()
    pos = find_seat_position(seat, header, rows)
    if not pos:
        print("Invalid seat code.")
        return

    row_index = pos[0]
    col_index = pos[1]

    if rows[row_index][col_index] == "R":
        print("This seat is already booked.This seat is already booked.")
    elif rows[row_index][col_index] in ["X", "S"]:
        print("This seat is not for people to sit on.")
    else:
        rows[row_index][col_index] = "R"
        print(f"Seat {seat} has been successfully booked.")

# release Seat
def free_seat(rows, header):
    seat = input("Enter seat code to release (e.g. 54F): ").strip()
    pos = find_seat_position(seat, header, rows)

    if not pos:
        print("Invalid seat code.")
        return

    row_index = pos[0]
    col_index = pos[1]

    if rows[row_index][col_index] != "R":
        print("This seat hasn't been reserved in advance, so there's no need to release it.")
    else:
        # Restore the original seat code (e.g. 54F)
        seat_code = f"{row_index+1}{header[col_index]}"
        rows[row_index][col_index] = seat_code
        print(f"Seat {seat} has been released.")

# main menu loop
def main():
    filename = "airlines.csv"
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
            print("Thank you")
            break
        else:
            print("You can only enter numbers from 1 to 5. If you enter something else, try again.")

# entry point
if __name__ == "__main__":
    main()
