# write_files.py
f = open("sample.txt", "w")
f.write("Hello\n")
f.close()

f = open("sample.txt", "a")
f.write("World\n")
f.close()
