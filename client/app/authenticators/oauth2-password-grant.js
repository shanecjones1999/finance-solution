import OAuth2PasswordGrant from 'ember-simple-auth/authenticators/oauth2-password-grant';
import ENV from 'client/config/environment';

export default class CustomTokenAuthenticator extends OAuth2PasswordGrant {
    async restore(data) {
        if (data && data.token) {
            return data;
        }
        return { token: null };
    }

    async authenticate(username, password) {
        try {
            let response = await fetch(`${ENV.apiHost}/api/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });

            if (!response.ok) {
                console.error('Unable to authenticate user.');
            }

            const data = await response.json();
            return { token: data.token };
        } catch (error) {
            return error;
        }
    }
}
