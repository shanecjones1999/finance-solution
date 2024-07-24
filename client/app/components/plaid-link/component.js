import Component from '@glimmer/component';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';
import { inject as service } from '@ember/service';

export default class PlaidLink extends Component {
    @service store;
    @service api;

    @tracked linkToken = null;

    @tracked transactions = [];
    @tracked financialItems = [];

    constructor() {
        super(...arguments);
        this.createLinkToken();
    }

    async createLinkToken() {
        const options = {
            method: 'POST',
        };

        const response = await this.api.call('/api/create_link_token', options);

        if (!response) {
            return;
        }

        this.linkToken = response.link_token;
    }

    @action
    openPlaidLink() {
        if (this.linkToken) {
            const handler = Plaid.create({
                token: this.linkToken,
                onSuccess: async (public_token) => {
                    const options = {
                        method: 'POST',
                        body: JSON.stringify({ public_token }),
                    };
                    await this.api.call('/api/set_access_token', options);
                },
                onExit: (err) => {
                    if (err != null) {
                        console.error(err);
                    }
                },
            });

            handler.open();
        }
    }
}
