import BaseAuthenticator from 'ember-simple-auth/authenticators/base';
import ENV from 'client/config/environment';

export default class CustomTokenAuthenticator extends BaseAuthenticator {
    async restore(data) {
        if (data && data.token) {
            return data;
        }
        return { token: null };
    }

    async authenticate(tokenPromise) {
        // return new Promise((resolve) => setTimeout(resolve, 1000)); // Simulated delay
        const data = await tokenPromise;
        return { token: data.token };
    }
}
