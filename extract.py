"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach

# INFO
""" For those who reading/grading this, I come from C and this syntax of tabs is really bothering me so I'mma just add the tailing end for everything =)))) """
""" You can quickly skim through what I changed by the keyword 'TASK - DONE' ;) """

# TASK - DONE
def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection (a list) of `NearEarthObject`s.
    """
    list_of_neos = []
    neos_file = open(neo_csv_path)
    read_csv = csv.DictReader(neos_file)
    for row in read_csv:
        designator = row["pdes"]

        name = row["name"] or None

        if (row["diameter"] != "") and (row["diameter"] != None):
            diameter = float(row["diameter"])
        else:
            diameter = float("nan")
        #endif

        if row["pha"] == "Y":
            hazardous = True
        else:
            hazardous = False
        #endif

        list_of_neos.append(NearEarthObject(designator, name, diameter, hazardous))
    #endfor

    return list_of_neos
#enddef

# TASK - DONE
def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection (a list) of `CloseApproach`es.
    """
    list_of_cas = []
    cad_file = open(cad_json_path)
    read_json = json.load(cad_file)
    for row in read_json["data"]:
        # ["des","orbit_id","jd","cd","dist","dist_min","dist_max","v_rel","v_inf","t_sigma_f","h"]
        """
            Index 0 - des
            Index 3 - cd
            Index 4 - dist
            Index 7 - v_rel
        """
        # Should parse for a dictinary of {field_name, index_of_field_name}, this removes the hard-code indexes and is more flexible 
        list_of_cas.append(CloseApproach(row[0], row[3], float(row[4]), float(row[7])))
    #endfor

    return list_of_cas
#enddef
