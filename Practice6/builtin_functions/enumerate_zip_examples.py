# enumerate_zip_examples.py
names = ["Ali", "Dias", "Aruzhan"]
scores = [90, 80, 85]

for i, name in enumerate(names):
    print(i, name)

for name, score in zip(names, scores):
    print(name, score)

num_str = "123"
num = int(num_str)
print(type(num))
