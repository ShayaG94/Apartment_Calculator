from datetime import date, timedelta
import os


def count_days(first_date: date, last_date: date) -> int:
    """Calculates amount of days between 2 dates.

    Takes 2 dates and calculates the duration of the perioud between them.
    Including the last day.

    Args:
        first_date (date): First date of perioud. Must be of type datetime.date.
        last_date (date): Last date of the perioud. Must be of type datetime.date.

    Returns:
        int: Amount of days between the dates.
    """

    return (last_date - first_date).days + 1


def parse_date(date_str: str) -> date:
    """Creates a date type object out of a str.

    Can take strings in the following formats:
        D/M/YY | DD/MM/YY | DD/MM/YYYY |
        D.M.YY | DD.MM.YY | DD.MM.YYYY

    Args:
        date_str (str): A string representing a date.

    Returns:
        date: A datetime.date object.
    """

    date_list = date_str.replace("/", ".").split(".")
    # If year isn't fool, add "20" to the string
    if len(date_list[2]) == 2:
        date_list[2] = f"20{date_list[2]}"
    date_list = [int(num) for num in date_list]
    # datetime.date method accepts date in YYYY,MM,DD format.
    date_list.reverse()
    return date(*date_list)


def get_date_key(dictionary: dict) -> str:
    """Retrieves the key of a date item in a dictionary.

    Args:
        dictionary (dict): A dictionary that contains a date item.

    Returns:
        str: Key of a date item.
    """
    # Make a list out of dict.keys() object
    # Filter said list by searching "date" in each item.
    # Make a list out of the created iterator.
    # Take first item in the list (Should be the only one).
    return list(filter(lambda k: "date" in k, list(dictionary.keys())))[0]


def get_date_value(dictionary: dict) -> str:
    """Retrieves the value of a date item in a dictionary.

    Args:
        dictionary (dict): A dictionary that contains a date item.

    Returns:
        str: Value of a date item.
    """
    # Make a list out of dict.values() object
    # Filter said list by checking the type of item (datetime.date).
    # Make a list out of the created iterator.
    # Take first item in the list (Should be the only one).
    return list(filter(lambda v: type(v) == date, list(dictionary.values())))[0]


def get_roomates() -> list:
    """Gets the names of roomates in a shared apartment from user input.

    Returns:
        list of dicts: List of dictionaries representing the roomates in an apartment.
            Example: [{"name": "Alice"}, {"name": "Bob"}, {"name": "Charlie"}]
    """

    num_of_roomates = int(input("How many roomates are you? "))
    roomates = []
    for i in range(num_of_roomates):
        roomate = input(f"Roomate {i + 1}: ").capitalize()
        roomates.append({"name": roomate})
    return roomates


def update_vacators(roomates: list) -> list:
    """Updates the roomates' dictionaries regrading vacationing time.

    Adds a "vacated" item to a dict, showing whether the roomate was on vacation during a given perioud.
    Values are True | False, accordingly.

    Args:
        roomates (list of dicts): List of roomates dictionaries.

    Returns:
        list of dicts: Updated list of dictionaries.
    """

    # Iterate of list of dicts:
    for roomate in roomates:
        reply = input(f"Did {roomate['name']} go on vacation during the bill? (Y/N): ")
        # Add to dict a "vacated" item using ".update()":
        if reply.upper() == "Y":
            roomate.update({"vacated": True})
        else:
            roomate.update({"vacated": False})

    return roomates


def get_num_vacations(vacating_roomate: str) -> int:
    """Get's num of vacations of roomate from user input.

    Args:
        vacating_roomate (str): Roomate's name.

    Returns:
        int: Number of vacations roomate went on.
    """

    return int(input(f"On how many vacations did {vacating_roomate} go? "))


def get_vacation_dates(vacating_roomate: str) -> list:
    """Get vacation dates of roomate from user input.

    Args:
        vacating_roomate (str): Roomate's name.

    Returns:
        list of dicts: List with 2 dicts:
            1) First date of vacation.
            2) Last date of vacation.
    """

    print(f"When was {vacating_roomate} on vacation?")
    first_date = input("First date: ")
    last_date = input("Last date: ")
    return [
        {"first_date": parse_date(first_date)},
        {"last_date": parse_date(last_date)},
    ]


def construct_vacations_list(roomates: list) -> list:
    """Create a list of dates of vacations.

    Args:
        roomates (list of dicts): List of roomates dictionaries.

    Returns:
        list of dicts: Updated list of dictionaries.
    """

    for roomate in roomates:
        vacations_list = []
        # Check if roomate was vacationing:
        if roomate["vacated"]:
            name = roomate["name"]
            num_of_vacations = get_num_vacations(roomate["name"])

            for vacation in range(num_of_vacations):
                vacation_dates = get_vacation_dates(name)
                # Add vacation dates to vacations list:
                vacations_list.extend(vacation_dates)
        # Update roomate's dict with vacations list:
        roomate.update({"vacations_dates": vacations_list})

    return roomates


def get_bill_info() -> dict:
    """Get info of a utility bill from user input.

    Asks for name, dates and sum.

    Returns:
        dict: A dictionary representing information of a bill.
    """

    bill_name = input("Bill name: ").capitalize()
    first_date = parse_date(input("Bill's First Date: "))
    last_date = parse_date(input("Bill's Last Date: "))
    bill_sum = round(float(input("Bill sum: ")), 2)
    bill_dict = {
        "bill": bill_name,
        "bill_dates": [{"bill_first_date": first_date}, {"bill_last_date": last_date}],
        "sum": bill_sum,
    }
    return bill_dict


