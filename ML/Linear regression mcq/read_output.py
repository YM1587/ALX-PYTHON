try:
    with open("mcq_output.txt", "r", encoding="utf-16") as f:
        print(f.read())
except:
    with open("mcq_output.txt", "r", encoding="utf-8") as f:
        print(f.read())
