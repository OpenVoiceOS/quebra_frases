# The following lines are replaced during the release process.
# START_VERSION_BLOCK
VERSION_MAJOR = 0
VERSION_MINOR = 3
VERSION_BUILD = 8
VERSION_ALPHA = 1
# END_VERSION_BLOCK

__version__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_BUILD}"
if VERSION_ALPHA and int(VERSION_ALPHA) > 0:
    __version__ += f"a{VERSION_ALPHA}"
