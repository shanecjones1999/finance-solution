// app/models/payment-meta.js
import Model, { attr } from '@ember-data/model';

export default class PaymentMetaModel extends Model {
    @attr('string') by_order_of;
    @attr('string') payee;
    @attr('string') payer;
    @attr('string') payment_method;
    @attr('string') payment_processor;
    @attr('string') ppd_id;
    @attr('string') reason;
    @attr('string') reference_number;
}
