```python
class ControlVars:
    # Optional: Replaces keys in the object to unmarshal before
    # passing to __init__()
    # Useful for keys that are not valid Python variable names
    _unmarshal_key_swap = {
        "C": "c",
    }
    # Optional: Renames keys on the fly when marshalling.
    # If unmarshalling doesn't map multiple keys to the same value,
    # you can simply use:
    # _marshal_key_swap = {v: k for k, v in _unmarshal_key_swap.items()}
    _marshal_key_swap = {
        "c": "C",
    }
    # Optional: Ignores these members when marshalling
    _marshal_exclude = [
        'z',
    ]
    # Optional: Instead of using '_marshal_exclude', you can explicitly
    # exclude all keys that are not part of __init__().
    # Note:
    #     - This will cause _marshal_exclude to be ignored
    #     - The __init__ args must match the class member names

    # _marshal_only_init_args = True

    # Optional: Set to False to forbid extra keys from being present in
    # the object to unmarshal.  Defaults to True if not present.
    # This overrides allow_extra_keys=True in unmarshal_dict (called
    # by various unmarshal_* functions), and is the only way to
    # control extra keys from within nested objects

    # _unmarshal_allow_extra_keys = False

    # Optional: Exclude any key whose value is None when marshalling
    # The __init__ args this may affect should have a default value of None
    # and type_assert(..., allow_none=True) in the assignment

    _marshal_exclude_none = True

    # Optional: Exclude specific keys if their value is None when marshalling
    # The corresponding __init__ args should have a default value of None
    # and type_assert(..., allow_none=True) in the assignment
    # There is no need to set this if _marshal_exclude_none == True

    # _marshal_exclude_none_keys = ['key1', 'key2']

    # CSV

    # Using this when marshalling to CSV or other list types will
    # make this value the first column on every row.  Use this
    # when you are using multiple types as rows in a single CSV
    # document
    _marshal_list_row_header = "row_header"

    # map row headers to input arguments and types.
    # The __init__ args should all use type_assert_iter and accept a list
    # as an argument
    _unmarshal_csv_map = {
        # The value of a row header in the CSV
        'row_header': {
            # The name of the __init__ argument @row_header maps to
            'arg_name': '__init__ arg name',
            # This type should implement _marshal_list_row_header
            'type': Class,  # Or a factory function
        }
    }

    # Set a default input argument and type when no recognized header is in the
    # row.  This type should not implement _marshal_list_row_header
    _unmarshal_csv_default_arg = {
        'arg_name': '__init__ arg name',
        'type': Class,  # Or a factory function
    }

    # Set a row header as a singleton (non-list/tuple) field
    # Multiple rows matching this will overwrite each other.
    _unmarshal_csv_singletons = {
        'row_header': {
            'arg_name': '__init__ arg name',
            'type': Class,  # Or a factory function
        }
    }

    # Specify that the object should not be iterated using __iter__, but
    # marshalled into a list of key/value pairs in the format:
    # field_name,value
    _marshal_csv_dict = True

    def __init__(self, c, z="test", none=None):
        self.c = type_assert(c, float)
        # this will be ignored when marshalling because
        # of _marshal_exclude
        self.z = type_assert(z, str)
        # this will be ignored when marshalling because
        # of _marshal_exclude_none==True, assuming the
        # default value of None is used
        self.none = type_assert(none, str, allow_none=True)
```
