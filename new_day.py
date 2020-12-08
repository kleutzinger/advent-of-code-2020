import datetime
import os


dt = datetime.datetime.today()
folder_num = str(dt.day + 1).zfill(2)
os.system("mkdir " + folder_num)
os.system("cp boilerplate.py " + os.path.join(folder_num, "run.py"))
os.system("touch " + os.path.join(folder_num, "input.txt"))