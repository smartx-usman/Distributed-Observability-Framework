# Log query to get data from Loki
# logcli --addr=http://loki-headless.observability:3100 -o raw -q query '{app="mqtt-publisher-mixed"}' --limit 1000000 --batch 100 --forward --from "2023-01-26T12:25:00Z" --to "2023-01-26T13:24:59Z" > publisher-mixed

# Python code to
# demonstrate readlines()

header = "timestamp,level,message,sensor,status\n"

# File for writing
write_file = open('sensor-mixed-formatted.csv', 'w')
write_file.writelines(header)

# File to read
file1 = open('publisher-mixed', 'r')
Lines = file1.readlines()

count = 0
# Process the file
for line in Lines:
    count += 1
    try:
        line_split = line.split(",")
        timestamp = line_split[0]
        level_message = line_split[1].split("-")
        level = level_message[1].strip()
        message = level_message[2].split(":")[1].strip()
        sensor = line_split[2].split(":")[1].strip()
        status = line_split[3].split(":")[1].strip()

        write_file.writelines(timestamp + "," + level + "," + message + "," + sensor + "," + status + "\n")
    except IndexError as e:
        print("Error at line: " + str(count))
        print('Continue...')
    print("Line{}: {}".format(count, line.strip()))

write_file.close()
