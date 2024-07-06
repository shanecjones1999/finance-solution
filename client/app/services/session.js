import SessionService from 'ember-simple-auth/services/session';

export default class Session extends SessionService {
    async invalidate() {
        await super.invalidate();
    }
}
