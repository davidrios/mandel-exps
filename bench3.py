from mpmath import mp, mpf, libmp

mp.dps = 500

print libmp.BACKEND
f = mpf(0.1)
d = mpf(2)
print f
for i in xrange(1000000):
    f /= d
print f
