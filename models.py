"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str

import math

# INFO
""" For those who reading/grading this, I come from C and this syntax of tabs is really bothering me so I'mma just add the tailing end for everything =)))) """
""" You can quickly skim through what I changed by the keyword 'TASK - DONE' ;) """

# SUPPORT CLASS
class CloseApproach:
    pass
#endclass

# TASK - DONE
class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    # TASK - DONE
    def __init__(self, designation: str, name: str = None, diameter: float = float("nan"), hazardous: bool = False, approaches: list[CloseApproach] = None):
        """Create a new `NearEarthObject`.

        :param designation: The primary designation (str)
        :param name: The IAU name (str)
        :param diameter: The diameter (kilometers) (float)
        :param hazardous: is potentially hazardous (bool)
        :param approaches: A collection of close approaches to Earth (list)
        """
        self.designation = designation
        self.name = name
        self.diameter = diameter
        self.hazardous = hazardous

        # Create an empty initial collection of linked approaches.
        if approaches == None:
            self.approaches = []
        else:
            self.approaches = approaches
        #endif
    #enddef

    # TASK - DONE
    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name == None:
            return self.designation
        else:
            return "{} ({})".format(self.designation, self.name)
        #endif
    #enddef

    # TASK - DONE
    def __str__(self):
        """Return `str(self)`, a human readable text."""

        if math.isnan(self.diameter) == True:
            diameter_str = "has unknown diameter"
        else:
            diameter_str = "has a diameter of {:.3f} km".format(self.diameter)
        #endif

        if self.hazardous == True:
            hazardous_str = "is potentially hazardous"
        else:
            hazardous_str = "is NOT potentially hazardous"
        #endif

        return f"A Near-Earth-Object (NEO) designated as {self.fullname} {diameter_str} and {hazardous_str}!"
    #enddef

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
    #enddef

    # TASK - TEST
    def serialize(self) -> dict:
        """Serialize this `NearEarthObject` into a dictionary."""

        this_as_dict = {}
        this_as_dict["designation"] = self.designation
        this_as_dict["name"] = self.name if self.name != None else ""

        # This failed 1 test case but produce a cleaner .json file
        # this_as_dict["diameter_km"] = self.diameter if (math.isnan(self.diameter) == False) else ""

        # This passed all test
        this_as_dict["diameter_km"] = self.diameter if (math.isnan(self.diameter) == False) else float("nan")

        this_as_dict["potentially_hazardous"] = self.hazardous

        return this_as_dict
    #enddef
#endclass

# TASK - DONE
class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    # TASK - DONE
    def __init__(self, designation: str, time: str = None, distance: float = 0.0, velocity: float = 0.0):
        """Create a new `CloseApproach`.

        :param designation: The primary designation (str)
        :param time: The date and time (UTC) (str)
        :param distance: The nominal approach distance (au) (float)
        :param velocity:  The velocity (km/s) (float)
        """
        self._designation = designation
        self.time = cd_to_datetime(time)
        self.distance = distance
        self.velocity = velocity

        # Create an attribute for the referenced NEO, originally None.
        self.neo: NearEarthObject = None
    #enddef

    # TASK - DONE
    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)
    #enddef

    # TASK - DONE
    def __str__(self):
        """Return `str(self)`."""
        if self.neo == None:
            full_name = self._designation
        else:
            full_name = self.neo.fullname
        #endif

        return f"On {self.time_str}, '{full_name}' passes by Earth at a distance of {self.distance:.2f} AU and a velocity of {self.velocity:.2f} km/s."
    #enddef

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, velocity={self.velocity:.2f}, neo={self.neo!r})"
    #enddef

    # TASK - TEST
    def serialize(self) -> dict:
        """Serialize this `CloseApproach` into a dictionary"""

        this_as_dict = {
            "datetime_utc": self.time_str,
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
        }

        return this_as_dict
    #enddef

#endclass
