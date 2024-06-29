import SessionService from 'ember-simple-auth/services/session';
import { inject as service } from '@ember/service';
import ENV from 'client/config/environment';

export default class Session extends SessionService {
    @service router;

    // restore() {
    //     console.log('restoring');
    // }

    // Make this async for websocket.
    // async invalidate() {
    //     const token = this.data.authenticated.token;

    //     const headers = {
    //         Authorization: `${token}`,
    //         'Content-Type': 'application/json',
    //     };

    //     const response = await fetch(`${ENV.apiHost}/api/invalidateSession`, {
    //         method: 'POST',
    //         headers: headers,
    //     });

    //     super.invalidate();
    // }

    async invalidate() {
        await super.invalidate();
    }
}
