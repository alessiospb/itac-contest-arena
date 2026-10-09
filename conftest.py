pytest_plugins = (
    "fixtures.browsers",
    "fixtures.pages",
)

import logging, os

def pytest_configure(config):
    project_root = os.path.dirname(os.path.abspath(__file__))
    debug_path = os.path.join(project_root, "debug.log")
    formatter = logging.Formatter('%(asctime)s %(name)s: [%(levelname)s] %(name)s: %(message)s')


    logger_debug = logging.getLogger("DebugLogger")
    logger_debug.setLevel(logging.DEBUG)
    debug_handler = logging.FileHandler(debug_path, mode='w')
    debug_handler.setFormatter(formatter)
    logger_debug.addHandler(debug_handler)
    config.logger_debug = logger_debug

