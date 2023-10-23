# crane-counter

You can enter the number of paper cranes you've folded today to calculate the your average speed and how many days it will take to reach your desired goal

## Buttons

- **Add/Subtract x!** -> pretty self-explanatory, adds x to the progress (customizable in config.json)
- **Add/Subtract!** -> Adds or subtracts the number entered into the entry in the middle
  - If you type in "clear" and press **Add/Subtract!** then it will clear all the progress
- **Change!** -> If you want to change the starting date for the counting, you can write it in the entry in the last row
  - You need to use YYYY MM DD HH MM format
  - The entry is exactly as long as the date is supposed to be, so if it's not equally long, you wrote something wrong

## Config

- **measure_in** -> Determines what to measure the progress in
  - (for example: 5 cranes/_day_)
  - Supports: second, minute, hour, day
  - Default: day
- **quick_add_amount** -> Determines how much progress you can add/remove quickly with the **Add/Subtract x!** buttons
  - Default: 1
- **font_size** -> This doesn't need explaining
  - 50 is the absolute max that can fit on a 1920x1080 screen
  - Default (and recommended): 45
- **bg_color** -> Background color
  - Supports: hexidecimal colors, colors spelled out (like yellow)
  - default: "#2aaaaa"
- **fg_color** -> Text color
  - Supports: hexidecimal colors, colors spelled out (like yellow)
  - defualt: "#000000"
