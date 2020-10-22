
from enum import Enum
import base64
import time

"""time_str=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
time_str=time_str.replace("-","")"""

def console(name,*arg,**_dict):
    doc={"doc":_dict}
    print(name,arg,doc)


console("hwb","is","man",job="coder",isRead=1)

def main():
    print("This Test.py's Main Method")

if __name__ == "__main__":
    pass
