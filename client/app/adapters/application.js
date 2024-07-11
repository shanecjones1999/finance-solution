import JSONAPIAdapter from '@ember-data/adapter/json-api';
import { inject as service } from '@ember/service';
import { computed } from '@ember/object';

export default class ApplicationAdapter extends JSONAPIAdapter {
    @service session;

    namespace = 'api';
    host = 'http://127.0.0.1:5000';

    @computed('session.isAuthenticated', 'session.data.authenticated.token')
    get headers() {
        const headers = {};
        headers['Content-Type'] = 'application/json';

        if (this.session.isAuthenticated) {
            headers[
                'Authorization'
            ] = `Bearer ${this.session.data.authenticated.token}`;
        }

        return headers;
    }
}
