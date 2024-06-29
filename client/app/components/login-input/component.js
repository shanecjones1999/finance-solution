import Component from '@glimmer/component';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';
import { inject as service } from '@ember/service';

export default class LoginInput extends Component {
    @service session;
    @service router;

    @tracked username = '';
    @tracked password = '';

    @action
    async submit() {
        try {
            const response = await this.session.authenticate(
                'authenticator:custom-token',
                this.username,
                this.password
            );

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
