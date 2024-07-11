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
        this.getItems();
    }

    async createLinkToken() {
        const options = {
            method: 'POST',
        };

        const response = await this.api.call('/api/create_link_token', options);
        this.linkToken = response.link_token;
    }

    // @action
    // async getTransactions() {
    //     try {
    //         const transactions = await this.store.findAll('transaction');
    //         this.transactions = transactions;
    //     } catch (e) {
    //         console.error('Error getting transactions', e);
    //     }
    // }

    async getItems() {
        try {
            const options = {
                method: 'GET',
            };
            const items = await this.api.call('/api/items', options);
            console.log(items);
            const itms = items.data.map((it) => it.institution);
            this.financialItems = itms;
        } catch (e) {
            console.error('Error getting items', e);
        }
    }

    @action
    openPlaidLink() {
        if (this.linkToken) {
            const handler = Plaid.create({
                token: this.linkToken,
                onSuccess: async (public_token, metadata) => {
                    const options = {
                        method: 'POST',
                        body: JSON.stringify({ public_token }),
                    };
                    await this.api.call('/api/set_access_token', options);
                },
                onExit: (err, metadata) => {
                    if (err != null) {
                        console.error(err);
                    }
                },
            });

            handler.open();
        }
    }
}
