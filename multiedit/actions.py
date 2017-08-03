"""This is the code used for applying the curator actions to the records."""


def run_action(schema, record, key, action, value, values_to_check):
    """Initial function to run the recursive one."""
    keys = key.split('/')
    apply_action(schema, record, keys, action, values_to_check, value)
    return record


def apply_action(schema, record, keys, action,
                 values_to_check, value_to_input):
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
        record[key] = create_schema_record(schema, keys, value_to_input)
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
                apply_action(new_schema, array_record, new_keys, action,
                             values_to_check, value_to_input)
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
            apply_action(new_schema, record[key], new_keys, action,
                         values_to_check, value_to_input)


def create_schema_record(schema, path, value):
    """Object creation in par with the schema."""
    record = {}
    temp_record = record
    if schema['type'] == 'array':
        schema = schema['items']['properties']
    elif schema['type'] == 'object':
        schema = schema['properties']
    for key in path:
        schema = schema[key]
        if schema['type'] == 'object':
            schema = schema['properties'][key]
            temp_record[key] = {}
            temp_record = temp_record[key]

        elif schema['type'] == 'array':
            if schema['items']['type'] == 'object':
                schema = schema['items']['properties']
                temp_record[key] = [{}]
            temp_record = temp_record[key][0]
    temp_record[path[-1]] = value
    if isinstance(record[path[0]], list):
        return record[path[0]][0]
    else:
        return record[path[0]]
