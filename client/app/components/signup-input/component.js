import Component from '@glimmer/component';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';
import { inject as service } from '@ember/service';

export default class SignupInput extends Component {
    @service auth;

    @tracked username = '';
    @tracked password = '';

    @action
    async submit() {
        try {
            await this.auth.register(this.username, this.password);
        } catch (error) {
            console.error('Error during login:', error);
        }
    }
}
