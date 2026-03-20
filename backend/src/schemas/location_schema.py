from marshmallow import Schema, fields


class CountriesItemsSchema(Schema):
    iso3 = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)


class StatesItemsSchema(Schema):
    state_code = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)


class CountriesSchema(Schema):
    data = fields.List(fields.Nested(CountriesItemsSchema))


class StatesSchema(Schema):
    data = fields.List(fields.Nested(StatesItemsSchema))


class CitiesSchema(Schema):
    data = fields.List(fields.Str(dump_only=True))
