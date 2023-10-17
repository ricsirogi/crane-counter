import time
import json


class Crane_counter():
    def __init__(self) -> None:
        pass

    def mainloop(self):
        while True:
            while True:
                ans = input("amount")
                if ans.isdigit():
                    break
            self.calculate_average(int(ans))

    def calculate_average(self, amount):
        data = json.loads("data.json")
        data["amounts_folded"][time.strftime("%Y %m %d %H %M %S")] = amount
        time.strftime("%Y %m %d %H %M %S")


if __name__ == "__main__":
    app = Crane_counter()
    app.mainloop()
