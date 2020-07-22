-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2020-07-22 13:29:54.052

-- tables
-- Table: admin
CREATE TABLE admin (
    id int NOT NULL,
    first_name varchar(64) NOT NULL,
    last_name varchar(64) NULL,
    username varchar(128) NOT NULL,
    password varchar(300) NOT NULL,
    CONSTRAINT admin_pk PRIMARY KEY (id)
);

-- Table: customer
CREATE TABLE customer (
    id int NOT NULL,
    first_name varchar(128) NOT NULL,
    last_name varchar(128) NOT NULL,
    contact_email varchar(128) NULL,
    contact_phone varchar(10) NOT NULL,
    customer_address text NOT NULL,
    delivery_address text NULL,
    CONSTRAINT customer_pk PRIMARY KEY (id)
) COMMENT 'table for customer';

-- Table: delivery
CREATE TABLE delivery (
    id int NOT NULL,
    delivery_time_placed timestamp NOT NULL,
    deivery_time_actual timestamp NULL,
    notes int NULL,
    placed_order_id int NOT NULL,
    employee_id int NOT NULL,
    CONSTRAINT delivery_pk PRIMARY KEY (id)
);

-- Table: employee
CREATE TABLE employee (
    id int NOT NULL,
    first_name varchar(64) NOT NULL,
    last_name varchar(64) NULL,
    CONSTRAINT employee_pk PRIMARY KEY (id)
);

-- Table: order_item
CREATE TABLE order_item (
    id int NOT NULL,
    quantity decimal(10,3) NOT NULL,
    price decimal(10,3) NOT NULL,
    product_id int NOT NULL,
    placed_order_id int NOT NULL,
    CONSTRAINT order_item_pk PRIMARY KEY (id)
);

-- Table: order_status
CREATE TABLE order_status (
    id int NOT NULL,
    status_time timestamp NOT NULL,
    details text NULL,
    status_catalog_id int NOT NULL,
    CONSTRAINT order_status_pk PRIMARY KEY (id)
);

-- Table: placed_order
CREATE TABLE placed_order (
    id int NOT NULL,
    time_placed timestamp NOT NULL,
    details text NULL,
    delivery_address text NOT NULL,
    customer_id int NOT NULL,
    order_status_id int NOT NULL,
    CONSTRAINT placed_order_pk PRIMARY KEY (id)
);

-- Table: product
CREATE TABLE product (
    id int NOT NULL AUTO_INCREMENT,
    product_name varchar(64) NOT NULL,
    product_description varchar(255) NOT NULL,
    product_type_id int NOT NULL,
    price_per_unit decimal(8,2) NOT NULL,
    unit_id int NOT NULL,
    CONSTRAINT product_pk PRIMARY KEY (id)
);

-- Table: product_type
CREATE TABLE product_type (
    id int NOT NULL AUTO_INCREMENT,
    type_name varchar(64) NOT NULL,
    CONSTRAINT product_type_pk PRIMARY KEY (id)
);

-- Table: shop_details
CREATE TABLE shop_details (
    id int NOT NULL,
    shop_name varchar(128) NOT NULL,
    details text NULL,
    address text NOT NULL,
    admin_id int NOT NULL,
    CONSTRAINT shop_details_pk PRIMARY KEY (id)
);

-- Table: status_catalog
CREATE TABLE status_catalog (
    id int NOT NULL,
    status_name varchar(128) NOT NULL,
    CONSTRAINT status_catalog_pk PRIMARY KEY (id)
);

-- Table: stock
CREATE TABLE stock (
    product_id int NOT NULL AUTO_INCREMENT,
    in_stock decimal(8,2) NOT NULL,
    last_update_time timestamp NOT NULL,
    CONSTRAINT stock_pk PRIMARY KEY (product_id)
);

-- Table: units
CREATE TABLE units (
    id int NOT NULL,
    unit_name varchar(64) NOT NULL,
    unit_short varchar(8) NULL,
    CONSTRAINT units_pk PRIMARY KEY (id)
) COMMENT 'info about, the units for each item, in inventory. eg 
unit_name - > "kilogram" 
unit_short - > "kg"';

-- views
-- View: product_details
CREATE VIEW product_details AS
SELECT
  p.id,
  p.product_name,
  p.product_description,
  pt.type_name,
  p.unit_id,
  p.price_per_unit,
  s.in_stock,
  s.last_update_time
FROM product p
LEFT JOIN units ut ON p.unit_id = ut.id
LEFT JOIN product_type pt ON p.product_type_id = pt.id
LEFT JOIN stock s ON p.id = s.product_id;

-- foreign keys
-- Reference: delivery_employee (table: delivery)
ALTER TABLE delivery ADD CONSTRAINT delivery_employee FOREIGN KEY delivery_employee (employee_id)
    REFERENCES employee (id);

-- Reference: delivery_placed_order (table: delivery)
ALTER TABLE delivery ADD CONSTRAINT delivery_placed_order FOREIGN KEY delivery_placed_order (placed_order_id)
    REFERENCES placed_order (id);

-- Reference: order_item_placed_order (table: order_item)
ALTER TABLE order_item ADD CONSTRAINT order_item_placed_order FOREIGN KEY order_item_placed_order (placed_order_id)
    REFERENCES placed_order (id);

-- Reference: order_item_product (table: order_item)
ALTER TABLE order_item ADD CONSTRAINT order_item_product FOREIGN KEY order_item_product (product_id)
    REFERENCES product (id);

-- Reference: order_status_status_catalog (table: order_status)
ALTER TABLE order_status ADD CONSTRAINT order_status_status_catalog FOREIGN KEY order_status_status_catalog (status_catalog_id)
    REFERENCES status_catalog (id);

-- Reference: placed_order_Customer (table: placed_order)
ALTER TABLE placed_order ADD CONSTRAINT placed_order_Customer FOREIGN KEY placed_order_Customer (customer_id)
    REFERENCES customer (id);

-- Reference: placed_order_order_status (table: placed_order)
ALTER TABLE placed_order ADD CONSTRAINT placed_order_order_status FOREIGN KEY placed_order_order_status (order_status_id)
    REFERENCES order_status (id);

-- Reference: product_product_type (table: product)
ALTER TABLE product ADD CONSTRAINT product_product_type FOREIGN KEY product_product_type (product_type_id)
    REFERENCES product_type (id);

-- Reference: product_units (table: product)
ALTER TABLE product ADD CONSTRAINT product_units FOREIGN KEY product_units (unit_id)
    REFERENCES units (id);

-- Reference: shop_details_admin (table: shop_details)
ALTER TABLE shop_details ADD CONSTRAINT shop_details_admin FOREIGN KEY shop_details_admin (admin_id)
    REFERENCES admin (id);

-- Reference: stock_product (table: stock)
ALTER TABLE stock ADD CONSTRAINT stock_product FOREIGN KEY stock_product (product_id)
    REFERENCES product (id);

-- End of file.

