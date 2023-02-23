
counter = 0
active = True
holder = ""
n = input("")


for i in n:
    if i.isdigit() and active:
        holder += i
    else:
        if active and holder != "" and holder[0] != 'o':
            counter += int(holder)
            holder = ""
        if i == "=":
            print(f"Sum: {counter}")
        else:
            j = i.casefold()
            if j == "o":
                holder = j
            elif j == "f" and holder == "o":
                holder += j
            else:
                if j == "f" and holder == "of":
                    active = False
                elif  j == "n" and holder == "o":
                    active = True
                holder = ""