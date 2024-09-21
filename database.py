"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""

from models import NearEarthObject, CloseApproach
from filters import Filter

# INFO
""" For those who reading/grading this, I come from C and this syntax of tabs is really bothering me so I'mma just add the tailing end for everything =)))) """
""" You can quickly skim through what I changed by the keyword 'TASK - DONE' ;) """

# TASK - DONE
class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    # TASK - DONE
    def __init__(self, neos: list[NearEarthObject], approaches: list[CloseApproach]):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection (a list) of `NearEarthObject`s.
        :param approaches: A collection (a list) of `CloseApproach`es.
        """

        self._neos = neos
        self._approaches = approaches

        # We need to create 2 dictionary for quick query: {designator:index} and {name:index}
        # with Index as the index of the neo instance in the neos list

        self._dict_des_inx = {}
        self._dict_name_inx = {}

        # Populate all dictionary
        inx = 0
        for neo in self._neos:
            self._dict_des_inx[neo.designation] = inx
            if neo.name != None:
                self._dict_name_inx[neo.name] = inx
            # endif
            inx += 1
        #endfor

        for ca in self._approaches:
            temp_neo = self.get_neo_by_designation(ca._designation)
            if temp_neo != None:
                ca.neo = temp_neo
                temp_neo.approaches.append(ca)
            #endif
        #endfor
    #enddef

    # TASK - DONE
    def get_neo_by_designation(self, designation: str) -> NearEarthObject:
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        # Simply query dict to get instance
        index_value = self._dict_des_inx.get(designation, -1)
        if index_value >= 0:
            return self._neos[index_value]
        #endif
        return None
    #enddef

    # TASK - DONE
    def get_neo_by_name(self, name: str) -> NearEarthObject:
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        # Simply query dict to get instance
        index_value = self._dict_name_inx.get(name, -1)
        if index_value >= 0:
            return self._neos[index_value]
        #endif
        return None
    #enddef

    # TASK - DONE
    def query(self, filters: Filter = None):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """

        if filters != None:
            for approach in self._approaches:
                if filters.check(approach) == True:
                    yield approach
                #endif
            #endfor
        else:
            for approach in self._approaches:
                yield approach
            #endfor
        #endif
    #enddef
#endclass

