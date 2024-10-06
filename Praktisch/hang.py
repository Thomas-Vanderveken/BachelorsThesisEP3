import re
cik_pattern = re.compile(r'^(?!.*\s)(?=.*\d)[A-Z0-9]{5,12}$', re.IGNORECASE)

print(cik_pattern.match("4616207"))