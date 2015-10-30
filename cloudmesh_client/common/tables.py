"""Convenient methods and classes to print tables"""
from __future__ import print_function

import json

from prettytable import PrettyTable
import yaml
from cloudmesh_base.util import convert_from_unicode


def list_printer(l,
                 order=None,
                 header=None,
                 output="table",
                 sort_keys=True,
                 show_none="", key="name"):
    d = {}
    for c in l:
        name = c[key]
        d[name] = c

    return dict_printer(d,
                        order=order,
                        header=header,
                        sort_keys=sort_keys,
                        output=output,
                        show_none=show_none)


def dict_printer(d,
                 order=None,
                 header=None,
                 output="table",
                 sort_keys=True,
                 show_none=""):
    """
    TODO
    :param d: A a dict with dicts of the same type.
    :type d: dict
    :param order:The order in which the columns are printed.
                The order is specified by the key names of the dict.
    :type order:
    :param header: The Header of each of the columns
    :type header: list or tuple of field names
    :param output: type of output (table, csv, json, yaml or dict)
    :type output: string
    :param sort_keys:
    :type sort_keys: bool
    :return:
    """
    if output == "table":
        if d == {}:
            return None
        else:
            return dict_table_printer(d, order=order, header=header,
                                      sort_keys=sort_keys)
    elif output == "csv":
        return dict_csv_printer(d, order=order, header=header,
                                sort_keys=sort_keys)
    elif output == "json":
        return json.dumps(d, sort_keys=sort_keys, indent=4)
    elif output == "yaml":
        return yaml.dump(convert_from_unicode(d), default_flow_style=False)
    elif output == "dict":
        return d
    else:
        return "UNKOWN FORMAT. Please use table, csv, json, yaml, dict."


def dict_csv_printer(d,
                     order=None,
                     header=None,
                     sort_keys=True):
    """
    prints a table in csv format

    :param d: A a dict with dicts of the same type.
    :type d: dict
    :param order:The order in which the columns are printed.
                The order is specified by the key names of the dict.
    :type order:
    :param header: The Header of each of the columns
    :type header: list or tuple of field names
    :param sort_keys: TODO: not yet implemented
    :type sort_keys: bool
    :return: a string representing the table in csv format
    """
    first_element = d.keys()[0]

    def _keys():
        return d[first_element].keys()

    def _get(element, key):
        try:
            tmp = str(d[element][key])
        except:
            tmp = ' '
        return tmp

    if d is None or d == {}:
        return None

    if order is None:
        order = _keys()

    if header is None and order is not None:
        header = order
    elif header is None:
        header = _keys()

    table = ""
    content = []
    for attribute in order:
        content.append(attribute)
    table = table + ",".join([str(e) for e in content]) + "\n"

    for job in d:
        content = []
        for attribute in order:
            try:
                content.append(d[job][attribute])
            except:
                content.append("None")
        table = table + ",".join([str(e) for e in content]) + "\n"
    return table


def dict_table_printer(d, order=None, header=None, sort_keys=True,
                       show_none=""):
    """prints a pretty table from an dict of dicts
    :param d: A a dict with dicts of the same type.
                  Each key will be a column
    :param order: The order in which the columns are printed.
                  The order is specified by the key names of the dict.
    :param header: The Header of each of the columns
    
    """
    first_element = d.keys()[0]

    def _keys():
        return d[first_element].keys()

    def _get(item, key):
        try:
            tmp = str(d[item][key])
            if tmp == "None":
                tmp = show_none
        except:
            tmp = ' '
        return tmp

    if d is None or d == {}:
        return None

    if order is None:
        order = _keys()

    if header is None and order is not None:
        header = order
    elif header is None:
        header = _keys()

    x = PrettyTable(header)

    if sort_keys:
        sorted_list = sorted(d, key=d.get)
    else:
        sorted_list = d

    for element in sorted_list:
        values = []
        for key in order:
            values.append(_get(element, key))
        x.add_row(values)
    x.align = "l"
    return x


def attribute_printer(d, header=["Attribute", "Value"], sort_keys=True,
                      output="table"):
    if output == "table":
        x = PrettyTable(header)
        if sort_keys:
            sorted_list = sorted(d, key=d.get)
        else:
            sorted_list = d

        for key in sorted_list:
            x.add_row([key, d[key]])
        x.align = "l"
        return x
    else:
        return dict_printer(d)


def print_list(l, output='table'):
    def dict_from_list(l):
        d = dict([(idx, item) for idx, item in enumerate(l)])
        return d

    if output == 'table':
        x = PrettyTable(["Index", "Host"])
        for (idx, item) in enumerate(l):
            x.add_row([idx, item])
        x.align = "l"
        x.align["Index"] = "r"
        return x
    elif output == 'csv':
        return (",".join(l))
    elif output == 'dict':
        d = dict_from_list(l)
        return d
    elif output == 'json':
        d = dict_from_list(l)
        result = json.dumps(d, indent=4)
        return result
    elif output == 'yaml':
        d = dict_from_list(l)
        result = yaml.dump(d, default_flow_style=False)
        return result
    elif output == 'txt':
        return ("\n".join(l))
