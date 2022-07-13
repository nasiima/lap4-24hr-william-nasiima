DROP TABLE IF EXISTS urltable;

CREATE TABLE urltable (
  id serial PRIMARY KEY,
  url varchar(255) NOT NULL,
  short_id varchar(50) NOT NULL
);
