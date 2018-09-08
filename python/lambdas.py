
Y = lambda M : (lambda f : M (lambda a : (f(f))(a)))(lambda f : M (lambda a : (f(f))(a)))

count = lambda x : 0 if x == 0 else count(x-1)+1
lcount = Y(lambda rf : (lambda x : 0 if x == 0 else rf(x-1)+1))
Y(lambda rf : (lambda x : 0 if x == 0 else rf(x-1)+1))(10) # => 10

F = lambda r : lambda x : 1 if x == 0 else r(x-1) * x
fact = Y(F)
fact(4) # => 24
Y(lambda r : lambda x : 1 if x == 0 else r(x-1) * x)(4) # => 24

##############

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
g(3) # => 2, f was defined above

h = lambda x : g(x) + x
h(4) # => 6

h = lambda y : g(x) + y
h(4) # => 6, arg name does not make a difference

##############

f = lambda x,y : x*y
f(3,5) # => 15

f = lambda x : lambda y : x*y
f(3,5) # => TypeError: <lambda>() takes exactly 1 argument (2 given)
f(3) # => <function <lambda> at 0x1034eb668>
f(3)(5) # => 15

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
