import json
import copy


def get_json_from_file(file_path):
    """
    From a given file name, return either an array of dictionaries or a dictionary.
    :param file_path: The file path of the file (relative or absolute). 
    :return: The JSON object loaded from the file (must be valid JSON). Returned as a 
             Python dictionary or an array of dictionary if the given JSON is an array.
    """
    with open(file_path) as data_file:
        return json.load(data_file)


def inner_join(left_json_array, right_json_array, left_key, right_key):
    """
    Perform an "inner join" with two json arrays with 
    the condition "leftObject[leftKey] = rightObject[rightKey]". The resulting array contains the
    intersection of both arrays using the previously mentioned condition and merge both objects 
    together.
    NOTE: If right_json_array's objects contain one or more key the 
          same as left_json_array's objects, they will be ignored.
          As like every time you use JSON, order is not necessarily kept.
    :param left_json_array: The array of the "left" objects.
    :param right_json_array: The array of the "right" objects.
    :param left_key: The key of the left objects to use to join the right objects with. 
    :param right_key: The key of the right objects to use to join the left objects with.
    :return: An array containing the inner-joined objects.
    """
    resulting_array = []
    left_objects = __populate_objects_dictionary(left_json_array, left_key)

    for right_json_object in right_json_array:
        if right_json_object[right_key] in left_objects:
            __merge_and_join_objects(left_objects[right_json_object[right_key]], right_json_object,
                                     resulting_array)

    return resulting_array


def full_outer_join(left_json_array, right_json_array, left_key, right_key):
    """
        Perform an "outer join" with two json arrays with 
        the condition "leftObject[leftKey] = rightObject[rightKey]". The resulting array contains the
        union of both arrays. If the condition is met, merge both objects.
        NOTE: If right_json_array's objects contain one or more key the 
              same as left_json_array's objects, they will be ignored.
              As like every time you use JSON, order is not necessarily kept.
        :param left_json_array: The array of the "left" objects.
        :param right_json_array: The array of the "right" objects.
        :param left_key: The key of the left objects to use to join the right objects with. 
        :param right_key: The key of the right objects to use to join the left objects with.
        :return: An array containing the outer-joined objects.
        """
    resulting_array = []
    already_joined_left_object_keys = {}
    left_objects = __populate_objects_dictionary(left_json_array, left_key)

    for right_json_object in right_json_array:
        if right_json_object[right_key] in left_objects:
            __merge_and_join_objects(left_objects[right_json_object[right_key]], right_json_object,
                                     resulting_array)
            already_joined_left_object_keys[right_json_object[right_key]] = True
        else:
            resulting_array.append(right_json_object)

    for key in already_joined_left_object_keys.keys():
        left_objects[key] = None

    __add_unjoined_objects(left_objects, resulting_array)

    return resulting_array


def __merge_objects(left_json_object, right_json_object):
    """
    Takes every key of both provided objects and create a new object with all the keys in it.
    NOTE: If right_json_object has one or more key that is the same as left_json_object, 
          it will be IGNORED.
    :param left_json_object: The object to be merged with the right_json_object
    :param right_json_object: The object to merge to the left_json_object
    :return: The merged objects as one object. 
    """
    merged_object = copy.deepcopy(right_json_object)
    for key, value in left_json_object.items():
        merged_object[key] = value
    return merged_object


def __merge_and_join_objects(left_objects_to_merge, right_json_object, merged_objects):
    """
    Foreach element in left_objects_to_merge, merge right_json_object to it and appends the result 
    in merged_objects.
    SIDE EFFECT ON MERGED_OBJECTS.
    :param left_objects_to_merge: The array of objects to merge with right_json_object, 
                                  one at the time. 
    :param right_json_object:  The object to merge with left_objects_to_merge, one at the time.
    :param merged_objects: The merged objects dictionary. Will have more
                           elements after the routine call.
    """
    for left_json_object in left_objects_to_merge:
        merged_objects.append(__merge_objects(left_json_object, right_json_object))


def __populate_objects_dictionary(json_array, key):
    """
    Builds a dictionary of objects using json_array[i][key] as key and an array containing all the 
    elements with the same key as value. 
    Example: json_array = [
                            {"a": "myKey1", "b": "First one"},
                            {"a": "myKey2", "b": "Second one"},
                            {"a": "myKey1", "b": "Third one"}
                          ] 
             key = "a"
             WILL OUTPUT:
                         {
                            "myKey1": [
                                        {"a": "myKey1", "b": "First one"},
                                        {"a": "myKey1", "b": "Third one"}
                                      ],
                            "myKey2": [
                                        {"a": "myKey2", "b": "Second one"}
                                      ]
                         }
    :param json_array: The array of objects to use.
    :param key: The key of the json object to use to build the dictionary.
    :return: objects_dictionary: The dictionary that has just been created.
    """
    objects_dictionary = {}
    for left_json_object in json_array:
        if left_json_object[key] in objects_dictionary:
            objects_dictionary[left_json_object[key]].append(left_json_object)
        else:
            objects_dictionary[left_json_object[key]] = [left_json_object]
    return objects_dictionary


def __add_unjoined_objects(unjoined_objects_dictionary, resulting_array):
    """
    For each element in unjoined_objects_dictionary, add it in resulting_array.
    Ex: unjoined_objects_dictionary = {
          1 => None,
          2 => [{anObject}],
          3 => [{anotherObject}, {aThirdObject}]
        }
        Then, {anObject}, {anotherObject} and {aThirdObject} will be appended to resulting_array.
    :param unjoined_objects_dictionary: The dictionary containing the unjoined objects 
    :param resulting_array: The array in which to add unjoined objects.
    """
    for left_object_array in unjoined_objects_dictionary.values():
        if left_object_array:
            resulting_array += left_object_array
