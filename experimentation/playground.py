import re

string_var = "The quick brown fox goes somewhere."

string_var = re.sub('brown', 'black', string_var)

print(string_var)