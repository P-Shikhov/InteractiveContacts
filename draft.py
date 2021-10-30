a = {'x': 1, 'a': ''}

b = {k: v for k, v in a.items() if v}

print(b)