import Service from '@ember/service';
import { inject as service } from '@ember/service';
import ENV from 'client/config/environment';

export default class AuthService extends Service {
    @service router;
    @service session;

    async login(username, password) {
        try {
            const response = await fetch(`${ENV.apiHost}/api/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });

            if (!response || !response.ok) {
                console.log('Unable to authenticate user.');
                return;
            }

            await this.session.authenticate(
                'authenticator:custom-token',
                response.json()
            );

            if (this.session.isAuthenticated) {
                console.log('Successful login');
                this.router.transitionTo('home');
            }
        } catch (error) {
            console.error('Error during login:', error);
        }
    }
}
