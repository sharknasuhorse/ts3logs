from glob import glob
import html
import re
import datetime


def get_id_list(logs_file_name_list):
    name_id_list = []
    user_name = "Cl0wn"
    pattern = '(.+?)id:\d+'
    repatter = re.compile(pattern)

    for log in logs_file_name_list:
        with open(log, mode="r", encoding="utf8") as f:
            log_lines = f.readlines()

        for log_line in log_lines:
            if user_name in html.unescape(log_line) and "id:" in html.unescape(log_line).split()[6]:
                name_id = repatter.match(
                    repr(html.unescape(log_line).split()[6])).group().split(":")[1]
                if name_id not in name_id_list:
                    name_id_list.append(name_id)

    return sorted(name_id_list)


def get_date(logs_file_name_list, name_id_list):
    user_most_long_connected_time = ""
    user_most_long_connected_date = ""
    connected_date = ""
    disconnected_date = ""

    pattern = '.?\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}'
    repatter = re.compile(pattern)

    for log in logs_file_name_list:
        connected_flag = False

        with open(log, mode="r", encoding="utf8") as f:
            log_lines = f.readlines()

        for log_line in log_lines:
            if "client connected" in log_line:
                for name_id in name_id_list:
                    if "id:" + name_id + ")" in log_line and connected_flag == False:
                        connected_flag = True
                        connected_date = get_date_time(repatter, log_line)

            if "client disconnected" in log_line and connected_flag == True:
                for name_id in name_id_list:
                    if "id:" + name_id + ")" in log_line:
                        connected_flag = False
                        disconnected_date = get_date_time(repatter, log_line)
                        connected_time = disconnected_date - connected_date

                        if user_most_long_connected_time == "" or user_most_long_connected_time < connected_time:
                            user_most_long_connected_time = connected_time
                            user_most_long_connected_date = connected_date

    return user_most_long_connected_time, user_most_long_connected_date


def get_date_time(repatter, log_line):
    date_result = repatter.match(
        repr(log_line)).group().replace("\"", "").replace("\'", "")
    date = datetime.datetime.strptime(
        date_result, "%Y-%m-%d %H:%M:%S")
    return date


def print_logs(logs_file_name_list):
    for log in logs_file_name_list:
        with open(log, mode="r", encoding="utf8") as f:
            log_lines = f.readlines()
        for log_line in log_lines:
            print(html.unescape(log_line))


if __name__ == '__main__':
    logs_file_name_list = glob("./logs/*1.log")
    name_id_list = get_id_list(logs_file_name_list)
    print(name_id_list)
    time, date = get_date(logs_file_name_list, name_id_list)
    print(time, date)
