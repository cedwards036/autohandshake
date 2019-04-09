class InvalidURLError(Exception):
    """Raised when a Page or Handshake session is passed an invalid Handshake URL"""
    pass

class WrongPageForMethodError(Exception):
    """Raised when a Page method is called when the browser is not on the correct page"""
    pass

class BrowserTimeoutError(Exception):
    """Raised when a HandshakeBrowser waits too long for something to happen"""
    pass

class NoSuchElementError(Exception):
    """Raised when a HandshakeBrowser attempts to find an element that doesn't exist"""
    pass

class InvalidEmailError(Exception):
    """Raised when attempting to log into Handshake with an invalid email"""
    pass

class InvalidPasswordError(Exception):
    """Raised when attempting to log into Handshake with an invalid password"""
    pass