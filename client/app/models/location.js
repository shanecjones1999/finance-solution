// app/models/location.js
import Model, { attr } from '@ember-data/model';

export default class LocationModel extends Model {
    @attr('string') address;
    @attr('string') city;
    @attr('string') country;
    @attr('number') lat;
    @attr('number') lon;
    @attr('string') postal_code;
    @attr('string') region;
    @attr('string') store_number;
}
