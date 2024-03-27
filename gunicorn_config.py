"""Gunicorn Config for Print Manager API Service"""

import multiprocessing

workers = 4
bind = "unix:kumpe3dapi.sock"  # pylint: disable=invalid-name
umask = 0o007  # pylint: disable=invalid-name
reload = True  # pylint: disable=invalid-name

# logging
accesslog = "-"  # pylint: disable=invalid-name
errorlog = "-"  # pylint: disable=invalid-name
