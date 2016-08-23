from collections import Counter

c = Counter()

for ch in 'programming':
    print ch
    c[ch] = c[ch] + 1

print c
