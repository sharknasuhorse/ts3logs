from glob import glob
import html
import re
import datetime


def get_id_list(logs_file_name_list):
    name_id_list = []
    pattern = '(.+?)id:\d+'
    repatter = re.compile(pattern)

    for log in logs_file_name_list:
        with open(log, mode="r", encoding="utf8") as f:
            log_lines = f.readlines()

        for log_line in log_lines:
            if "Cl0wn" in html.unescape(log_line) and "id:" in html.unescape(log_line).split()[6]:
                name_id = repatter.match(
                    repr(html.unescape(log_line).split()[6])).group().split(":")[1]
                if name_id not in name_id_list:
                    name_id_list.append(name_id)
    return sorted(name_id_list)


def get_date(logs_file_name_list, name_id_list):
    user_most_long_date = ""
    # client connected
    # client disconnected
    for log in logs_file_name_list:
        with open(log, mode="r", encoding="utf8") as f:
            log_lines = f.readlines()
        for log_line in log_lines:
            if "client connected" in log_line and name_id_list in log_line:

    return user_most_long_date


if __name__ == '__main__':
    logs_file_name_list = glob("./logs/*1.log")
    name_id_list = get_id_list(logs_file_name_list)
    print(name_id_list)
    get_date(logs_file_name_list, name_id_list)
