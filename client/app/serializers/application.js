import JSONSerializer from '@ember-data/serializer/json';

export default class ApplicationSerializer extends JSONSerializer {
    normalizeResponse(store, primaryModelClass, payload, id, requestType) {
        if (payload.data) {
            return super.normalizeResponse(
                store,
                primaryModelClass,
                payload.data,
                id,
                requestType
            );
        } else {
            return super.normalizeResponse(
                store,
                primaryModelClass,
                payload,
                id,
                requestType
            );
        }
    }
}
