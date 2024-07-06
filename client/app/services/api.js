import Service from '@ember/service';
import { inject as service } from '@ember/service';

export default class ApiService extends Service {
    @service session;

    async call(url, options = {}) {
        let headers = options.headers || {};

        // Get the auth token from the session
        if (this.session.isAuthenticated) {
            let { token } = this.session.data.authenticated;
            headers['Authorization'] = `Bearer ${token}`;
        }
    }
}
