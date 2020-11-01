import os
import sys
import pathlib
import shutil
import datetime
import math
import concurrent.futures

def get_freq(line, old_minute):
    minute = float(line.split(",")[0].split(":")[1])
    if abs(minute - old_minute) == 0 or abs(minute - old_minute) == 45:
        return 0.25
    return abs((minute - old_minute))/60

def create_totals(f, total_dir, apt_num, year):
    f.seek(0,0)
    total = 0.0
    freq = 0
    if(year == "2014" or year == "2015"):
        freq = 0.25
    if(year == "2016"):
        freq = 1/60
    old_minute = 0

    for line in f:
        if(year == "2015"):
            freq = get_freq(line, old_minute)
        total += float(line.split(",")[1])*freq
        old_minute = float(line.split(",")[0].split(":")[1])
    total_file = open("{}/{}".format(total_dir, apt_num), "w")
    total_file.write(str(total));
    total_file.write("\n");
    total_file.close()
    
def create_daily(f, daily_dir, apt_num, year):
    f.seek(0,0)
    freq = 0
    if(year == "2014" or year == "2015"):
        freq = 0.25
    if(year == "2016"):
        freq = 1/60
    old_minute = 0

    daily_file = open("{}/{}".format(daily_dir, apt_num), "w")
    date = datetime.date.fromtimestamp(0);
    daily_energy = 0.0

    for line in f:
        if(year == "2015"):
            freq = get_freq(line, old_minute)
        line_date = datetime.datetime.strptime(line.split(",")[0], '%Y-%m-%d %H:%M:%S')
        if(date == datetime.date.fromtimestamp(0)):
            date = line_date
        line_energy = float(line.split(",")[1])*freq
        if line_date.date() != date.date():
            daily_file.write(str(date.date()))
            daily_file.write(",")
            daily_file.write(str(daily_energy))
            daily_file.write("\n")
            daily_energy = line_energy
            date = line_date
        else:
            daily_energy += line_energy
        old_minute = float(line.split(",")[0].split(":")[1])
    daily_file.write(str(date.date()))
    daily_file.write(",")
    daily_file.write(str(daily_energy))
    daily_file.write("\n")
    daily_energy = line_energy
    date = line_date


min_lines = 50000;

directory = pathlib.Path(sys.argv[1])
year = directory.parts[1]

total_dir = "{}/total-{}".format(directory, year)
try:
    os.mkdir(total_dir)
except FileExistsError:
    pass

daily_dir = "{}/daily-{}".format(directory, year)
try:
    os.mkdir(daily_dir)
except FileExistsError:
    pass

def proc_file(path):
    if path.is_file() and path.parts[-1].startswith("Apt"):
        with open(path) as f:
            n_lines = len(f.readlines())
            apt_num = path.name.split("_")[0]
            create_totals(f, total_dir, apt_num, year)
            create_daily(f, daily_dir, apt_num, year)

print("Início do Parsing de {}".format(directory.name))
#for path in directory.iterdir():
directories = directory.iterdir()
with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(proc_file, directories);
