import time
import json
import os
import tkinter as tk


class Crane_counter():
    def __init__(self) -> None:
        self.print_average_per = "minutes"  # print the average cranes folded per what? (hours, minutes, seconds, days)
        self.DEFAULT_DATA = {"desired_amount": 1000, "amount_folded": []}

    def mainloop(self):
        while True:
            while True:
                ans = input("amount: ")
                if ans.isdigit() or ans == "clear":
                    break
                else:
                    print("Invalid input")
            self.write_to_json(ans)
            if ans != "clear":
                self.calculate_average()

    def write_to_json(self, amount):
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
                print("Cleared!")
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
            if self.print_average_per == "day":
                time_difference = time_difference / 60 / 60 / 24
            elif self.print_average_per == "hour":
                time_difference = time_difference / 60 / 60
            elif self.print_average_per == "minute":
                time_difference = time_difference / 60
            average = total_folded/time_difference
        else:
            average = total_folded
        remaining_time = (data["desired_amount"] - total_folded)/average
        print(
            f"The average crane folding speed is {round(average, 2)} cranes/{self.print_average_per}.\nYou'll get to your goal in {round(remaining_time, 2)} {self.print_average_per}(s)\nYou need to make {data['desired_amount'] - total_folded} more")


if __name__ == "__main__":
    os.chdir(__file__.rstrip("main.py"))
    app = Crane_counter()
    app.mainloop()