def sort_dates(bill_dates: list, vacations_dates: list) -> list:
    """Sorts list of date dictionaries. Ealiest to latest.

    Args:
        bill_dates (list of dicts): Dates of a bill.
        vacations_dates (list of dicts): Dates of vacations.

    Returns:
        list of dicts: A sorted list of date dictionaries
    """

    # Create a single list of all dates:
    vacations_dates.extend(bill_dates)
    # Sort dictionaries by the values:
    vacations_dates.sort(key=lambda d: get_date_value(d))
    return vacations_dates


def combine_dates(bill_info: dict, roomates: list) -> list:
    """Create a single sorted list of dates.

    Args:
        bill_info (dict): Dictionary representing a bill.
        roomates (list of dicts): List of roomates dictionaries.

    Returns:
        list: Updated list of dictionaries.
    """
    # Extract bill's dates:
    bill_dates = bill_info["bill_dates"]
    # Iterate over list of roomates dicts:
    for roomate in roomates:
        # Extract vacations dates of roomate:
        vacations_dates = roomate["vacations_dates"]
        # Combine and sort upper mentioned lists of dates:
        all_dates = sort_dates(bill_dates, vacations_dates)
        # Update roomate's dict with sorted list:
        roomate.update({"all_dates": all_dates})
        # Remove from roomate's dictionary vacations list (no longer needed):
        roomate.pop("vacations_dates", None)
    return roomates


def calculate_presense(roomates: list) -> list:
    """Calculate the amount of days each roomate was present during bill.

    Args:
        roomates (list of dicts): List of roomates dictionaries.

    Returns:
        list of dicts: Updated list of roomates dictionaries.
    """

    # Iterate over roomates dicts:
    for roomate in roomates:
        # Set logging to False:
        logging = False
        # Set presence to True:
        present = True
        # Initiate presence counter
        days_present = 0
        # Extract sorted list of bill and vacations dates
        dates = roomate["all_dates"]

        # Iterate over list of dates:
        for i in range(len(dates)):
            # Set current date:
            current_date = dates[i]

            # If didn't get to the end of the list:
            if i + 1 < len(dates):
                # Then set the next date:
                next_date = dates[i + 1]
            else:
                # Otherwise, continue (get's out of loop)
                continue

            # Extract keys of current and next date:
            current_date_key = get_date_key(current_date)
            next_date_key = get_date_key(next_date)

            # Set logging to True if reached bill's first date:
            if current_date_key == "bill_first_date":
                logging = True
            # Set logging to False if reached bill's last date:
            if current_date_key == "bill_last_date":
                logging = False

            # Set presence to False if reached first date of a vacation:
            if current_date_key == "first_date":
                present = False
            # Set presence to True if reached last date of a vacation:
            if current_date_key == "last_date":
                present = True

            # If reached first date of bill and roomate is present (not on vacation):
            if logging and present:
                # Extract values of current and next date.
                # Assign to first & last date of a period
                first_date = get_date_value(current_date)
                last_date = get_date_value(next_date)

                # If current date is last date of a vacation
                if current_date_key == "last_date":
                    # Increase the first date of the period by 1
                    # Since the last date of a vacation isn't taken in account:
                    first_date += timedelta(days=1)

                # If next date is first date of a vacation
                if next_date_key == "first_date":
                    # Decrease the last date of the period by 1
                    # Since the first date of a vacation isn't taken in account:
                    last_date -= timedelta(days=1)

                # Count days of presence and add to counter:
                days_present += count_days(first_date, last_date)

        # Update roomate's dict:
        roomate.update({"days_present": days_present})
    return roomates


def calculate_part_of_bill(roomates: list, bill_info: dict) -> list:
    """Calculates each roomate's part of the bill, according to presence.

    Args:
        roomates (list of dicts): List of roomates dictionaries.
        bill_info (dict): Dictionary representing a bill.

    Returns:
        list of dicts: Updated list of dictionaries.
    """

    # Extract sum to pay of the bill:
    bill_sum = bill_info["sum"]
    # Sum of all roomates' presence:
    total_presence = sum([roomate["days_present"] for roomate in roomates])
    # Calculate cost of day-person:
    day_person_cost = bill_sum / total_presence
    # Iterate of list of roomates:
    for roomate in roomates:
        # Calculate each roomate's part of the bill according to presence:
        part_of_bill = round(day_person_cost * roomate["days_present"], 2)
        # Update dict of roomate with amount:
        roomate.update({"part_of_bill": part_of_bill})


def print_results(roomates: list):
    """Prints out result of the calcualtor.

    Args:
        roomates (list of dicts): List of roomates dictionaries.
    """

    # Print using list comprehension. Add NIS symbol to string.
    [
        print(f"{roomate['name']}: {roomate['part_of_bill']}\u20AA")
        for roomate in roomates
    ]


def print_terminal_header(message: str, symbol: str = "=") -> None:
    """Create a nice header in terminal.

    Args:
        message (str): Header to be printed
        symbol (str, optional): Symbol for filling. Defaults to "=".
    """
    os.system("cls")
    terminal = os.get_terminal_size()
    size = (terminal.columns - len(message) - 2) // 2
    header = symbol * size
    print(f"\n{header} {message} {header}\n")


if __name__ == "__main__":
    print_terminal_header("Shaya's Apartment Calculater")
    input(
        "Please note, this was made for personal usage, so there's no error catching.\n\
    Please don't try to break it..."
    )
    bill_info = get_bill_info()
    roomates = get_roomates()
    update_vacators(roomates)
    construct_vacations_list(roomates)
    combine_dates(bill_info, roomates)
    calculate_presense(roomates)
    calculate_part_of_bill(roomates, bill_info)
    print_results(roomates)
