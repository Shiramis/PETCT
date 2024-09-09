from math import exp, log
from datetime import datetime
import pandas as pd


def calculate_remaining_fdg(initial_fdg_mbq, elapsed_time_minutes, half_life_minutes):
    """
    Calculate the remaining FDG activity after a given elapsed time.

    Parameters:
    initial_fdg_mbq (float): The initial FDG activity in MBq.
    elapsed_time_minutes (float): The elapsed time in minutes.
    half_life_minutes (float): The half-life of FDG in minutes.

    Returns:
    float: The remaining FDG activity in MBq.
    """
    decay_constant = log(2) / half_life_minutes
    remaining_fdg = initial_fdg_mbq * exp(-decay_constant * elapsed_time_minutes)
    return remaining_fdg


# Example usage with input validation
try:
    fdg_half_life_minutes = 110  # Example half-life for FDG

    initial_fdg_mbq = float(input("Enter the initial FDG activity in MBq: "))
    initial_time = input("Enter the initial time (HH:MM): ")
    current_time = input("Enter the current time (HH:MM): ")

    elapsed_time = (datetime.strptime(current_time, "%H:%M") - datetime.strptime(initial_time,
                                                                                 "%H:%M")).total_seconds() / 60  # convert to minutes

    remaining_fdg = calculate_remaining_fdg(initial_fdg_mbq, elapsed_time, fdg_half_life_minutes)

    print(f"The remaining FDG activity is {remaining_fdg:.2f} MBq.")

    # Prepare the data for saving
    data = {"Initial FDG Activity (MBq)": [initial_fdg_mbq], "Remaining FDG Activity (MBq)": [remaining_fdg],
        "Initial Time": [initial_time], "Current Time": [current_time]}

    # Convert to a DataFrame
    df = pd.DataFrame(data)

    # Save to Excel file
    file_name = "fdg_activity_data.xlsx"
    df.to_excel(file_name, index=False)
    print(f"Data saved to {file_name}.")

except ValueError as e:
    print(e)
except Exception as e:
    print(f"An error occurred: {e}")
