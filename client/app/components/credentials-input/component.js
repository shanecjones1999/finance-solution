import Component from '@glimmer/component';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';
import ENV from 'client/config/environment';
import { inject as service } from '@ember/service';

export default class CredentialsInput extends Component {
    @service session;
    @service router;

    @tracked username = '';
    @tracked password = '';

    @action
    async submit() {
        try {
            let response = undefined;
            if (this.args.endpoint == 'login') {
                response = await this.session.authenticate(
                    'authenticator:custom-token',
                    this.username,
                    this.password
                );
            } else {
                response = await fetch(
                    `${ENV.apiHost}/api/${this.args.endpoint}`,
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            username: this.username,
                            password: this.password,
                        }),
                    }
                );
            }

            if (response && response.ok) {
                console.log('Successful login');
            }

            if (this.session.isAuthenticated) {
                this.router.transitionTo('home');
            }
        } catch (error) {
            console.error('Error during login:', error);
        }
    }
}
