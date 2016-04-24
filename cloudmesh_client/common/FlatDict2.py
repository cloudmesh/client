from cloudmesh_client.common.FlatDict import FlatDict


class FlatDict2(object):

    primitive = (int, str, bool, unicode, dict, list)

    @classmethod
    def is_primitive(cls, thing):
        return type(thing) in cls.primitive

    @classmethod
    def convert(cls, obj, flatten=True):
        """
            This function converts object into a Dict optionally Flattening it
            :param obj: Object to be converted
            :param flatten: boolean to specify if the dict has to be flattened
            :return dict: the dict of the object (Flattened or Un-flattened)
        """
        dict_result = cls.object_to_dict(obj)
        if flatten:
            dict_result = FlatDict(dict_result)
        return dict_result

    @classmethod
    def object_to_dict(cls, obj):
        """
            This function converts Objects into Dictionary
        """
        dict_obj = dict()
        if obj is not None:
            if type(obj) == list:
                dict_list = []
                for inst in obj:
                    dict_list.append(cls.object_to_dict(inst))
                dict_obj["list"] = dict_list

            elif not cls.is_primitive(obj):
                for key in obj.__dict__:
                    # is an object
                    if type(obj.__dict__[key]) == list:
                        dict_list = []
                        for inst in obj.__dict__[key]:
                            dict_list.append(cls.object_to_dict(inst))
                        dict_obj[key] = dict_list
                    elif not cls.is_primitive(obj.__dict__[key]):
                        temp_dict = cls.object_to_dict(obj.__dict__[key])
                        dict_obj[key] = temp_dict
                    else:
                        dict_obj[key] = obj.__dict__[key]
            elif cls.is_primitive(obj):
                return obj
        return dict_obj
