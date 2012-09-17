from bigfloat import precision, setcontext, BigFloat

setcontext(precision(500))

f = BigFloat(0.1)
print f
for i in xrange(10000):
    f /= 2
print f
