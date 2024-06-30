import OAuth2PasswordGrant from 'ember-simple-auth/authenticators/oauth2-password-grant';
import ENV from 'client/config/environment';

export default class CustomTokenAuthenticator extends OAuth2PasswordGrant {
    async restore(data) {
        if (data && data.token) {
            return data;
        }
        return { token: null };
    }

    authenticate(token) {
        return { token: token };
    }
}
