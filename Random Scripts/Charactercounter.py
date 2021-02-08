query = str(input("Input Text to count"))

Count = {}

for x in query:
    if x in Count:
        Count[x] += 1
    else:
        Count[x] = 1

print(Count)