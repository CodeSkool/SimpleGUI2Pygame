# why all the lambdas?

def function_caller(n, handler):
    """Call the handler function n times"""
    for i in range(n):
        handler(i+1)  # handler is a function that takes ZERO arguments

# define a global function that takes one argument
def bar(i):
    print "bar called", i

# try passing bar to function_caller
function_caller(5, bar)
# this works
print


# define  a global function that takes no arguments
def foo():
    print "foo called"

# try passing foo to function_caller:
# function_caller(5, foo)
# TypeError: foo() takes no arguments (1 given)

#hmmm is there a way we can call foo from function_caller?
# yes. we can call it if we wrap it in a function that accepts the correct
# number of parameters:
def baz(i):
    foo()
function_caller(5, baz)
print

# hmm, seems like a lot of work: we must define a new function just to call foo
# any better ways?
# yes. we can use a lambda expression to make an anonymous function in-line.
function_caller(5, lambda i: foo())
# lambda expression creates a new function that wraps an inner function call.
# the new function takes the correct number of arguments, but discards them
# because they are not needed by the inner function (foo)

#ok, this works in classes too, even though class methods have an extra parameter (self)

# suppose we want to call a class method using the function_caller
class SomeClass:
    def my_method(self, i):
        print "Calling my_method", i

    def my_other_method(self):
        print "Calling my_other_method"

    def caller(self):
        function_caller(5, self.my_method)
        #function_caller(5, self.my_other_method) # TypeError: my_other_method()
        #                                     takes exactly 1 argument (2 given)

    # we can still pass my_other_method by wrapping it in another function:
    def baz(self, i):
        self.my_other_method()

    def other_caller(self):
        function_caller(5, self.baz)

    # but again, this seems like a lot of extra code just to call
    # my_other_method. Can we use a lambda?
    # yes:
    def yet_another_caller(self):
        function_caller(5, lambda i: self.my_other_method())
# Once again:
# lambda expression creates a new function that wraps an inner function call.
# the new function takes the correct number of arguments, but discards them
# because they are not needed by the inner function (foo)


value = SomeClass()
value.caller()
