import os
from datetime import datetime

cmd_path = r'D:\Temp\INSCommand.ini'
cmd_mtime_timestamp = os.path.getmtime(cmd_path)
cmd_mtime_str = datetime.fromtimestamp(cmd_mtime_timestamp).strftime("%H_%M_%S")
print(cmd_mtime_timestamp)
print(cmd_mtime_str)
