import Component from '@glimmer/component';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';
import ENV from '../../config/environment';
import { inject as service } from '@ember/service';

//import fetch from 'fetch';

export default class PlaidLink extends Component {
    @service store;

    @tracked linkToken = null;

    @tracked transactions = [];

    constructor() {
        super(...arguments);
        this.createLinkToken();
    }

    async createLinkToken() {
        let response = await fetch(`${ENV.apiHost}/api/create_link_token`, {
            method: 'POST',
        });
        let data = await response.json();
        this.linkToken = data.link_token;
    }

    @action
    async getTransactions() {
        // const response = await fetch(`${ENV.apiHost}/api/transactions`, {
        //     method: 'GET',
        // });
        // const data = await response.json();
        // this.transactions = data['latest_transactions'];
        // console.log(this.transactions);

        // ember data test
        const transactions = await this.store.findAll('transaction');
        console.log(transactions);
        this.transactions = transactions;
    }

    @action
    openPlaidLink() {
        if (this.linkToken) {
            const handler = Plaid.create({
                token: this.linkToken,
                onSuccess: async (public_token, metadata) => {
                    // Send the public_token to your server for further processing
                    await fetch(`${ENV.apiHost}/api/set_access_token`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ public_token }),
                    });
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
