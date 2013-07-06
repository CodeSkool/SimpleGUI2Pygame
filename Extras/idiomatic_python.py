#Idiomatic Python:
#(from http://www.youtube.com/watch?v=iTT85DOwEXY)

import argparse, os
import itertools, functools, collections
import urllib, decimal, threading
import contextlib, sys, pydoc

#1. Don't loop over indices
x = [1,7, 3, 4,2]
#Wrong:
for i in range(len(x)):
    print x[i]
#Right: (cleaner)
for i in x:
    print i
print

#2. If you need the index of an element, use enumerate:
#Wrong:
for i in range(len(x)):
   print i, x[i]
#Right: (faster, cleaner)
for i,v in enumerate(x):
    print i, v
print

#3. Use range (in Python 2, use xrange) to make iterable lists

#4. Use reversed
# Wrong:
for i in range(len(x) -1, -1, -1):
    print x[i]
# Right: (cleaner)
for i in reversed(x):
    print i
print

#4. To loop over two lists, use izip:
y = [5,6,7,8]
#Wrong:
l = min(len(x), len(y))
for i in range(l):
	print x[i], y[i]
#Right: (cleaner)
for i,j in itertools.izip(x,y):
	print i, j
print

# 5. Sort an iterable
for i in sorted(x):
    print i

for i in sorted(x, reverse=True):
    print i
print

# 6. Custom sort order:
colors = ["red", "yellow", "green", "blue"]
# Wrong:
def compare_length(c1, c2):
    if len(c1) < len(c2): return -1
    if len(c1) > len(c2): return 1
    return 0
print sorted(colors, cmp=compare_length)
# Right: (cleaner)
print sorted(colors, key=len)
print

# 7: Use iter with a sentinel value:
blocks = []
mystr = "The quick brown fox jumps over the lazy dog."
i = -1
def getc():
    global i
    i += 1
    if i<len(mystr):
        return mystr[i]
    return ''
# Wrong:
while True:
    c = getc()
    print c
    if c == '': # Empty string ('') is the sentinel value
        break
    blocks.append(c)
print "".join(blocks)
# Right: (cleaner)
for c in iter(getc, ''): # Empty string ('') is the sentinel value
    blocks.append(c)
print "".join(blocks)
print

# 8: Partial instead of lambda when you need fewer args
def foo(f):
    f()
def bar(s):
    print s
# One option:
foo(lambda: bar("hello world"))
# Another option:
foo(functools.partial(bar, "hello world"))
print

# DICTIONARIES
d = {"Andrew":"Black & White", "Jules":"Many Colors", "Andre":"Color and Darkness", "Tanya":"Blonde"}
# 9: Loop over a dictionary
# In general, use this form:
for k in d:
    print k, d[k]
# If you want to mutate d, iterate over d.keys()
for k in d.keys():
    if k.startswith("J"):
        del d[k]
print d
print

# 10: Loop over keys and values:
d = {"Andrew":"Black & White", "Jules":"Many Colors", "Andre":"Color and Darkness", "Tanya":"Blonde"}
# Wrong:
for k in d:
    print k, d[k]
# Better: (cleaner, faster due to no hash lookup for each k)
for k,v in d.items():
    print k, v
# Best: (cleaner, faster, less memory used (items creates a list))
for k,v in d.iteritems():
    print k, v
print

# 11: Building a dictionary
a = ("alpha", "bravo", "charlie", "delta")
b = (1,2,3,4)
# Wrong:
d = {}
for i in range(len(a)):
    d[a[i]] = b[i]
print d
# Right:
d = dict(itertools.izip(a, b))
print d
print

# 12: Counting with dicts
colors = ["red", "yellow", "pink", "green", "purple", "orange", "blue", "red", "green", "red", "blue", "red"]
# Good (basic, but you should know this)
d = {}
for color in colors:
    if color not in d:
        d[color] = 0
    d[color] += 1
print d
# Better (cleaner, get provides a default value)
d = {}
for color in colors:
    d[color] = d.get(color, 0) + 1
print d
# Another alternative (no need to initialize)
d = collections.defaultdict(int)
for color in colors:
    d[color] += 1
print dict(d) # result is not an actual dict
print

# 13: Group with dictionaries
names = ["Tanya", "Tony", "Tara", "Peter", "Potter", "Andre", "Abe", "Adele", "Ralph", "Raymond", "Betty", "Bea", "Bob"]
# Good (basic but know this)
d = {}
for name in names:
    key = len(name)
    if key not in d:
        d[key] = []
    d[key].append(name)
print d
# Better (cleaner)
d = {}
for name in names:
    key = len(name)
    d.setdefault(key, []).append(name)
print d
# Another option (cleaner still)
d = collections.defaultdict(list)
for name in names:
    key = len(name)
    d[key].append(name)
print dict(d)
print

# 14: Popitem is atomic! THREAD SAFE!
a = ("alpha", "bravo", "charlie", "delta")
b = (1,2,3,4)
d = dict(itertools.izip(a,b))
while d:
    k,v = d.popitem() # This is thread safe: no need for a lock
    print k, v
print

# 15: Linking dicts
a = ("color", "user")
b = ("red", "guest")
defaults = dict(itertools.izip(a,b))
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user")
parser.add_argument("-c", "--color")
namespace = parser.parse_args([])
command_line_args = {k:v for k, v in vars(namespace).items() if v}
# Bad: Copies too much data
d = defaults.copy()
d.update(os.environ)
d.update(command_line_args)
print d
# Good (python 3 :'(   )
#d = ChainMap(command_line_args, os.environ, defaults)
#print d
print


