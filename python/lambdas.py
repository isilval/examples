
def f():
	return 1
f() # => 1

f = lambda : 1
f() # => 1

##############

def g(x):
	return h(x)+1

g = lambda x : h(x)+1
g(3) # => NameError: global name 'h' is not defined

g = lambda x : f()+1
g(3) # => 2, f was defined above; arg not used

j = lambda x : g(x) + x
j(4) # => 6

j = lambda y : g(y) + y
j(4) # => 6, arg name does not make a difference

##############

f = lambda x,y : x*y
f(3,5) # => 15

f = lambda x : lambda y : x*y
f(3,5) # => TypeError: <lambda>() takes exactly 1 argument (2 given)
f(3) # => <function <lambda> at 0x1034eb668>
f(3)(5) # => 15

##############

(lambda x,y : x*y)(3,5) # => 15, truly anonymous, no function names

(lambda x: x+1)(3) # => 4
# Is the same as:
(lambda y: (lambda x: x+1)(y))(3) # => 4

##############

f = lambda g,x : g(x)
f(lambda y : y+2,3) # => 5, a whole function passed in, not an evaluation

f = lambda g,x,y : g(x)+y
f(lambda y : y+1,2,3) # => 6

##############

f = lambda x : lambda y : x*y
g = lambda h,x : h(x)
g(lambda y : y+2,3) # => 5, no surprise, only g and h involved
g(f(7),5) # => 35, an evaluation passed in, whose value happens to be a whole function

##############

a = [1,2,3,4]
b = [17,12,11,10]
c = [-1,-4,5,9]
map(lambda x:x-1,a) # => [0, 1, 2, 3]
map(lambda x,y:x+y, a,b) # => [18, 14, 14, 14]
map(lambda x,y,z:x+y+z, a,b,c) # => [17, 10, 19, 23]

reduce(lambda x,y: x+y, [47,11,42,13]) # => 113

##############

def fact(x):
	return 1 if x == 0 else fact(x-1) * x

fact = lambda x : 1 if x == 0 else fact(x-1) * x
# Either way:
fact(5) # => 120

# What if I wanted to do:
(lambda x : 1 if x == 0 else fact(x-1) * x)(5) # where fact is not defined yet?

# Let's use an extra argument that, when applied to anything, returns a function like fact
fact_maker = lambda f : lambda x : 1 if x == 0 else fact_maker(f)(x-1) * x # But the recursion keeps applying the dummy f
fact = fact_maker('foo')
fact(5) # => 120

# Could we apply fact_maker to itself? Sure, the arg does nothing (yet)
fact = fact_maker(fact_maker)
fact(5) # => 120

# This way, the recursion above also looks like fact_maker(fact_maker)
fact_maker_maker = lambda f : lambda x : 1 if x == 0 else fact_maker_maker(fact_maker_maker)(x-1) * x
# And we can just use f(f) as the recursion, as long as we call it with fact_maker(fact_maker) originally:
fact_maker_maker = lambda f : lambda x : 1 if x == 0 else f(f)(x-1) * x
fact = fact_maker_maker(fact_maker_maker)
fact(5) # => 120

# So, now we have lost the bound name in the recursion, and we only use args
# Now, since:
(lambda x: x+1)
# is the same as:
(lambda y: (lambda x: x+1)(y))
# then:
fact_maker_maker = lambda f : lambda x : 1 if x == 0 else (lambda a: f(f)(a))(x-1) * x
fact = fact_maker_maker(fact_maker_maker)
fact(5) # => 120

# Also, since:
(lambda y: (lambda x: x+1)(y))
# is the same as:
(lambda y: (lambda f: f(y))(lambda x: x+1))
# then we can always abstract out (lambda a: f(f)(a)):
fact_maker_maker = lambda f : (lambda r: lambda x : 1 if x == 0 else r(x-1) * x)(lambda a: f(f)(a))
fact = fact_maker_maker(fact_maker_maker)
fact(5) # => 120

# Now, since (lambda r: lambda x : 1 if x == 0 else r(x-1) * x) is self contained
# we can pull it out and assign to a variable:
M = lambda r: lambda x : 1 if x == 0 else r(x-1) * x
function_maker = lambda f : M(lambda a: f(f)(a)) # we can also rename fact_maker_maker
fact = function_maker(function_maker) # as long as we keep using it consistently
fact(5) # => 120

# And since the value of function_maker does not depend on the name, then we can replace it in the definition of fact:
M = lambda r: lambda x : 1 if x == 0 else r(x-1) * x
fact = (lambda f : M(lambda a: f(f)(a)))(lambda f : M(lambda a: f(f)(a)))
fact(5) # => 120

# Finally, M can be generalized by abstracting it away inside a lambda:
Y = lambda M: (lambda f : M(lambda a: f(f)(a)))(lambda f : M(lambda a: f(f)(a))) # This is (a variation of) the so-called Y combinator
F = lambda r: lambda x : 1 if x == 0 else r(x-1) * x
fact = Y(F)
fact(5) # => 120

# Or just:
Y = lambda M: (lambda f : M(lambda a: f(f)(a)))(lambda f : M(lambda a: f(f)(a)))
fact = Y(lambda r: lambda x : 1 if x == 0 else r(x-1) * x)
fact(5) # => 120

# Or even:
Y = lambda M: (lambda f : M(lambda a: f(f)(a)))(lambda f : M(lambda a: f(f)(a)))
Y(lambda r : lambda x : 1 if x == 0 else r(x-1) * x)(5) # => 120

# Or even yet:
(lambda M: (lambda f : M(lambda a: f(f)(a)))(lambda f : M(lambda a: f(f)(a))))(lambda r : lambda x : 1 if x == 0 else r(x-1) * x)(5) # => 120

##############

# Exercise, count is defined as follows:
def count(x):
	return  0 if x == 0 else count(x-1)+1

# Redefine count without calling itself

# First, count can also be defined as:
count = lambda x : 0 if x == 0 else count(x-1)+1

# Then:
Y = lambda M: (lambda f : M(lambda a: f(f)(a)))(lambda f : M(lambda a: f(f)(a)))
lcount = Y(lambda rf : (lambda x : 0 if x == 0 else rf(x-1)+1))
lcount(10) # => 10
Y(lambda rf : (lambda x : 0 if x == 0 else rf(x-1)+1))(10) # => 10
