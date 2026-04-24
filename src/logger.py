# ------------------------------------------------------------
# Student Name       : Kiran Manikandan
# Student ID         : 24062131
# University         : University of Hertfordshire
# Description        : Log application errors t seperate module log file
# Last Modifide Date : 24-04-2026

# Copyright (c) 2026 Kiran Manikandan
# ------------------------------------------------------------

import datetime
import traceback

def exception_handler(error, file_name):
    with open(f"./error_logs/{file_name}.txt", "a") as file:
        file.write("\n-----------------------------\n")
        file.write(f"Time: {datetime.datetime.now()}\n")
        file.write(f"Error: {str(error)}\n")
        file.write("Trace:\n")
        file.write(traceback.format_exc())
        file.write("\n-----------------------------\n")