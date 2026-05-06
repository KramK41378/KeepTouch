sp = [0] * 1440
for i in open('26_9847.txt'):
    start, end = map(int, i.split())
    for j in range(start, end):
        sp[j] += 1
k = max(sp)
for i in range(len(sp)):
    if sp[i] != k:
        sp[i] = 0
    else:
        sp[i] = 1
s = ''.join(map(str, sp))
while '00' in s:
    s = s.replace('00', '0')
s = s.strip('0').rstrip('0').lstrip('0')
print(len(s.split('0')))
print(k)