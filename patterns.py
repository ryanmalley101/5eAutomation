# Regex for valid dice roll strings (like 1d6+4). M is used to inherit the
# ability modifier
# Valid Strings:
# 1d8
# 10d2+10
# 2d4+M
# 1d6-10
# 6d2-M
# 1d6+2d8+10d4+7
# 2d4+4d6+6d8+M
# Invalid Strings:
# 1d8+3M2
# 1d8-1d6+1d8+N
DICESTRINGPATTERN = r'(\d+)d(\d+)|(?=(\d+|M))'
