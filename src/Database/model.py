from peewee import *
from src.Connector.MA import MA

ma = MA()
database = SqliteDatabase(ma.readConfig()['data_location']['Database'])


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class BasicPerformance(BaseModel):
    bounce_rate = DecimalField(null=True)
    click = IntegerField(null=True)
    creation_time = TextField(null=True)
    ctr = TextField(null=True)
    delivered = IntegerField(null=True)
    editor = TextField(null=True)
    hard_bounces = TextField(null=True)
    open_rate = DecimalField(null=True)
    opened = IntegerField(null=True)
    sent = IntegerField(null=True)
    smc_campaign_id = IntegerField()
    soft_bounces = TextField(null=True)
    unique_click = IntegerField(null=True)
    unique_click_to_open_rate = DecimalField(null=True)
    unique_ctr = IntegerField(null=True)
    valid_click = IntegerField(null=True)
    valid_click_to_open_rate = DecimalField(null=True)
    vanilla_click_to_open_rate = DecimalField(null=True)

    class Meta:
        table_name = 'BasicPerformance'


class ClickPerformance(BaseModel):
    click_number = IntegerField()
    creation_time = TextField()
    editor = TextField(null=True)
    if_main_link = DecimalField()
    link_alias = IntegerField(null=True)
    link_name = TextField(null=True)
    smc_campaign_id = IntegerField()

    class Meta:
        table_name = 'ClickPerformance'


class Request(BaseModel):
    blast_date = DateField(null=True)
    campaign_name = TextField(null=True)
    comments = TextField(null=True)
    creation_time = DateTimeField(null=True)
    editor = TextField(null=True)
    event_date = DateField(null=True)
    last_modified_time = DateTimeField(null=True)
    location = TextField(null=True)
    mu = TextField(null=True)
    owner_first_name = TextField(null=True)
    owner_full_name = TextField(null=True)
    owner_last_name = TextField(null=True)
    report_date = TextField(null=True)
    request_id = IntegerField(null=True)
    request_status = IntegerField(null=True)
    request_type = TextField(null=True)
    smc_campaign_id = IntegerField(null=True)
    team = TextField(null=True)
    wave = IntegerField(null=True)

    class Meta:
        table_name = 'Request'


class Staff(BaseModel):
    email = TextField(null=True)
    first_name = TextField()
    last_name = TextField()
    location = TextField(null=True)
    team = TextField()
    user_id = TextField(null=True)

    class Meta:
        table_name = 'Staff'


class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False
