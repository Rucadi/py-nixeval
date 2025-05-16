import nixeval
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
print(nixeval.loads(f"import {dir_path}/default.nix"))