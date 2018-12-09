import api.filemanagement
import api.networkmanagement
import api.networktraining

"""
Is used to register primary APIs for the entire program in one place. Does not take any arguments.
Any other APIs that need to be registered can be registered separately.
"""
def register_all_apis():
    api.filemanagement.register_all_apis()
    api.networkmanagement.register_all_apis()
    api.networktraining.register_all_apis()
