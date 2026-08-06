binary_str = "00000000000011000000000001110000000000111000000000011100000000001110000000000011100000000001110000000000111000000000111000000000011100000000000011001100000000000001100000000000011000000000000110000000000010000000000000"

BG_WHITE = "\033[47m"  
BG_CYAN = "\033[46m"   
RESET = "\033[0m"      

for i in range(0, len(binary_str), 15):
    row = binary_str[i:i+15]
    row_output = ""
    for char in row:
        if char == "1":
            row_output += f"{BG_CYAN}  {RESET}"
        else:
            row_output += f"{BG_WHITE}  {RESET}"
    print(row_output)
