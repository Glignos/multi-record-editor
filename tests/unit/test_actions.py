# This is a test for the actions
from multiedit import actions


def test_action_adding():
    record = {
        'a': [{'bla': ['val5', 'val4']}, {'bla': ['val1', 'val6']},
              {'bla': ['val2']}, {'bla': ['val3']}], 'b': {'c': {'d': 'pong'}}
    }
    expected_map = {
        'a': [{'bla': ['val5', 'success']}, {'bla': ['val1', 'val6']},
              {'bla': ['val2']}, {'bla': ['val3']}], 'b': {'c': {'d': 'pong'}}
    }
    key = 'a/bla'
    action = 'update'
    values_to_check = ['val4']
    value = 'success'
    assert actions.run_action({}, record, key, action, value, values_to_check)\
        == expected_map
