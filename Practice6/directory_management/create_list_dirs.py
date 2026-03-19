# create_list_dirs.py
import os

os.makedirs("test_dir/sub_dir", exist_ok=True)
print("Directories:", os.listdir("."))
print("Current folder:", os.getcwd())
