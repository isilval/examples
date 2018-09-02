# This works:
A = lambda x : (lambda y : y + 1) (x)

# This does not:
Y = lambda M : (lambda f : M(f(f)))(lambda f : M(f(f)))
F = lambda r : lambda x : 1 if x == 0 else r(x-1) * x
fact = Y(F)

# This works:
facts = lambda x : 1 if x == 0 else facts(x-1) * x
facts(3)

# But this does not:
facts = lambda f : lambda x : 1 if x == 0 else f(x-1) * x
facts(facts) # Although this does
facts(facts)(3) # But this does not
facts(facts(facts))(3) # Nor does this
