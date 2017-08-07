"""This is the code used for applying the curator actions to the records."""


def run_action(schema, record, key, action, value, values_to_check):
    """Initial function to run the recursive one."""
    keys = key.split('/')
    apply_action(schema, record, keys, action,
                 values_to_check, value, ['ignore'], '')
    return record


def apply_action(schema, record, keys, action,
                 values_to_check, value_to_input,
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
    try:
        record[key]
        pass
    except KeyError:
        record.update(create_schema_record(schema, keys, value_to_input))
        return
    temp_record = record[key]
    if isinstance(temp_record, list):
        for index, array_record in enumerate(temp_record):
            if len(new_keys) == 0:
                if action == 'update' and array_record in values_to_check:
                    record[key][index] = value_to_input
                elif action == 'add':
                    record[key].append(value_to_input)
                    return
                elif action == 'delete' and array_record in values_to_check:
                    record[key].pop(index)
            else:
                if where_keys[0] != 'ignore' and len(where_keys) != 0\
                        and key != where_keys[0]:
                    if check_value(record, where_keys,
                                   schema, where_value) == 0:
                        return
                    else:
                        where_keys[0] == 'ignore'
                elif where_keys[0] != 'ignore':
                    new_where_keys = where_keys[:]
                    new_where_keys.pop(0)
                else:
                    new_where_keys = where_keys
                apply_action(new_schema, array_record, new_keys, action,
                             values_to_check, value_to_input,
                             new_where_keys, where_value)
                if action == 'delete':  # dont leave empty objects
                    if not record[key]:
                        del(record[key])
    else:
        if len(new_keys) == 0:
            if action == 'update' and record[key] in values_to_check:
                record[key] = value_to_input
            elif action == 'add':
                record[key] = value_to_input
                return
            elif action == 'delete' and record[key] in values_to_check:
                del(record[key])
        else:
            if where_keys[0] != 'ignore' and len(where_keys) != 0\
                    and key != where_keys[0]:
                if check_value(record, where_keys,
                               schema, where_value) == 0:
                    return
                else:
                    where_keys[0] == 'ignore'
            elif where_keys[0] != 'ignore':
                new_where_keys = where_keys[:]
                new_where_keys.pop(0)
            else:
                new_where_keys = where_keys
            apply_action(new_schema, record[key], new_keys, action,
                         values_to_check, value_to_input,
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
    # if isinstance(record[path[0]], list):
    #     return record[path[0]][0]
    # else:
    #     return record[path[0]]
    return record


def check_value(record, keys, schema, value_to_check):
    """Where continues to find the value."""
    new_keys = keys[:]
    key = new_keys.pop(0)
    new_schema = {}
    if schema:  # fixme in a more stable version the
        #  schema should always be present
        if schema['type'] == 'object':
            new_schema = schema['properties'][key]
        elif schema['type'] == 'array':
            new_schema = schema['items']['properties'][key]
    try:
        record[key]
        pass
    except KeyError:
        return 0
    temp_record = record[key]
    if isinstance(temp_record, list):
        for index, array_record in enumerate(temp_record):
            if len(new_keys) == 0:
                if array_record == value_to_check:
                    return 1
            else:
                return check_value(array_record, keys,
                                   new_schema, value_to_check)
    else:
        if len(new_keys) == 0:
            if temp_record == value_to_check:
                return 1
        else:
            return check_value(temp_record, keys, new_schema, value_to_check)
