import Component from '@glimmer/component';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';
import { inject as service } from '@ember/service';
import ENV from 'client/config/environment';

export default class SignupInput extends Component {
    @service session;
    @service router;

    @tracked username = '';
    @tracked password = '';

    @action
    async submit() {
        try {
            let response = await fetch(`${ENV.apiHost}/api/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: this.username,
                    password: this.password,
                }),
            });

            if (response && response.ok) {
                response = await this.session.authenticate(
                    'authenticator:custom-token',
                    this.username,
                    this.password
                );

                if (this.session.isAuthenticated) {
                    this.router.transitionTo('home');
                }
            }

            if (this.session.isAuthenticated) {
                this.router.transitionTo('home');
            }
        } catch (error) {
            console.error('Error during login:', error);
        }
    }
}
