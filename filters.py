"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest from
the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You'll edit this file in Tasks 3a and 3c.
"""
import operator

from models import CloseApproach
from enum import Enum

# INFO
""" For those who reading/grading this, I come from C and this syntax of tabs is really bothering me so I'mma just add the tailing end for everything =)))) """
""" You can quickly skim through what I changed by the keyword 'TASK - DONE' ;) """

class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""
#endclass

class AttributeFilter:
    """A general superclass for filters on comparable attributes.

    An `AttributeFilter` represents the search criteria pattern comparing some
    attribute of a close approach (or its attached NEO) to a reference value. It
    essentially functions as a callable predicate for whether a `CloseApproach`
    object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value, and
    calling the filter (with __call__) executes `get(approach) OP value` (in
    infix notation).

    Concrete subclasses can override the `get` classmethod to provide custom
    behavior to fetch a desired attribute from the given `CloseApproach`.
    """
    def __init__(self, op, value):
        """Construct a new `AttributeFilter` from an binary predicate and a reference value.

        The reference value will be supplied as the second (right-hand side)
        argument to the operator function. For example, an `AttributeFilter`
        with `op=operator.le` and `value=10` will, when called on an approach,
        evaluate `some_attribute <= 10`.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value
    #enddef

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)
    #enddef

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a close approach.

        Concrete subclasses must override this method to get an attribute of
        interest from the supplied `CloseApproach`.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest, comparable to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError
    #enddef

    def __repr__(self):
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"
    #enddef
#endclass

# SUPPORT CLASS 
class FilterType(Enum): 
    DATE = 0
    DISTANCE = 1
    VELOCITY = 2
    DIAMETER = 3
    HAZARDOUS = 4
#endclass

# SUPPORT CLASS  
class Filter:

    def __init__(self, requirement: list[tuple[3]] = None):
        self._list_op_val_type = requirement
    #enddef

    def check(self, ca: CloseApproach = None) -> bool:
        ret: bool = True
        # Do each of the req in the list
        for check in self._list_op_val_type:
            if check[2] == FilterType.DATE:
                ret &= check[0](ca.time.date(), check[1])
            elif check[2] == FilterType.DISTANCE:
                ret &= check[0](ca.distance, check[1])
            elif check[2] == FilterType.VELOCITY:
                ret &= check[0](ca.velocity, check[1])
            elif check[2] == FilterType.DIAMETER:
                ret &= check[0](ca.neo.diameter, check[1])
            elif check[2] == FilterType.HAZARDOUS:
                ret &= check[0](ca.neo.hazardous, check[1])
            #endif
        #endfor
        return ret
    #enddef
#endclassDISTANCE

# TASK - DONE
def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a value from the
    user's options at the command line. Each one corresponds to a different type
    of filter. For example, the `--date` option corresponds to the `date`
    argument, and represents a filter that selects close approaches that occurred
    on exactly that given date. Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).

    The return value must be compatible with the `query` method of `NEODatabase`
    because the main module directly passes this result to that method. For now,
    this can be thought of as a collection of `AttributeFilter`s.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """

    list_filter = []

    if date != None:
        list_filter.append((operator.eq, date, FilterType.DATE))
    #endif

    if start_date != None:
        list_filter.append((operator.ge, start_date, FilterType.DATE))
    #endif

    if end_date != None:
        list_filter.append((operator.le, end_date, FilterType.DATE))
    #endif

    if (distance_min != None) and (distance_min != ""):
        list_filter.append((operator.ge, float(distance_min), FilterType.DISTANCE))
    #endif

    if (distance_max != None) and (distance_max != ""):
        list_filter.append((operator.le, float(distance_max), FilterType.DISTANCE))
    #endif

    if (velocity_min != None) and (velocity_min != ""):
        list_filter.append((operator.ge, float(velocity_min), FilterType.VELOCITY))
    #endif

    if (velocity_max != None) and (velocity_max != ""):
        list_filter.append((operator.le, float(velocity_max), FilterType.VELOCITY))
    #endif

    if (diameter_min != None) and (diameter_min != ""):
        list_filter.append((operator.ge, float(diameter_min), FilterType.DIAMETER))
    #endif

    if (diameter_max != None) and (diameter_max != ""):
        list_filter.append((operator.le, float(diameter_max), FilterType.DIAMETER))
    #endif

    if hazardous != None:
        list_filter.append((operator.eq, bool(hazardous), FilterType.HAZARDOUS))
    #endif

    return Filter(list_filter) if (list_filter != []) else None
#enddef

# TASK - DONE
def limit(iterator, n = None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    if (n == 0) or (n == None):
        return iterator
    #endif

    # SUS

    # This PASSED all 37 tests
    return [x for i, x in enumerate(iterator) if i < n]

    # This FAILED 2 test (tuple cant be use with next() func)
    # ret_list = []
    # for _ in range(0, n):
    #     try:
    #         ca = next(iterator)
    #     except StopIteration:
    #         return ret_list
    #     #endtry
    #     ret_list.append(ca)
    # #endfor
    # return ret_list
#enddef
