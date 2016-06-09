class ProfileNotFound(Exception):
    """ Exception if the linkedin url points to the linkedin not found page """
    pass

class NotAProfile(Exception):
    """ Exception raised if you pass a non linkedin profile as url """
    pass

class ServerIpBlacklisted(Exception):
    pass

class BadStatusCode(Exception):
    pass