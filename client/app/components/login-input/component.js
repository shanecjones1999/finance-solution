import Component from '@glimmer/component';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';
import { inject as service } from '@ember/service';

export default class LoginInput extends Component {
    @service auth;

    @tracked username = '';
    @tracked password = '';

    @action
    async submit() {
        await this.auth.login(this.username, this.password);
    }
}
