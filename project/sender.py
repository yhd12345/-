import os
import time

if __name__ == '__main__':
    while True:
        os.system("ncat -l 9999 -c \"python /home/daisy/文档/project/getKeyword.py\"")
        time.sleep(1)