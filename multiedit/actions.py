"""This is the code used for applying the curator actions to the records."""

import re


def run_action(schema, record, key, action, value,
               values_to_check, regex, where_key, where_value):
    """Initial function to run the recursive one."""
    keys = key.split('/')
    if where_key:
        where_keys = where_key.split('/')
    else:
        where_keys = []
    apply_action(schema, record, keys, action,
                 values_to_check, regex, value, where_keys, where_value)
    return record


def apply_action(schema, record, keys, action,
                 values_to_check, regex, value_to_input,
                 where_keys, where_value):
    """Recursive function to change a record object."""
    new_keys = keys[:]
    key = new_keys.pop(0)
    new_schema = {}
    if schema:  # fixme in a more stable version the
        #  schema should always be present
        if schema['type'] == 'object':
            new_schema = schema['properties'][key]
        elif schema['type'] == 'array':
            new_schema = schema['items']['properties'][key]
    if not record.get(key) and action == 'add':
        record.update(create_schema_record(schema, keys, value_to_input))
        return
    if len(where_keys) != 0 and key != where_keys[0]:
        if check_value(record, where_keys, where_value) == 0:
            return
        else:
            where_keys = []
    if isinstance(record[key], list):
        for index, array_record in enumerate(record[key]):
            if len(new_keys) == 0:
                if action == 'update':
                    if regex and re.search(re.escape(values_to_check[0]), record[key][index]):
                        record[key][index] = value_to_input
                    elif array_record in values_to_check:
                        record[key][index] = value_to_input
                elif action == 'add':
                    record[key].append(value_to_input)
                    return
                elif action == 'delete':
                    if len(values_to_check) == 0\
                            or array_record in values_to_check:
                        record[key].pop(index)
            else:
                if len(where_keys) != 0:
                    new_where_keys = where_keys[:]
                    new_where_keys.pop(0)
                else:
                    new_where_keys = where_keys
                apply_action(new_schema, array_record, new_keys, action,
                             values_to_check, regex, value_to_input,
                             new_where_keys, where_value)
                if action == 'delete':  # dont leave empty objects
                    if not record[key]:
                        del(record[key])
    else:
        if len(new_keys) == 0:
            if action == 'update':
                if regex and re.search(re.escape(values_to_check[0]), record[key]):
                    record[key] = value_to_input
                elif record[key] in values_to_check:
                    record[key] = value_to_input
            elif action == 'add':
                record[key] = value_to_input
                return
            elif action == 'delete':
                if len(values_to_check) == 0 \
                        or record[key] in values_to_check:
                    del(record[key])
        else:
            if len(where_keys) != 0:
                new_where_keys = where_keys[:]
                new_where_keys.pop(0)
            else:
                new_where_keys = where_keys
            apply_action(new_schema, record[key], new_keys, action,
                         values_to_check, regex, value_to_input,
                         new_where_keys, where_value)
            if action == 'delete':
                if not record[key]:
                    del (record[key])


def create_schema_record(schema, path, value):
    """Object creation in par with the schema."""
    record = {}
    temp_record = record
    new_schema = schema
    if new_schema['type'] == 'array':
        new_schema = new_schema['items']['properties']
    elif new_schema['type'] == 'object':
        new_schema = new_schema['properties']
    for key in path:
        new_schema = new_schema[key]
        if new_schema['type'] == 'object':
            new_schema = schema['properties']
            temp_record[key] = {}
            temp_record = temp_record[key]

        elif new_schema['type'] == 'array':
            if new_schema['items']['type'] == 'object':
                new_schema = new_schema['items']['properties']
                temp_record[key] = [{}]
                temp_record = temp_record[key][0]
    temp_record[path[-1]] = value
    return record


def check_value(record, keys, value_to_check):
    """Where continues to find the value."""
    new_keys = keys[:]
    key = new_keys.pop(0)
    if key not in record:
        return False
    temp_record = record[key]
    if isinstance(temp_record, list):
        for index, array_record in enumerate(temp_record):
            if len(new_keys) == 0:
                if array_record == value_to_check:
                    return True
            else:
                if check_value(array_record,
                               new_keys, value_to_check):
                    return True
    else:
        if len(new_keys) == 0:
            if temp_record == value_to_check:
                return True
        else:
            return check_value(temp_record,
                               new_keys, value_to_check)
    return False
