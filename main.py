import time
import json
import os
import tkinter as tk
from datetime import datetime, timezone, timedelta


class Crane_counter():
    def __init__(self) -> None:
        with open("config.json", "r") as config:
            config_data = json.load(config)
        # print the average cranes folded per what? (hours, minutes, seconds, days)
        self.MEASURE_IN = config_data["measure_in"]
        self.QUICK_ADD_AMOUNT = config_data["quick_add_amount"]
        self.DEFAULT_FONT = ("Consolas", config_data["font_size"])
        self.BG_COLOR = config_data["bg_color"]
        self.FG_COLOR = config_data["fg_color"]

        self.DEFAULT_DATA = {"desired_amount": 1000, "amount_folded": []}

        self.root = tk.Tk()
        self.root.configure(bg=self.BG_COLOR)
        self.root.title("Crane counter")

        self.progress_label = tk.Label(self.root, fg=self.FG_COLOR, bg=self.BG_COLOR, font=self.DEFAULT_FONT)

        self.add_entry = tk.Entry(self.root, fg=self.FG_COLOR, bg=self.BG_COLOR, font=self.DEFAULT_FONT, width=5)
        self.add_button = tk.Button(self.root, fg=self.FG_COLOR, bg=self.BG_COLOR, text="Add!", font=self.DEFAULT_FONT,
                                    width=16, command=lambda: self.logic(self.add_entry.get()))
        self.add_1_button = tk.Button(self.root, fg=self.FG_COLOR, bg=self.BG_COLOR,
                                      text=f"Add {self.QUICK_ADD_AMOUNT}!", font=self.DEFAULT_FONT, width=16, command=lambda: self.logic(str(self.QUICK_ADD_AMOUNT)))
        self.subtract_button = tk.Button(self.root, fg=self.FG_COLOR, bg=self.BG_COLOR, text="Subtract!", font=self.DEFAULT_FONT,
                                         width=16, command=lambda: self.logic(self.add_entry.get()))
        self.subtract_1_button = tk.Button(self.root, fg=self.FG_COLOR, bg=self.BG_COLOR, text=f"Subtract -{self.QUICK_ADD_AMOUNT}!",
                                           font=self.DEFAULT_FONT, width=16, command=lambda: self.logic("-" + str(self.QUICK_ADD_AMOUNT)))

        self.change_date_entry = tk.Entry(self.root, fg=self.FG_COLOR, bg=self.BG_COLOR,
                                          font=self.DEFAULT_FONT, width=16)
        self.change_date_button = tk.Button(self.root, fg=self.FG_COLOR, bg=self.BG_COLOR, font=self.DEFAULT_FONT,
                                            width=16, text="Change!", command=lambda: self.change_date())  # change the date

        self.progress_label.grid(row=0, column=0, columnspan=3)

        self.add_1_button.grid(row=1, column=0, sticky="w")
        self.add_entry.grid(row=1, column=1)
        self.add_button.grid(row=1, column=2, sticky="e")

        self.subtract_1_button.grid(row=2, column=0, sticky="w")
        self.subtract_button.grid(row=2, column=2, sticky="e")

        self.change_date_entry.grid(row=3, column=0, sticky="w")
        self.change_date_button.grid(row=3, column=2, sticky="e")

        self.root.mainloop()

    def logic(self, ans):
        if ans.lstrip("+-").isdigit() or ans == "clear":
            if (ans != "clear" and int(ans) != 0) or ans == "clear":
                self.write_to_json(ans)
                if ans != "clear":
                    self.calculate_average()
                return
        print("Invalid input")

    def change_date(self):
        new_date_raw = self.change_date_entry.get()
        year = int(new_date_raw[0:4])
        month = int(new_date_raw[5:7])
        day = int(new_date_raw[8:10])
        hour = int(new_date_raw[11:13])
        minute = int(new_date_raw[14:])

        hungary_tz = timezone(timedelta(hours=1))  # CET (UTC+1) without daylight saving time

        # Check if the date falls within daylight saving time
        dst_start = datetime(year, 3, 25, 2, tzinfo=hungary_tz)
        dst_end = datetime(year, 10, 28, 3, tzinfo=hungary_tz)

        current_datetime = datetime(year, month, day, hour, minute, tzinfo=hungary_tz)

        if dst_start <= current_datetime < dst_end:
            hungary_tz = timezone(timedelta(hours=2))  # CEST (UTC+2) during daylight saving time

        specific_date = datetime(year, month, day, hour, minute, tzinfo=hungary_tz)
        epoch = datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc)

        # Calculate the difference between the specific date and the epoch
        time_difference = specific_date - epoch

        # Extract the total seconds from the time difference
        seconds = int(time_difference.total_seconds())

        with open("data.json", "r") as file:
            data = json.load(file)

        # bool that becomes true if the desired time is before the latest time, and the integer is the index of the first or the last item in "amount folded"
        if seconds < data["amount_folded"][1][0]:
            data["amount_folded"][0][0] = seconds
        else:
            self.progress_label["text"] += "\nDate entered is too high!"

        with open("data.json", "w") as file:
            file.write(json.dumps(data))
        self.calculate_average()

    def write_to_json(self, amount):
        self.add_entry.delete(0, "end")
        if amount != "clear":
            amount = int(amount)
        with open("data.json", "r") as file:
            data = json.load(file)
        if amount == "clear":
            pass
        elif len(data["amount_folded"]) < 2:
            data["amount_folded"].append((time.time(), amount))
        # Replace the last item of the list with the latest "crane folding" and add together the "old" cranes folded amount and the "new" cranes folded amount
        else:
            data["amount_folded"][1] = (time.time(), amount + data["amount_folded"][1][1])
        with open("data.json", "w") as file:
            if amount == "clear":
                file.write(json.dumps(self.DEFAULT_DATA))
                self.progress_label["text"] = "Cleared!"
            else:
                file.write(json.dumps(data))

    def calculate_average(self):
        with open("data.json", "r") as file:
            data = json.load(file)
        total_folded = 0
        for i in data["amount_folded"]:
            total_folded += i[1]
        if len(data["amount_folded"]) > 1:
            time_difference = int(data["amount_folded"][-1][0]) - int(data["amount_folded"][0][0])
            if self.MEASURE_IN == "day":
                time_difference = time_difference / 60 / 60 / 24
            elif self.MEASURE_IN == "hour":
                time_difference = time_difference / 60 / 60
            elif self.MEASURE_IN == "minute":
                time_difference = time_difference / 60

            # These are here so if total folded is 0 it will become 1, but when printing, it will remain 0
            average = (1 if total_folded == 0 else total_folded) / time_difference
        else:
            average = (1 if total_folded == 0 else total_folded)
        remaining_time = (data["desired_amount"] - total_folded)/average
        text = f"The average crane folding speed is {round(average, 2)} cranes/{self.MEASURE_IN}.\nYou'll get to your goal in {round(remaining_time, 2)} {self.MEASURE_IN}(s)\nYou need to make {data['desired_amount'] - total_folded} more"
        self.progress_label["text"] = text


if __name__ == "__main__":
    os.chdir(__file__.rstrip("main.py"))
    app = Crane_counter()
