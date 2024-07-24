import ProtectedRoute from './protected';
import { inject as service } from '@ember/service';

export default class HomeRoute extends ProtectedRoute {
    @service api;
    @service store;

    async model() {
        try {
            const options = {
                method: 'GET',
            };
            const data = await this.api.call('/api/items', options);
            console.log(data);
            const items = data.data.map((item) => item.institution);
            this.financialItems = items;

            return { financialItems: items };
        } catch (e) {
            console.error('Error getting items', e);
        }
    }
}
