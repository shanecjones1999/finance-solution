import Component from '@glimmer/component';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';
import { inject as service } from '@ember/service';
import ENV from 'client/config/environment';

export default class LoginInput extends Component {
    @service session;
    @service router;

    @tracked username = '';
    @tracked password = '';

    @action
    async submit() {
        try {
            let response = await fetch(`${ENV.apiHost}/api/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: this.username,
                    password: this.password,
                }),
            });

            if (!response || !response.ok) {
                console.log('Unable to authenticate user.');
                return;
            }

            // const data = await response.json();

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
