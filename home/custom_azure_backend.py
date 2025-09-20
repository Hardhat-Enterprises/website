"""
Custom Azure AD OAuth2 backend that fixes common OAuth issues
"""
from social_core.backends.azuread_tenant import AzureADTenantOAuth2
from social_core.exceptions import AuthForbidden, AuthTokenError
import logging
from django.conf import settings
import requests


class CustomAzureADTenantOAuth2(AzureADTenantOAuth2):
    """
    Custom Azure AD OAuth2 backend that handles OAuth flow properly
    """
    
    # Disable state validation for local development
    STATE_PARAMETER = False
    REDIRECT_STATE = False
    
    def get_redirect_uri(self, state=None):
        """
        Override to always return localhost redirect URI for local development
        """
        redirect_uri = 'http://localhost:8000/complete/azuread-tenant-oauth2/'
        logging.getLogger('social').debug(f"CustomAzureADTenantOAuth2.get_redirect_uri -> {redirect_uri}")
        return redirect_uri
    
    def auth_params(self, state=None):
        """
        Ensure the authorization request forces a fresh Microsoft login.
        """
        params = super().auth_params(state)
        # Force credential prompt to avoid silent SSO into previous account
        params['prompt'] = 'login'
        return params

    def validate_state(self):
        """
        Override to completely disable state validation
        """
        return None
    
    def auth_complete_params(self, state=None):
        """
        Override to ensure proper OAuth parameters are passed
        """
        params = super().auth_complete_params(state)
        
        # Ensure redirect_uri is set correctly
        if 'redirect_uri' not in params:
            params['redirect_uri'] = self.get_redirect_uri(state)

        # Also include prompt on the token step for consistency (harmless if ignored)
        params['prompt'] = 'login'
        
        safe_params = {k: ('***' if 'secret' in k.lower() or k in {'code'} else v) for k, v in params.items()}
        logging.getLogger('social').debug(f"auth_complete_params -> {safe_params}")
        return params
    
    def request_access_token(self, *args, **kwargs):
        """
        Override to handle token request errors more gracefully
        """
        try:
            return super().request_access_token(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logging.getLogger('social').error(f"OAuth token request failed with 401: {e.response.text}")
                raise AuthTokenError(self, "Invalid client credentials. Please check your Azure app registration settings.")
            raise
        except Exception as e:
            logging.getLogger('social').error(f"OAuth token request failed: {str(e)}")
            raise AuthTokenError(self, f"Authentication failed: {str(e)}")

    def get_user_details(self, response):
        details = super().get_user_details(response)
        
        # Ensure unique usernames for different users
        email = details.get('email', '')
        if email:
            # Use email as username to ensure uniqueness
            details['username'] = email
        
        safe_details = {k: (v if k not in {'access_token', 'id_token'} else '***') for k, v in details.items()}
        logging.getLogger('social').debug(f"get_user_details -> {safe_details}")
        return details
    
    def get_username(self, details):
        """
        Override to ensure unique usernames for each user
        """
        email = details.get('email', '')
        if email:
            # Use email as username to ensure uniqueness for each Deakin account
            return email
        return super().get_username(details)
    
    def social_user(self, *args, **kwargs):
        """
        Override to ensure proper user creation for each unique Microsoft account
        """
        result = super().social_user(*args, **kwargs)
        
        # Log the social user result for debugging
        if result and hasattr(result, 'user'):
            logging.getLogger('social').debug(f"social_user found existing user: {result.user.email}")
        else:
            logging.getLogger('social').debug("social_user: No existing user found, will create new user")
        
        return result
