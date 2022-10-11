import os
import sys

for root, dirs, files in os.walk("/mydir"):
    for file in files:
        print(file)
        sys.exit()