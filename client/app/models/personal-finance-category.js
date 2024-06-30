// app/models/personal-finance-category.js
import Model, { attr } from '@ember-data/model';

export default class PersonalFinanceCategoryModel extends Model {
    @attr('string') confidence_level;
    @attr('string') detailed;
    @attr('string') primary;
}
