create table instrument_identifiers (
    id bigint not null auto_increment,
    instrument_id bigint not null,
    namespace varchar(80) not null,
    identifier varchar(160) not null,
    normalized_identifier varchar(160) not null,
    purpose varchar(60) not null,
    source varchar(80) not null,
    enabled boolean not null default true,
    notes varchar(500),
    created_at datetime(6) not null default current_timestamp(6),
    updated_at datetime(6) not null default current_timestamp(6),
    primary key (id),
    constraint fk_instrument_identifier_instrument foreign key (instrument_id) references instruments (id),
    constraint uk_instrument_identifier_namespace_value_purpose unique (namespace, normalized_identifier, purpose)
);

create index idx_instrument_identifiers_instrument_namespace
    on instrument_identifiers (instrument_id, namespace);

create index idx_instrument_identifiers_purpose_enabled
    on instrument_identifiers (purpose, enabled);

insert into instrument_identifiers (
    instrument_id,
    namespace,
    identifier,
    normalized_identifier,
    purpose,
    source,
    enabled,
    created_at,
    updated_at
)
select id,
       'YFINANCE',
       concat(symbol, '.KS'),
       concat(symbol, '.KS'),
       'MARKET_DATA',
       'seed',
       true,
       current_timestamp(6),
       current_timestamp(6)
from instruments
where market = 'KR';

insert into instrument_identifiers (
    instrument_id,
    namespace,
    identifier,
    normalized_identifier,
    purpose,
    source,
    enabled,
    created_at,
    updated_at
)
select id,
       'YFINANCE',
       symbol,
       symbol,
       'MARKET_DATA',
       'seed',
       true,
       current_timestamp(6),
       current_timestamp(6)
from instruments
where market = 'US';

insert into instrument_identifiers (
    instrument_id,
    namespace,
    identifier,
    normalized_identifier,
    purpose,
    source,
    enabled,
    created_at,
    updated_at
)
select id,
       'KRX_TICKER',
       symbol,
       symbol,
       'EXCHANGE_REFERENCE',
       'seed',
       true,
       current_timestamp(6),
       current_timestamp(6)
from instruments
where market = 'KR';

insert into instrument_identifiers (
    instrument_id,
    namespace,
    identifier,
    normalized_identifier,
    purpose,
    source,
    enabled,
    created_at,
    updated_at
)
select id,
       'US_TICKER',
       symbol,
       symbol,
       'EXCHANGE_REFERENCE',
       'seed',
       true,
       current_timestamp(6),
       current_timestamp(6)
from instruments
where market = 'US';

insert into instrument_identifiers (
    instrument_id,
    namespace,
    identifier,
    normalized_identifier,
    purpose,
    source,
    enabled,
    created_at,
    updated_at
)
select id,
       'NAVER_STOCK_BOARD',
       symbol,
       symbol,
       'COMMUNITY_BOARD',
       'seed',
       true,
       current_timestamp(6),
       current_timestamp(6)
from instruments
where market = 'KR';
