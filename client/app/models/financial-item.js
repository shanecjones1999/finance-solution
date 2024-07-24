import Model, { attr, belongsTo } from '@ember-data/model';

export default class FinancialItemModel extends Model {
    @attr() availableProducts;
    @attr() billedProducts;
    @attr() consentExpirationTime;
    @attr() error;
    @attr('string') institutionId;
    @attr('string') itemId;
    @attr() products;
    @attr('string') updateType;
    @attr() webhook;
}
