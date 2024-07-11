import Service from '@ember/service';
import { inject as service } from '@ember/service';
import ENV from 'client/config/environment';

export default class ApiService extends Service {
    @service session;

    async call(url, options = {}) {
        const headers = options.headers || {};
        headers['Content-Type'] = 'application/json';

        // Get the auth token from the session
        if (this.session.isAuthenticated) {
            const { token } = this.session.data.authenticated;
            headers['Authorization'] = `Bearer ${token}`;
        }

        options.headers = headers;
        options.method = options.method || 'GET';

        try {
            const response = await fetch(`${ENV.apiHost}${url}`, options);

            if (!response.ok) {
                throw new Error(
                    `API request failed with status ${response.status}: ${response.statusText}`
                );
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    }
}
