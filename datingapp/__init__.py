import os

baseurl = "http://api.mpi2d-corp.tk"
cache_directory = ".cache/"


def init():
    global cache_directory
    import datingapp.api as api
    import datingapp.cache as cache
    import datingapp.ui as ui

    if cache_directory[-1] != "/":
        cache_directory += "/"

    # Create cache directory if it does not exist
    if not os.path.isdir(cache_directory):
        if os.path.exists(cache_directory):
            raise RuntimeError("The cache directory is a file !")
        os.makedirs(cache_directory)

    api.init(baseurl, cache_directory)
    cache.init(cache_directory)
