"""
Abstract Class, Abstract Method, Virtual Method, Hook

An abstract class is one that is never intended to be instantiated. It is only
meant to be a base class for other classes.

An abstract method is what makes a class abstract: the abstract class makes a
call to at least one method for which the class does not provide a definition.
This will fail if the class is instantiated and the code that calls the abstract method is run.
Derived classes MUST implement this method or face an exception.

A virtual method is simply a method that can be overridden. All methods are virtual in python (as far as I know).

Abstract Class, Abstract Method, and Virtual Method are all object oriented programming concepts.

A Hook is a Virtual Method that does nothing in the base case. It is virtual, so derived classes need not override it. It does nothing,
so derived classes that *do* override it are not replacing any behavior, only adding behaviour.
Hooks are called from Template Methods (a design pattern).
"""




class StateBase: # abstract class - if we instantiate it we get errors because some methods are missing!
    def __init__(self):
        self.foo() # abstract method: must be overridden in every child class, otherwise run-time error
        self.my_hook()

    def my_hook(self): # virtual method: CAN be overridden but it's not mandatory (in python, all methods are virtual)
        pass # this is what makes my_hook a hook: it is a virtual method that *does nothing by default*

class SomeState(StateBase): # overrides foo (because it must), but does not override my_hook
    def __init__(self):
        print
        print "SomeState"
        StateBase.__init__(self)
    def foo(self):
        print "call to foo"

class OtherState(StateBase): # overrides foo (because it must) AND overrides my_hook (because it wants to)
    def __init__(self):
        print
        print "OtherState"
        StateBase.__init__(self)

    def foo(self):
        print "call to foo"
    def my_hook(self):
        print "call to my_hook"

#s1 = StateBase() # AttributeError: StateBase instance has no attribute 'foo'
s2 = SomeState() # This works just fine
s3 = OtherState() # This works just fine, and my_hook is overridden
