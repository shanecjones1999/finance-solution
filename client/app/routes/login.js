import Route from '@ember/routing/route';
import { inject as service } from '@ember/service';

export default class LoginRoute extends Route {
    @service router;
    @service session;

    beforeModel() {
        if (this.session.isAuthenticated) {
            this.router.transitionTo('home');
        }
    }
}
