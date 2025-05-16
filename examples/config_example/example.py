import nixeval
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

os.environ["MYSECRET"] = "123456"
print(nixeval.loads(f"import {dir_path}/default.nix"))

os.environ["MYSECRET"] = "NOTREAL"
print(nixeval.loads(f"import {dir_path}/default.nix"))

#should assert
os.environ["MYSECRET"] = ""
try :
    print(nixeval.loads(f"import {dir_path}/default.nix"))
    os.environ["MYSECRET"] = ""
except ValueError:
    print("Assert inside nix failed")
