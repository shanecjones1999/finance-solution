import Model, { attr, belongsTo } from '@ember-data/model';

export default class FinancialInstitutionModel extends Model {
    @attr() countryCodes;
    @attr() dtcNumbers;
    @attr('string') institutionId;
    @attr('string') name;
    @attr('boolean') oath;
    @attr() products;
    @attr() routingNumbers;
}
