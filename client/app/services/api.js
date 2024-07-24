import Service from '@ember/service';
import { inject as service } from '@ember/service';
import ENV from 'client/config/environment';

export default class ApiService extends Service {
    @service session;

    async call(endpoint, options = {}) {
        const headers = options.headers || {};
        headers['Content-Type'] = 'application/json';

        if (this.session.isAuthenticated) {
            const { token } = this.session.data.authenticated;
            headers['Authorization'] = `Bearer ${token}`;
        }

        options.headers = headers;
        options.method = options.method || 'GET';

        try {
            const response = await fetch(`${ENV.apiHost}${endpoint}`, options);

            if (!response.ok) {
                throw new Error(
                    `API request to ${endpoint} failed with status ${response.status}: ${response.statusText}`
                );
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error(`API request to ${endpoint} error: ${error}`);
            throw error;
        }
    }
}
