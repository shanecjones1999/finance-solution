import Model, { hasMany, belongsTo } from '@ember-data/model';

export default class FinancialInstitutionItemModel extends Model {
    @belongsTo('financial-institution') institutions;
    @belongsTo('financial-item') items;
}
