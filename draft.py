s = b'first_name=Pavel111&last_name=&phone_number=90990&email=&date_born=2021-10-05'
s = s.decode('utf-8')
print(s.split("&"))
for item in s.split("&"):
    pair = item.split("=")
    if pair[1]:
        print(pair[0])