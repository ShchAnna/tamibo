CREATE DATABASE tamibo
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE TYPE public.size_ranges AS ENUM
    ('XS', 'S', 'M', 'L', 'XL');

CREATE TABLE model
(
    model_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
	PRIMARY KEY(model_id),
    model_name text NOT NULL,
    article_number text NOT NULL,
    photo bytea,
    layout_patterns bytea,
    tailoring_technology text,
    size_range size_ranges[]

);

CREATE TABLE shipment
(
    shipment_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
	PRIMARY KEY(shipment_id),
	model_id integer NOT NULL,
    FOREIGN KEY (model_id) REFERENCES model (model_id),
    shipment_date date,
    products_number integer,
    rulers_number integer
);

CREATE TABLE delivery
(
    delivery_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
	PRIMARY KEY(delivery_id),
	shipment_id integer NOT NULL,
    FOREIGN KEY (shipment_id ) REFERENCES shipment  (shipment_id ),
    from_where text NOT NULL,
    to_where text NOT NULL,
    tipe_delivery text NOT NULL,
    object_delivery text NOT NULL,
    delivery_cost money NOT NULL
);

CREATE TABLE packing
(
    packing_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
	PRIMARY KEY(packing_id),
    shipment_id integer NOT NULL,
	FOREIGN KEY (shipment_id ) REFERENCES shipment  (shipment_id ),
    tags_cost money NOT NULL,
    label_cost money NOT NULL,
    packege_cost money NOT NULL
);

CREATE TABLE jobs
(
    jobs_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
	PRIMARY KEY(jobs_id),
    shipment_id integer NOT NULL,
	FOREIGN KEY (shipment_id ) REFERENCES shipment  (shipment_id ),
    jobs_tipe text NOT NULL,
    employee text NOT NULL,
    jobs_cost money NOT NULL
);

CREATE TABLE accessories
(
    accessories_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    PRIMARY KEY(accessories_id),
	model_id integer NOT NULL,
    FOREIGN KEY (model_id) REFERENCES model (model_id),
    accessories_name text NOT NULL,
    number_per_one integer NOT NULL
);

CREATE TABLE materials
(
    materials_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    PRIMARY KEY(materials_id),
	model_id integer NOT NULL,
    FOREIGN KEY (model_id) REFERENCES model (model_id),
    materials_name text NOT NULL,
    m_per_ruler numeric NOT NULL
);

CREATE TABLE accessories_cost
(
    accessories_cost_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    PRIMARY KEY(accessories_cost_id),
	shipment_id integer NOT NULL,
    FOREIGN KEY (shipment_id) REFERENCES shipment (shipment_id),
    accessories_id integer NOT NULL,
	FOREIGN KEY (accessories_id) REFERENCES accessories (accessories_id),
    accessories_number integer NOT NULL,
    accessories_cost money NOT NULL
);

CREATE TABLE materials_cost
(
    materials_cost_id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    PRIMARY KEY(materials_cost_id),
	shipment_id integer NOT NULL,
    FOREIGN KEY (shipment_id) REFERENCES shipment (shipment_id),
    materials_id integer NOT NULL,
	FOREIGN KEY (materials_id) REFERENCES materials (materials_id),
    materials_number numeric NOT NULL,
    materials_cost money NOT NULL
);
