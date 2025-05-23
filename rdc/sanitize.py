import csv
import json

with open('data/map.json', 'r') as json_file:
    channel_map_by_date = json.load(json_file)

valid_channels = [
    "rdcgaming", "rdcgamingtwo", "rdcgamingthree", "rdcgamingfour", "rdcgamingfive"
]

input_csv = '../raw/data.csv'
output_csv = 'data/data.csv'

with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
        open(output_csv, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    seen = set()

    writer.writerow(['username', 'message', 'channel', 'date'])

    for row in reader:
        if len(row) != 4:
            continue

        username, message, channel, date = row
        if channel in valid_channels:
            name_map = channel_map_by_date.get(date, {})
            mapped_channel = name_map.get(channel)
            if mapped_channel and message not in seen:
                writer.writerow([username, message, mapped_channel, date])
                seen.add(message)
