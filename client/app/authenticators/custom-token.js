import BaseAuthenticator from 'ember-simple-auth/authenticators/base';
import ENV from 'client/config/environment';

export default class CustomTokenAuthenticator extends BaseAuthenticator {
    async restore(data) {
        if (data && data.token) {
            return data;
        }
        return { token: null };
    }

    async authenticate(username, password) {
        try {
            const response = await fetch(`${ENV.apiHost}/api/login`, {
                method: 'POST',
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                return;
            }

            const data = await response.json();
            return { token: data.token };
        } catch (error) {
            return error;
        }
    }
}
