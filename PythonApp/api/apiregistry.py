__api_actions = {}

"""
Registers an action to the registry
"""
def register_action(action_name, action_function, arg_parser):
    if action_name in __api_actions:
        raise Exception(f"Action with name {action_name} already registered.")
    __api_actions[action_name] = {
        "function": action_function,
        "arg_parser": arg_parser
    }

"""
Gets an action that has been registered or throws
"""
def get_registered_action(action_name):
    if not action_name in __api_actions:
        raise Exception(f"Action with name {action_name} not yet registered.")
    return __api_actions[action_name]