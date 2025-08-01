class Parent:
    def method(self):
        pass

    def wrong(self):
        pass


class Child(Parent):
    def method(self):
        parent = super()  # ok
        super().method()  # ok
        Parent.method(self)  # ok
        Parent.super(1, 2)  # ok

    def wrong(self):
        parent = super(Child, self)  # wrong
        super(Child, self).method  # wrong
        super(
            Child,
            self,
        ).method()  # wrong


class BaseClass:
    def f(self):
        print("f")


def defined_outside(self):
    super(MyClass, self).f()  # CANNOT use super()


class MyClass(BaseClass):
    def normal(self):
        super(MyClass, self).f()  # can use super()
        super().f()

    def different_argument(self, other):
        super(MyClass, other).f()  # CANNOT use super()

    def comprehension_scope(self):
        [super(MyClass, self).f() for x in [1]]  # CANNOT use super()

    def inner_functions(self):
        def outer_argument():
            super(MyClass, self).f()  # CANNOT use super()

        def inner_argument(self):
            super(MyClass, self).f()  # can use super()
            super().f()

        outer_argument()
        inner_argument(self)

    def inner_class(self):
        class InnerClass:
            super(MyClass, self).f()  # CANNOT use super()

            def method(inner_self):
                super(MyClass, self).f()  # CANNOT use super()

        InnerClass().method()

    defined_outside = defined_outside


from dataclasses import dataclass


@dataclass
class DataClass:
    def normal(self):
        super(DataClass, self).f()  # Error
        super().f()  # OK


@dataclass(slots=True)
def normal(self):
    super(DataClass, self).f()  # OK
    super().f()  # OK (`TypeError` in practice)


# see: https://github.com/astral-sh/ruff/issues/18477
class A:
    def foo(self):
        pass


class B(A):
    def bar(self):
        super(__class__, self).foo()


# see: https://github.com/astral-sh/ruff/issues/18684
class C:
    def f(self):
        super = print
        super(C, self)


import builtins


class C:
    def f(self):
        builtins.super(C, self)


# see: https://github.com/astral-sh/ruff/issues/18533
class ClassForCommentEnthusiasts(BaseClass):
    def with_comments(self):
        super(
            # super helpful comment
            ClassForCommentEnthusiasts,
            self
        ).f()
        super(
            ClassForCommentEnthusiasts,
            # even more helpful comment
            self
        ).f()
        super(
            ClassForCommentEnthusiasts,
            self
            # also a comment
        ).f()


# Issue #19096: super calls with keyword arguments should emit diagnostic but not be fixed
class Ord(int):
    def __len__(self):
        return super(Ord, self, uhoh=True, **{"error": True}).bit_length()

class ExampleWithKeywords:
    def method1(self):
        super(ExampleWithKeywords, self, invalid=True).some_method()  # Should emit diagnostic but NOT be fixed
    
    def method2(self):
        super(ExampleWithKeywords, self, **{"kwarg": "value"}).some_method()  # Should emit diagnostic but NOT be fixed
    
    def method3(self):
        super(ExampleWithKeywords, self).some_method()  # Should be fixed - no keywords