# 16: Clarify function calls with keyword arguments
def twitter_search(text, retweets, numtweets, popular):
    pass
# Bad:
twitter_search("obama", False, 20, True)
# Good: (more human readable)
twitter_search("obama", retweets=False, numtweets=20, popular=True)

# 17: Use named tuples
# Bad:
test_results = (0, 4)
print test_results
# Good:
TestResults = collections.namedtuple("TestResults", ["failed", "attempted"])
test_results = TestResults(failed=0, attempted=4)
print test_results
print

# 18: Unpacking sequences
p = "Andrew", "Sadavoy", 0x29, "python@example.com"
# Wrong:
fname = p[0]
lname = p[1]
age = p[2]
email = p[3]
print fname, lname, age, email
# Right: sequence unpacking
fname, lname, age, email = p
print fname, lname, age, email
print

# 19: Simultaneous state updates
# Wrong:
def fib(n):
    x = 0
    y = 1
    for i in range(n):
        print x,
        t = y
        y = x + y
        x = t
print fib(10)
# Right: (atomic operation, cleaner, higher level thinking)
def fib(n):
    x, y = 0, 1
    for i in range(n):
        print x,
        x, y = y, x + y      # atomic operation, cleaner, higher level thinking
print fib(10)
print

# 20: Concatenate strings
names = ["Tanya", "Tony", "Tara", "Peter", "Potter", "Andre", "Abe", "Adele", "Ralph", "Raymond", "Betty", "Bea", "Bob"]
# BAD:
s = names[0]
for name in names[1:]:
    s += ", " + name
print s
# GOOD: MUCH MORE PERFORMANT
s = ", ".join(names)
print s
print

# 21: Updating sequences
names = ["Tanya", "Tony", "Tara", "Peter", "Potter", "Andre", "Abe", "Adele", "Ralph", "Raymond", "Betty", "Bea", "Bob"]
# BAD: WRONG DATA STRUCTURE
del names[0]
names.pop(0)
names.insert(0, "mark")
print names
# GOOD: Use deque - more efficient than updating the 0th element of a list
names = collections.deque(["Tanya", "Tony", "Tara", "Peter", "Potter", "Andre", "Abe", "Adele", "Ralph", "Raymond", "Betty", "Bea", "Bob"])
del names[0]
names.popleft()
names.appendleft("mark")
print list(names)
print


# DECORATORS and CONTEXT MANAGERS
# Helps separate business logic from admin logic
# Clean beautiful tools for factoring code and improving code reuse
# Good naming is essential
# Spiderman rule: With great power comes great responsibility

# 22: Use decorators to factor-out admin logic
# Bad: admin logic mixed in with business logic
def web_lookup(url, saved={}):
    if url in saved:
        return saved[url]
    page = urllib.urlopen(url).read()
    saved[url] = page
    return page
#print web_lookup("http://www.google.com/")
# Good: first define "cache" function decorator...
def cache(func):
    saved = {}
    @functools.wraps(func)
    def newfunc(*args):
        if args in saved:
            return saved[args]
        result = func(*args)
        saved[args] = result
        return result
    return newfunc
#      ...now adorn the web_lookup function with the decorator. MUCH CLEANER!
@cache
def web_lookup(url):
    return urllib.urlopen(url).read()
#print web_lookup("http://www.google.com/")
print

# 23: Factor out temporary contexts:
# Bad:
old_context = decimal.getcontext().copy()
decimal.getcontext().prec = 50
print decimal.Decimal(355) / decimal.Decimal(113)
decimal.setcontext(old_context)
# Good:
with decimal.localcontext(decimal.Context(prec=50)):
    print decimal.Decimal(355) / decimal.Decimal(113)
print

# 24: Opening and closing files
# Bad:
f = open("data.txt")
try:
    data = f.read()
finally:
    f.close()
print data
# Good:
with open("data.txt") as f:
    data = f.read()
print data
print

# 25: How to use locks
lock = threading.Lock()
# Old way:
lock.acquire()
try:
    print "Critical section 1"
    print "Critical section 2"
finally:
    lock.release() # MUST MUST MUST release the lock (or puppies die. every time.)
# New way:
with lock:
    print "Critical section 1"
    print "Critical section 2"
print

# 26: Ignore certain error types
# BAD:
# check if file exists, then remove it ---> This is bad because it creates a race condition NO NO NO
# Good
try:
    os.remove("somefile.tmp")
except OSError:
    pass
# Better: (Ignored is currently being added to the library - here's the code till then:)
@contextlib.contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass
# ... now we can use the ignored context manager:
with ignored(OSError):
    os.remove("somefile.tmp")
print


# 27: Factor out temporary contexts
# Good:
with open("help.txt", "w") as f:
    oldstdout = sys.stdout
    sys.stdout = f
    try:
        print "This is some text"
    finally:
        sys.stdout = oldstdout
# Better: (first we define redirect_stdout pending release in the library)
@contextlib.contextmanager
def redirect_stdout(fileobj):
    oldstdout = sys.stdout
    sys.stdout = fileobj
    try:
        yield
    finally:
        sys.stdout = oldstdout
#    ... now we can use it
with open("help.txt", "w") as f:
    with redirect_stdout(f):
        print "This is some text"
print




#Concise Expressive One-liners
# Two conflicting rules:
# 1: Don't put too much on one line
# 2: Don't break atoms of thought into subatomic particles
#
# Raymonds rule:
# One logical line of code equals one English sentence

# 28: List comprehensions and generators
# Good:
result = []
for i in xrange(10):
    s = (i + 1) ** 2
    result.append(s)
print sum(result)
# Better:
print sum((i + 1) ** 2 for i in xrange(10))
print