import base64
from oauth2_provider.models import AccessToken

from channels.db import database_sync_to_async
from channels.auth import UserLazyObject, AuthMiddleware
from channels.sessions import CookieMiddleware, SessionMiddleware


@database_sync_to_async
def get_user_by_access_token(scope):
    """
    Return the user model instance associated with the given scope.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    from django.contrib.auth.models import AnonymousUser

    if (access_token := scope.get('access_token', None)) is not None:
        user = AnonymousUser()
        access_token = AccessToken.objects.filter(token=access_token).first()
        if access_token and access_token.is_valid():
                user = access_token.user
        return user
    else:
        raise ValueError("Cannot find access_token in header.")


class CustomOauth2SubProtocolMiddleware(AuthMiddleware):

    def populate_scope(self, scope):
        if len(scope["subprotocols"]) > 1 and "Bearer" in scope["subprotocols"]:
            scope['access_token'] = scope["subprotocols"][1]

        if "user" not in scope:
            scope["user"] = UserLazyObject()

    async def resolve_scope(self, scope):
        scope["user"]._wrapped = await get_user_by_access_token(scope)

def CustomAuthSubProtocolMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(CustomOauth2SubProtocolMiddleware(inner)))
