/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     22/11/2023 15:52:20                          */
/*==============================================================*/


/*drop table client_addresses;

drop table client_invoice_components;

drop table client_invoices;

drop table client_order_components;

drop table client_orders;

drop table clients;

drop table labors;

drop table material_receipt_components;

drop table material_receipts;

drop table production_order_components;

drop table production_orders;

drop table products;

drop table purchasing_order_components;

drop table purchasing_orders;

drop table sales_order_components;

drop table sales_orders;

drop table stock_movements;

drop table supplier_invoices;

drop table suppliers;

drop table warehouses;*/

/*==============================================================*/
/* Table: clients                                               */
/*==============================================================*/
create table clients (
   id_client            SERIAL                 not null,
   name                 TEXT                 not null,
   email                TEXT                 not null,
   nif                  TEXT                 not null,
   phone                TEXT                 not null,
   address              TEXT                 not null,
   locality             TEXT                 not null,
   postal_code          TEXT                 not null,
   constraint PK_CLIENTS primary key (id_client)
);

/*==============================================================*/
/* Table: client_invoices                                       */
/*==============================================================*/
create table client_invoices (
   id_client_invoice    SERIAL                 not null,
   id_client            INTEGER                 not null,
   obs                  TEXT                 null,
   total_base           MONEY                not null default 0,
   vat_total            MONEY                not null default 0,
   discount_total       MONEY                not null default 0,
   expire_date          TIMESTAMPTZ          not null,
   invoice_date         TIMESTAMPTZ          not null,
   invoice_id           TEXT                 not null,
   total                MONEY                not null default 0,
   created_at           TIMESTAMPTZ                 not null default 'now()',
   constraint PK_CLIENT_INVOICES primary key (id_client_invoice),
   constraint FK_CINVOICES_HAS_CLIENT foreign key (id_client)
      references clients (id_client)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: products                                              */
/*==============================================================*/
CREATE TYPE products_type AS ENUM ('COMPONENT', 'EQUIPMENT');
create table products (
   id_product           SERIAL                 not null,
   name                 TEXT                 not null,
   description          TEXT                 null,
   weight               REAL                 null,
   type                 products_type        not null,
   profit_margin        REAL                not null,
   vat                  INTEGER              not null,
   price_cost           MONEY                null default 0,
   price_base           MONEY               null GENERATED ALWAYS AS (price_cost * (1 + (profit_margin / 100.0))) STORED,
   pvp                  MONEY                not null GENERATED ALWAYS AS ((price_cost * (1 + (profit_margin / 100.0))) * (1 + (vat / 100.0))) STORED,
   constraint PK_PRODUCTS primary key (id_product)
);

/*==============================================================*/
/* Table: client_invoice_components                             */
/*==============================================================*/
create table client_invoice_components (
   id_client_invoice_component SERIAL                 not null,
   id_product           INTEGER                 not null,
   id_client_invoice    INTEGER                 not null,
   quantity             INTEGER                 not null,
   price_base           MONEY                not null,
   vat                  INTEGER                 not null,
   vat_value            MONEY                not null default 0,
   discount             REAL               not null default 0,
   discount_value       MONEY                not null default 0, 
   line_total           MONEY                not null default 0,
   constraint PK_CLIENT_INVOICE_COMPONENTS primary key (id_client_invoice_component),
   constraint FK_CINVOICE_HAS_COMPONENTS foreign key (id_client_invoice)
      references client_invoices (id_client_invoice)
      on delete CASCADE on update CASCADE,
   constraint FK_CINVOICE_HAS_PRODUCTS foreign key (id_product)
      references products (id_product)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Index: CLIENT_INVOICE_COMPONENTS_PK                          */
/*==============================================================*/
create unique index Client_Invoice_Components_PK on client_invoice_components (
id_client_invoice_component
);

/*==============================================================*/
/* Index: CInvoices_Components_CInvoices                        */
/*==============================================================*/
create  index CInvoices_Components_CInvoices_key on client_invoice_components (
id_client_invoice
);

/*==============================================================*/
/* Index: CInvoices_Components_Products_key                     */
/*==============================================================*/
create  index CInvoices_Components_Products_key on client_invoice_components (
id_product
);

/*==============================================================*/
/* Index: CLIENT_INVOICES_PK                                    */
/*==============================================================*/
create unique index Client_Invoices_PK on client_invoices (
id_client_invoice
);

/*==============================================================*/
/* Index: HAS_FK2                                               */
/*==============================================================*/
create  index CInvoices_Clients_key on client_invoices (
id_client
);

/*==============================================================*/
/* Table: sales_orders                                          */
/*==============================================================*/
create table sales_orders (
   id_sale_order        SERIAL                 not null,
   id_user            INTEGER                 not null,
   id_client_invoice    INTEGER                 null,
   obs                  TEXT                 null,
   total_base           MONEY                not null default 0,
   vat_total            MONEY                not null default 0,
   discount_total       MONEY                not null default 0,
   total                MONEY                not null default 0,
   created_at           TIMESTAMPTZ                 not null default 'now()',
   constraint PK_SALES_ORDERS primary key (id_sale_order),
   constraint FK_AUTHUSER_MAKES_SALES foreign key (id_user)
      references auth_user (id)
      on delete restrict on update restrict,
   constraint FK_SALES_OR_HAS_CLIENT_I foreign key (id_client_invoice)
      references client_invoices (id_client_invoice)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: client_orders                                         */
/*==============================================================*/
create table client_orders (
   id_client_order      SERIAL                 not null,
   id_client            INTEGER                 not null,
   id_sale_order        INTEGER                 null,
   total_base           MONEY                not null default 0,
   vat_total            MONEY                not null default 0,
   discount_total       MONEY                not null default 0,
   total                MONEY                not null default 0,
   obs                  TEXT                 null,
   created_at           TIMESTAMPTZ                 not null default 'now()',
   constraint PK_CLIENT_ORDERS primary key (id_client_order),
   constraint FK_CLIENT_O_HAS_CLIENTS foreign key (id_client)
      references clients (id_client)
      on delete restrict on update restrict,
   constraint FK_CLIENT_O_HAS_SALES_OR foreign key (id_sale_order)
      references sales_orders (id_sale_order)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: client_order_components                               */
/*==============================================================*/
create table client_order_components (
   id_client_order_components SERIAL                 not null,
   id_product           INTEGER                 not null,
   id_client_order      INTEGER                 not null,
   quantity             INTEGER                 not null,
   price_base           MONEY                not null,
   vat                  INTEGER                 not null,
   vat_value            MONEY                not null default 0,
   discount             REAL               not null  default 0,
   discount_value       MONEY                not null default 0,
   line_total           MONEY                not null default 0,
   constraint PK_CLIENT_ORDER_COMPONENTS primary key (id_client_order_components),
   constraint FK_CLIENT_O_HAS_CLIENT_O foreign key (id_client_order)
      references client_orders (id_client_order)
      on delete restrict on update restrict,
   constraint FK_CLIENT_O_HAS_PRODUCTS foreign key (id_product)
      references products (id_product)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Index: CLIENT_ORDER_COMPONENTS_PK                            */
/*==============================================================*/
create unique index Client_Order_Components_PK on client_order_components (
id_client_order_components
);

/*==============================================================*/
/* Index: Client_Order_Components_COrder_key                                              */
/*==============================================================*/
create  index  Client_Order_Components_COrder_key on client_order_components (
id_client_order
);

/*==============================================================*/
/* Index: Client_Order_Components_Products_key                                              */
/*==============================================================*/
create  index Client_Order_Components_Products_key on client_order_components (
id_product
);

/*==============================================================*/
/* Index: CLIENT_ORDERS_PK                                      */
/*==============================================================*/
create unique index Client_Order_PK on client_orders (
id_client_order
);

/*==============================================================*/
/* Index: Client_Order_Client_key                               */
/*==============================================================*/
create  index Client_Order_Client_key on client_orders (
id_client
);

/*==============================================================*/
/* Index: Client_Order_Sale_Order_key                           */
/*==============================================================*/
create  index Client_Order_Sale_Order_key on client_orders (
id_sale_order
);

/*==============================================================*/
/* Index: CLIENTS_PK                                            */
/*==============================================================*/
create unique index Clients_PK on clients (
id_client
);

/*==============================================================*/
/* Table: labors                                                */
/*==============================================================*/
create table labors (
   id_labor             SERIAL                 not null,
   title                TEXT                 not null,
   cost                 MONEY               not null,
   constraint PK_LABORS primary key (id_labor)
);

/*==============================================================*/
/* Index: LABORS_PK                                             */
/*==============================================================*/
create unique index Labor_PK on labors (
id_labor
);

/*==============================================================*/
/* Table: suppliers                                             */
/*==============================================================*/
create table suppliers (
   id_supplier          SERIAL                 not null,
   name                 TEXT                 not null,
   email                TEXT                 not null,
   nif                  TEXT                 not null,
   phone                TEXT                 not null,
   address              TEXT                 not null,
   locality             TEXT                 not null,
   postal_code          TEXT                 not null,
   constraint PK_SUPPLIERS primary key (id_supplier)
);

/*==============================================================*/
/* Table: supplier_invoices                                     */
/*==============================================================*/
create table supplier_invoices (
   id_supplier_invoice  SERIAL                 not null,
   id_supplier          INTEGER                 not null,
   obs                  TEXT                 null,
   total_base           MONEY                not null default 0,
   vat_total            MONEY                not null default 0,
   discount_total       MONEY                not null default 0,
   total                MONEY                not null default 0,
   expire_date          TIMESTAMPTZ          not null,
   invoice_date         TIMESTAMPTZ          not null,
   invoice_id           TEXT                 not null,
   created_at           TIMESTAMPTZ                 not null default 'now()',
   constraint PK_SUPPLIER_INVOICES primary key (id_supplier_invoice),
   constraint FK_SUPPLIER_INVOICE_HAS_SUPPLIER foreign key (id_supplier)
      references suppliers (id_supplier)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: supplier_invoice_components                           */
/*==============================================================*/
create table supplier_invoice_components (
   id_supplier_invoice_component SERIAL                 not null,
   id_supplier_invoice  INTEGER                 not null,
   id_product           INTEGER                 not null,
   quantity             INTEGER                 not null,
   price_base           MONEY                not null,
   vat                  INTEGER                 not null,
   vat_value            MONEY                not null default 0,
   discount             REAL               not null   default 0,
   discount_value       MONEY                not null default 0,
   line_total           MONEY                not null default 0,
   constraint PK_SUPPLIER_INVOICE_COMPONENTS primary key (id_supplier_invoice_component),
   constraint FK_SUPPLIER_HAS_SUPPLIER_INVOICE foreign key (id_supplier_invoice)
      references supplier_invoices (id_supplier_invoice)
      on delete restrict on update restrict,
   constraint FK_SUPPLIER_HAS_PRODUCTS foreign key (id_product)
      references products (id_product)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Index: Supplier_Invoice_Components_Supplier_Invoices         */
/*==============================================================*/
create  index Supplier_Invoice_Components_Supplier_Invoices on supplier_invoice_components (
id_supplier_invoice
);

/*==============================================================*/
/* Index: Supplier_Invoices_Components_Products                 */
/*==============================================================*/
create  index Supplier_Invoices_Components_Products on supplier_invoice_components (
id_product
);



/*==============================================================*/
/* Table: purchasing_orders                                     */
/*==============================================================*/
create table purchasing_orders (
   id_purchasing_order  SERIAL                 not null,
   id_supplier          INTEGER                 not null,
   id_user            INTEGER                 not null,
   total_base           MONEY                not null default 0,
   vat_total            MONEY                not null default 0,
   discount_total       MONEY                not null default 0,
   total                MONEY                not null default 0,
   obs                  TEXT                 null,
   delivery_date        TIMESTAMPTZ         not null,
   created_at           TIMESTAMPTZ                 not null default 'now()',
   constraint PK_PURCHASING_ORDERS primary key (id_purchasing_order),
   constraint FK_PURCHASI_HAS_SUPPLIER foreign key (id_supplier)
      references suppliers (id_supplier)
      on delete restrict on update restrict,
   constraint FK_PURCHASI_HAS_AUTH_USE foreign key (id_user)
      references auth_user (id)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: material_receipts                                     */
/*==============================================================*/
create table material_receipts (
   id_material_receipt  SERIAL                 not null,
   id_supplier_invoice  INTEGER                 null,
   id_user            INTEGER                 not null,
   id_purchasing_order  INTEGER                 not null,
   n_delivery_note      TEXT                 not null,
   total_base           MONEY                not null default 0,
   vat_total            MONEY                not null default 0,
   discount_total       MONEY                not null default 0,
   total                MONEY                not null default 0,
   obs                  TEXT                 null,
   created_at           TIMESTAMPTZ                 not null default 'now()',
   constraint PK_MATERIAL_RECEIPTS primary key (id_material_receipt),
   constraint FK_MATERIAL_HAS_SUPPLIER foreign key (id_supplier_invoice)
      references supplier_invoices (id_supplier_invoice)
      on delete restrict on update restrict,
   constraint FK_MATERIAL_HAS_AUTH_USE foreign key (id_user)
      references auth_user (id)
      on delete restrict on update restrict,
   constraint FK_MATERIAL_HAS_PURCHASI foreign key (id_purchasing_order)
      references purchasing_orders (id_purchasing_order)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: warehouses                                            */
/*==============================================================*/
create table warehouses (
   id_warehouse         SERIAL                 not null,
   name                 TEXT                 not null,
   location             TEXT                 not null,
   constraint PK_WAREHOUSES primary key (id_warehouse)
);

/*==============================================================*/
/* Table: material_receipt_components                           */
/*==============================================================*/
create table material_receipt_components (
   id_material_receipt_component SERIAL                 not null,
   id_material_receipt  INTEGER                 not null,
   id_warehouse         INTEGER                 not null,
   id_product           INTEGER                 not null,
   quantity             INTEGER                 not null,
   price_base           MONEY                not null,
   vat                  INTEGER                 not null,
   vat_value            MONEY                not null default 0,
   discount             REAL               not null default 0,
   discount_value      MONEY                not null default 0,
   line_total           MONEY                not null default 0,
   constraint PK_MATERIAL_RECEIPT_COMPONENTS primary key (id_material_receipt_component),
   constraint FK_MATERIAL_HAS_MATERIAL foreign key (id_material_receipt)
      references material_receipts (id_material_receipt)
      on delete restrict on update restrict,
   constraint FK_MATERIAL_HAS_PRODUCTS foreign key (id_product)
      references products (id_product)
      on delete restrict on update restrict,
   constraint FK_MATERIAL_HAS_WAREHOUS foreign key (id_warehouse)
      references warehouses (id_warehouse)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Index: MATERIAL_RECEIPT_COMPONENTS_PK                        */
/*==============================================================*/
create unique index Material_Receipt_Components_PK on material_receipt_components (
id_material_receipt_component
);

/*==============================================================*/
/* Index: Material_Receipt_Components_Material_Receipt_key      */
/*==============================================================*/
create  index Material_Receipt_Components_Material_Receipts_key on material_receipt_components (
id_material_receipt
);

/*==============================================================*/
/* Index: Material_Receipt_Components_Products_key              */
/*==============================================================*/
create  index Material_Receipt_Components_Products_key on material_receipt_components (
id_product
);

/*==============================================================*/
/* Index: Material_Receipt_Components_Warehouse_key             */
/*==============================================================*/
create  index Material_Receipt_Components_Warehouses_key on material_receipt_components (
id_warehouse
);

/*==============================================================*/
/* Index: MATERIAL_RECEIPTS_PK                                  */
/*==============================================================*/
create unique index Material_Receipts_PK on material_receipts (
id_material_receipt
);

/*==============================================================*/
/* Index: Material_Receipts_SInvoices_key                       */
/*==============================================================*/
create  index Material_Receipts_SInvoices_key on material_receipts (
id_supplier_invoice
);

/*==============================================================*/
/* Index: Material_Receipts_Auth_Users                          */
/*==============================================================*/
create  index Material_Receipts_Auth_Users_key on material_receipts (
id_user
);

/*==============================================================*/
/* Index: Material_Receipts_Purchasing_Order_key                */
/*==============================================================*/
create  index Material_Receipts_Purchasing_Orders_key on material_receipts (
id_purchasing_order
);

/*==============================================================*/
/* Table: production_orders                                     */
/*==============================================================*/
CREATE TYPE production_order_status AS ENUM ('WAITING_PROD', 'IN_PROD', 'COMPLETED', 'CANCELED');
create table production_orders (
   id_order_production  SERIAL                 not null,
   id_labor             INTEGER                 not null,
   id_warehouse         INTEGER                  null,
   id_user            INTEGER                 not null,
   id_product            INTEGER                 not null,
   equipment_quantity   INTEGER                 not null,
   unit_cost            MONEY                null,
   production_cost      MONEY                null,
   obs                  TEXT                 null,
   status               production_order_status    null default 'WAITING_PROD',
   created_at           TIMESTAMPTZ                 null default 'now()',
   last_updated         TIMESTAMPTZ                 null default 'now()',
   constraint PK_PRODUCTION_ORDERS primary key (id_order_production),
   constraint FK_PRODUCTION_HAS_WAREHOUSE foreign key (id_warehouse)
      references warehouses (id_warehouse)
      on delete restrict on update restrict,
   constraint FK_PRODUCTI_HAS_LABORS foreign key (id_labor)
      references labors (id_labor)
      on delete restrict on update restrict,
    constraint FK_PRODUCTI_ORDER_HAS_PRODUCT foreign key (id_product)
      references products (id_product)
      on delete restrict on update restrict,
   constraint FK_PRODUCTI_MAKE_AUTH_USE foreign key (id_user)
      references auth_user (id)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: production_order_components                           */
/*==============================================================*/
create table production_order_components (
   id_production_order_components SERIAL                 not null,
   id_warehouse         INTEGER                 not null,
   id_order_production  INTEGER                 not null,
   id_product           INTEGER                 not null,
   quantity             INTEGER                 not null,
   price_base           MONEY                not null,
   line_total           MONEY                null GENERATED ALWAYS AS (price_base * quantity) STORED,
   constraint PK_PRODUCTION_ORDER_COMPONENTS primary key (id_production_order_components),
   constraint FK_PRODUCTI_HAS_PRODUCTI foreign key (id_order_production)
      references production_orders (id_order_production)
      on delete restrict on update restrict,
   constraint FK_PRODUCTI_HAS_PRODUCTS foreign key (id_product)
      references products (id_product)
      on delete restrict on update restrict,
   constraint FK_PRODUCTI_COME_WAREHOUS foreign key (id_warehouse)
      references warehouses (id_warehouse)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Index: PRODUCTION_ORDER_COMPONENTS_PK                        */
/*==============================================================*/
create unique index Production_Order_Components_PK on production_order_components (
id_production_order_components
);

/*==============================================================*/
/* Index: Production_Order_Components_Order_Production_key      */
/*==============================================================*/
create  index Production_Order_Components_Order_Productions_key on production_order_components (
id_order_production
);

/*==============================================================*/
/* Index: Production_Order_Components_Products_key                                              */
/*==============================================================*/
create  index Production_Order_Components_Products_key on production_order_components (
id_product
);

/*==============================================================*/
/* Index: Production_Order_Components_Warehouse_key             */
/*==============================================================*/
create  index Production_Order_Components_Warehouses_key on production_order_components (
id_warehouse
);

/*==============================================================*/
/* Index: PRODUCTION_ORDERS_PK                                  */
/*==============================================================*/
create unique index Production_Orders_PK on production_orders (
id_order_production
);

/*==============================================================*/
/* Index: Production_Orders_Labors                                               */
/*==============================================================*/
create  index Production_Orders_Labors on production_orders (
id_labor
);

/*==============================================================*/
/* Index: Production_Orders_Auth_Users_key                                              */
/*==============================================================*/
create  index Production_Orders_Auth_Users_key on production_orders (
id_user
);

/*==============================================================*/
/* Index: PRODUCTS_PK                                           */
/*==============================================================*/
create unique index Products_PK on products (
id_product
);

/*==============================================================*/
/* Table: purchasing_order_components                           */
/*==============================================================*/
create table purchasing_order_components (
   id_purchasing_order_components SERIAL                 not null,
   id_purchasing_order  INTEGER                 not null,
   id_product           INTEGER                 not null,
   quantity             INTEGER                 not null,
   price_base           MONEY                not null,
   vat                  INTEGER                 not null ,
   vat_value            MONEY                not null default 0,
   discount             REAL               not null default 0,
   discount_value      MONEY                not null default 0,
   line_total           MONEY                not null DEFAULT 0,
   constraint PK_PURCHASING_ORDER_COMPONENTS primary key (id_purchasing_order_components),
   constraint FK_PURCHASI_HAS_PURCHASI foreign key (id_purchasing_order)
      references purchasing_orders (id_purchasing_order)
      on delete restrict on update restrict,
   constraint FK_PURCHASI_HAS_PRODUCTS foreign key (id_product)
      references products (id_product)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Index: PURCHASING_ORDER_COMPONENTS_PK                        */
/*==============================================================*/
create unique index Purchasing_Order_Components_PK on purchasing_order_components (
id_purchasing_order_components
);

/*==============================================================*/
/* Index: Purchasing_Order_components_Purchasing_Order                                              */
/*==============================================================*/
create  index Purchasing_Order_components_Purchasing_Orders_key on purchasing_order_components (
id_purchasing_order
);

/*==============================================================*/
/* Index: Purchasing_Order_Components_Products_key                                           */
/*==============================================================*/
create  index Purchasing_Order_Components_Products_key on purchasing_order_components (
id_product
);

/*==============================================================*/
/* Index: PURCHASING_ORDERS_PK                                  */
/*==============================================================*/
create unique index Purchasing_Orders_PK on purchasing_orders (
id_purchasing_order
);

/*==============================================================*/
/* Index: Purchasing_Orders_Suppliers_key                                               */
/*==============================================================*/
create  index Purchasing_Orders_Suppliers_key on purchasing_orders (
id_supplier
);

/*==============================================================*/
/* Index: Purchasing_Orders_Auth_Users_key                                              */
/*==============================================================*/
create  index Purchasing_Orders_Auth_Users_key on purchasing_orders (
id_user
);

/*==============================================================*/
/* Table: sales_order_components                                */
/*==============================================================*/
create table sales_order_components (
   id_sales_order_component SERIAL                 not null,
   id_product           INTEGER                 not null,
   id_sale_order        INTEGER                 not null,
   quantity             INTEGER                 not null,
   price_base           MONEY                not null,
   vat                  INTEGER                 not null,
   vat_value            MONEY                not null default 0,
   discount             REAL               not null default 0,
   discount_value       MONEY                not null default 0,
   line_total           MONEY                not null default 0,
   constraint PK_SALES_ORDER_COMPONENTS primary key (id_sales_order_component),
   constraint FK_SALES_OR_HAS_SALES_OR foreign key (id_sale_order)
      references sales_orders (id_sale_order)
      on delete restrict on update restrict,
   constraint FK_SALES_OR_HAS_PRODUCTS foreign key (id_product)
      references products (id_product)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Index: SALES_ORDER_COMPONENTS_PK                             */
/*==============================================================*/
create unique index Sales_Order_Components_PK on sales_order_components (
id_sales_order_component
);

/*==============================================================*/
/* Index: Sales_Order_Components_Sales_Orders_key                                              */
/*==============================================================*/
create  index Sales_Order_Components_Sales_Orders_key on sales_order_components (
id_sale_order
);

/*==============================================================*/
/* Index: Sales_Order_Components_Products_key                                              */
/*==============================================================*/
create  index Sales_Order_Components_Products_key on sales_order_components (
id_product
);

/*==============================================================*/
/* Index: SALES_ORDERS_PK                                       */
/*==============================================================*/
create unique index Sales_Orders_PK on sales_orders (
id_sale_order
);

/*==============================================================*/
/* Index: Sales_Orders_Auth_Users_key                                               */
/*==============================================================*/
create  index Sales_Orders_Auth_Users_key on sales_orders (
id_user
);

/*==============================================================*/
/* Index: Sales_Orders_CInvoices_key                                                */
/*==============================================================*/
create  index Sales_Orders_CInvoices_key on sales_orders (
id_client_invoice
);

/*==============================================================*/
/* Table: stock                                                 */
/*==============================================================*/
create table stock (
   id_product           INTEGER                 not null,
   id_warehouse         INTEGER                 not null,
   quantity             INTEGER                 not null,
   constraint PK_STOCK primary key (id_product, id_warehouse),
   constraint FK_STOCK_HAS_PRODUCTS foreign key (id_product)
      references products (id_product)
      on delete restrict on update restrict,
   constraint FK_STOCK_HAS_WAREHOUS foreign key (id_warehouse)
      references warehouses (id_warehouse)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Index: HAS_PK                                                */
/*==============================================================*/
create unique index HAS_PK on stock (
id_product,
id_warehouse
);

/*==============================================================*/
/* Index: HAS_FK30                                              */
/*==============================================================*/
create  index HAS_FK30 on stock (
id_product
);

/*==============================================================*/
/* Index: HAS_FK31                                              */
/*==============================================================*/
create  index HAS_FK31 on stock (
id_warehouse
);


/*==============================================================*/
/* Table: stock_movements                                       */
/*==============================================================*/
CREATE TYPE MOVEMENT_STOCK_TYPE AS ENUM ('IN','OUT');
create table stock_movements (
   id_stock_movement    SERIAL                  not null,
   id_product           INTEGER                 not null,
   id_warehouse         INTEGER                 not null,
   quantity             INTEGER                 not null,
   type                 MOVEMENT_STOCK_TYPE     not null,
   reason               TEXT                    not null,
   id_reason            INTEGER                 not null,
    prev_quantity        INTEGER                not null,
    pos_quantity         INTEGER                not null,
    created_at           TIMESTAMPTZ                 not null default 'now()',
   constraint PK_STOCK_MOVEMENTS primary key (id_stock_movement),
   constraint FK_STOCK_MO_HAS_WAREHOUS foreign key (id_warehouse)
      references warehouses (id_warehouse)
      on delete restrict on update restrict,
   constraint FK_STOCK_MO_HAS_PRODUCTS foreign key (id_product)
      references products (id_product)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Index: STOCK_MOVEMENTS_PK                                    */
/*==============================================================*/
create unique index Stock_Movements_PK on stock_movements (
id_stock_movement
);

/*==============================================================*/
/* Index: HAS_FK7                                               */
/*==============================================================*/
create  index Stock_Movements_Warehouses_key on stock_movements (
id_warehouse
);

/*==============================================================*/
/* Index: HAS_FK8                                               */
/*==============================================================*/
create  index Stock_Movements_Products_key on stock_movements (
id_product
);

/*==============================================================*/
/* Index: SUPPLIER_INVOICES_PK                                  */
/*==============================================================*/
create unique index Stock_Movements_SInvoices_key on supplier_invoices (
id_supplier_invoice
);

/*==============================================================*/
/* Index: SUPPLIERS_PK                                          */
/*==============================================================*/
create unique index Suppliers_PK on suppliers (
id_supplier
);

/*==============================================================*/
/* Index: WAREHOUSES_PK                                         */
/*==============================================================*/
create unique index Warehouses_PK on warehouses (
id_warehouse
);

