edit docs/conf.py and add:

import pkg_resources
version = pkg_resources.get_distribution('PyOriginTools').version
release = pkg_resources.get_distribution('PyOriginTools').version