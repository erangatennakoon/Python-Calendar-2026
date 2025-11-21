from PIL import Image, ImageDraw, ImageFont
import calendar
import os

def draw_month(draw, year, month, x_offset, y_offset, cell_width, cell_height,
               font, smallfont, sunday_color, weekday_color):
    # Draw month header
    month_name = f"{calendar.month_name[month]} {year}"
    bbox = draw.textbbox((0, 0), month_name, font=font)
    w = bbox[2] - bbox[0]
    start_x = x_offset + (cell_width * 7 - w) // 2
    draw.text((start_x, y_offset), month_name, fill=weekday_color, font=font)

    # Draw day headers
    for i, day in enumerate(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']):
        color = sunday_color if i == 0 else weekday_color
        bbox = draw.textbbox((0, 0), day, font=smallfont)
        w = bbox[2] - bbox[0]
        tx = x_offset + i * cell_width + (cell_width - w) // 2
        ty = y_offset + 40
        draw.text((tx, ty), day, fill=color, font=smallfont)

    # Draw days
    cal = calendar.Calendar(firstweekday=6)
    weeks = cal.monthdayscalendar(year, month)
    for row, week in enumerate(weeks):
        for col, day in enumerate(week):
            if day == 0:
                continue
            color = sunday_color if col == 0 else weekday_color
            day_str = f"{day:2d}"  # Right aligned 2 characters
            bbox = draw.textbbox((0, 0), day_str, font=smallfont)
            w = bbox[2] - bbox[0]
            tx = x_offset + col * cell_width + (cell_width - w)
            ty = y_offset + 70 + row * cell_height
            draw.text((tx, ty), day_str, fill=color, font=smallfont)

def main():
    year = 2026
    year_title = "2026"
    months_per_row = 4
    rows = 3
    cell_width = 40
    cell_height = 28
    month_width = cell_width * 7 + 15
    month_height = 70 + cell_height * 6 + 10
    title_fontsize = 60
    title_pad = title_fontsize + 20
    img_width = month_width * months_per_row + 50
    img_height = month_height * rows + 30 + title_pad

    # Colors and fonts
    sunday_color = (220, 30, 30)  # Red
    weekday_color = (0, 0, 0)     # Black
    bg_color = (255, 255, 255)    # White

    # Path to Verdana font on Windows
    verdana_path = r"C:\Windows\Fonts\verdana.ttf"
    if not os.path.exists(verdana_path):
        raise FileNotFoundError(f"Could not find '{verdana_path}'. Please ensure the file exists on your system.")

    # Load Verdana fonts at different sizes
    titlefont = ImageFont.truetype(verdana_path, title_fontsize)
    font = ImageFont.truetype(verdana_path, 18)
    smallfont = ImageFont.truetype(verdana_path, 14)

    # Prepare image
    img = Image.new('RGB', (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw the large title "2026" at the top, centered
    bbox = draw.textbbox((0, 0), year_title, font=titlefont)
    w = bbox[2] - bbox[0]
    title_x = (img_width - w) // 2
    title_y = 10
    draw.text((title_x, title_y), year_title, fill=weekday_color, font=titlefont)

    # Draw each month
    for idx in range(12):
        row = idx // months_per_row
        col = idx % months_per_row
        x_offset = 25 + col * month_width
        y_offset = title_pad + 15 + row * month_height
        draw_month(
            draw, year, idx + 1, x_offset, y_offset,
            cell_width, cell_height,
            font, smallfont, sunday_color, weekday_color
        )
    # Save image
    img.save('calendar_2026.png')
    print('calendar_2026.png saved!')

if __name__ == "__main__":
    main()
