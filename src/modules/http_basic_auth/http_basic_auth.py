import base64

from functools import wraps
from flask import current_app, request, Response


class HttpBasicAuth(object):
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)
        else:
            self.app = None

        # --- initialize the 
        self._check_credentials = self._default_check_credentials


    def init_app(self, app):
        # --- initialize parameters from app.config
        app.config.setdefault('BASIC_AUTH_FORCE', False)
        app.config.setdefault('BASIC_AUTH_REALM', '')

    def _default_check_credentials(self, username, password):
        if self.app.config['BASIC_AUTH_USERNAME'] == username and self.app.config['BASIC_AUTH_PASSWORD'] == password:
            return True
        
        return False
    
    def check_credentials_loader(self, func):
        self._check_credentials = func
        return func

    # -- decorator @basic_auth_required
    def auth_required(self, f): 
        @wraps(f)

        def decorated(*args, **kwargs):
            auth = request.authorization

            if not auth:
                return Response("No Basic Credentials provided", 401)
            elif not self._check_credentials(auth.username, auth.password):
                # return self.challenge()
                return Response(
                    "Authentication Failed", 401
                )

            return f(*args, **kwargs)

        return decorated
    

    # -- this is not necessry (it will prompt a dialog at browser for login credentials)
    def challenge(self):
        if not current_app.config['BASIC_AUTH_REALM']:
            realm = 'Authentication Required'
        else:
            realm = current_app.config['BASIC_AUTH_REALM']

        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials',
            401,
            {'WWW-Authenticate': 'Basic realm="%s"' % realm}
        )
