from marshmallow import Schema, fields

class RoutesSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    url  = fields.String()
    doc  = fields.String()
    logs = fields.Nested('LogsSchema', many=True)

class LogsSchema(Schema):
    id = fields.Integer()
    id_route    = fields.Integer()
    status_code = fields.Integer()
    message     = fields.String()
    time        = fields.DateTime(format='%Y-%m-%d %H:%M:%S')