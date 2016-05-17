"""Ascii menu class"""
from __future__ import print_function
from cloudmesh_client.common.Printer import Printer

from builtins import input


def ascii_menu(title=None, menu_list=None):
    """
    creates a simple ASCII menu from a list of tuples containing a label
    and a functions reference. The function should not use parameters.
    :param title: the title of the menu
    :param menu_list: an array of tuples [('label', f1), ...]
    """
    if not title:
        title = "Menu"

    n = len(menu_list)

    def display():
        index = 1
        print()
        print(title)
        print(len(title) * "=")
        print()
        for label, function in menu_list:
            print("    {0:>3} - {1}".format(index, label))
            index += 1
        print("    q - quit")
        print()
        print()

    display()
    running = True
    while running:
        result = input("Select between {0} - {1}: ".format(1, n))
        print("<{0}>".format(result))
        if result.strip() in ["q"]:
            running = False
        else:
            try:
                result = int(result) - 1
                if 0 <= result < n:
                    (label, f) = menu_list[result]
                    print("EXECUTING:", label, f.__name__)
                    f()
                else:
                    print("ERROR: wrong selection")
            except Exception as e:
                print("ERROR: ", e)
        display()


def menu_return_num(title=None, menu_list=None, tries=1, with_display=True):
    """
    creates a simple ASCII menu from a list of labels
    :param title: the title of the menu
    :param menu_list: a list of labels to choose
    :param tries: num of tries till discard
    :return: choice num (head: 0), quit: return 'q'
    """
    if not title:
        title = "Menu"

    n = len(menu_list)

    def display():
        index = 1
        print()
        print(title)
        print(len(title) * "=")
        print()
        for label in menu_list:
            print("    {0:>3} - {1}".format(index, label))
            index += 1
        print("      q - quit")
        print()
        print()

    display()
    while tries > 0:
        # display()
        result = input("Select between {0} - {1}: ".format(1, n))
        if result == "q":
            return 'q'
        else:
            try:
                result = int(result)
            except:
                print("invalid input...")
                tries -= 1
                continue
            if 0 < result <= n:
                print("choice {0} selected.".format(result))
                return result - 1
            else:
                print("ERROR: wrong selection")

    return 'q'


def num_choice(n, tries=1):

    while tries > 0:
        # display()
        result = input("Select between {0} - {1}: ".format(1, n))
        if result == "q":
            return 'q'
        else:
            try:
                result = int(result)
            except:
                print("invalid input...")
                tries -= 1
                continue
            if 0 < result <= n:
                print("choice {0} selected.".format(result))
                return result - 1
            else:
                print("ERROR: wrong selection")

    return 'q'


def dict_choice(d):
    if d is None:
        return None

    elements = dict(d)
    i = 1
    for e in d:
        elements[e]["id"] = i
        i += 1
    #   pprint(d)
    if elements != {}:
        # noinspection PyPep8
        print(Printer.write(elements,
                            order=["id",
                                  "name",
                                  "comment",
                                  "uri",
                                  "fingerprint",
                                  "source"],
                            output="table",
                            sort_keys=True))
    else:
        print("ERROR: No keys in the database")
        return

    n = num_choice(i - 1, tries=10) + 1
    element = None
    for e in elements:
        if str(elements[e]["id"]) is str(n):
            element = elements[e]
            break
    return element
