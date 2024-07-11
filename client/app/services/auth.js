import Service from '@ember/service';
import { inject as service } from '@ember/service';
import ENV from 'client/config/environment';

export default class AuthService extends Service {
    @service api;
    @service router;
    @service session;

    async login(username, password) {
        const options = {
            method: 'POST',
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        };

        const response = await this.api.call('/api/login', options);

        if (!response) {
            console.log('Unable to authenticate user.');
            return;
        }

        await this.session.authenticate('authenticator:custom-token', response);

        if (this.session.isAuthenticated) {
            console.log('Successful login');
            this.router.transitionTo('home');
        }
    }

    async register(username, password) {
        try {
            const options = {
                method: 'POST',
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            };

            const response = await this.api.call('/api/register', options);

            if (response && response.ok) {
                await this.login(username, password);
            } else {
                console.log('Unable to register.', response);
            }
        } catch (error) {
            console.error('Error during registration:', error);
        }
    }
}
