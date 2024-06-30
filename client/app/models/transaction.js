import Model, { attr, belongsTo } from '@ember-data/model';

export default class TransactionModel extends Model {
    @attr('string') account_id;
    @attr('string') account_owner;
    @attr('number') amount;
    @attr('date') authorized_date;
    @attr() authorized_datetime;
    @attr() category; // Array of strings
    @attr('string') category_id;
    @attr('string') check_number;
    @attr() counterparties; // Array of objects
    @attr('date') date;
    @attr() datetime;
    @attr('string') iso_currency_code;
    @attr() location;
    @attr('string') logo_url;
    @attr('string') merchant_entity_id;
    @attr('string') merchant_name;
    @attr('string') name;
    @attr('string') payment_channel;
    @attr() payment_meta;
    @attr('boolean') pending;
    @attr('string') pending_transaction_id;
    @attr() personal_finance_category;
    @attr('string') personal_finance_category_icon_url;
    @attr('string') transaction_code;
    @attr('string') transaction_id;
    @attr('string') transaction_type;
    @attr('string') unofficial_currency_code;
    @attr('string') website;
}
