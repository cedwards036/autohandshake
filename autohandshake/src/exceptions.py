class InvalidURLError(Exception):
    """Raised when a Page or Handshake session is passed an invalid Handshake URL"""
    pass

class WrongPageForMethodError(Exception):
    """Raised when a Page method is called when the browser is not on the correct page"""
    pass

class BrowserTimeoutError(Exception):
    """Raised when a HandshakeBrowser waits too long for something to happen"""
    pass