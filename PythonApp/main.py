import re
import traceback
import sys

import apiregistrar
import api.apiregistry as apiregistry
from api.responsemodels.baseresponse import SuccessResponse, FailureResponse

command_pieces_regex = r"([^\"]\S*|\".*?\")\s*"

"""
Gets all command pieces, such as by ignoring spaces inside of quotes.
"""
def get_command_pieces(full_command):
    if full_command.count('"') % 2 > 0:
        raise Exception("Invalid number of quotation marks in command")

    full_args = re.findall(command_pieces_regex, full_command)

    for i in range(len(full_args)):
        if full_args[i].startswith('"'):
            full_args[i] = full_args[i][1:-1]

    return full_args

"""
Runs the main program
"""
def main():
    apiregistrar.register_all_apis()

    should_show_stacktrace = False

    while True:
        try:
            full_command = input()
            full_args = get_command_pieces(full_command)

            action_name = full_args[0]
            if action_name == "quit":
                print(SuccessResponse())
                break # Breaking will kill the loop and hence the program
            if action_name == "toggle_stacktrace":
                should_show_stacktrace = not should_show_stacktrace
                print(SuccessResponse())
                continue

            api_action = apiregistry.get_registered_action(action_name)
            action_response = None

            if api_action["arg_parser"] is not None:
                action_args = api_action["arg_parser"].parse_args(full_args[1:])
                action_response = api_action["function"](**vars(action_args))
            else:
                action_response = api_action["function"]()

            print(action_name + "," + str(action_response))
        except BaseException as ex:
            if should_show_stacktrace:
                print(action_name + "," + str(FailureResponse(traceback.format_exc())))
            else:
                print(action_name + "," + str(FailureResponse(str(ex))))

if __name__ == "__main__":
    main()
