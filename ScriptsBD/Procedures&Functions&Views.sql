-- ====================== MÓDULO DE STOCKS ======================

-- ProcArmazenado	warehouses	PA_Create_Warehouse(name,location)	Criar um armazém
CREATE OR REPLACE PROCEDURE PA_Create_Warehouse(
    _name TEXT,
    _location TEXT
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO warehouses (name, location)
    VALUES (_name, _location);
END;
$$;

-- ProcArmazenado	warehouses	PA_Update_Warehouse(id_warehouse,name,location)	Atualiza um armazém
CREATE OR REPLACE PROCEDURE PA_Update_Warehouse(
    _id_warehouse INT,
    _name TEXT,
    _location TEXT
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    UPDATE warehouses
    SET name     = _name,
        location = _location
    WHERE id_warehouse = _id_warehouse;
END;
$$;

-- View	warehouses	V_Warehouses	Lista todos os armazéns (com total de produtos em stock)
DROP VIEW IF EXISTS V_Warehouses CASCADE;
CREATE OR REPLACE VIEW V_Warehouses
            (
             id_warehouse,
             name,
             location,
             total_stock
                )
AS
SELECT wh.id_warehouse,
       wh.name,
       wh.location,
       COALESCE(SUM(quantity), 0) as total_stock
FROM warehouses wh
         LEFT JOIN stock USING (id_warehouse)
GROUP BY wh.id_warehouse;

-- View	stock	V_Stock	Listar quantidade por produto em armazéns
DROP VIEW IF EXISTS V_Stock CASCADE;
CREATE OR REPLACE VIEW V_Stock
            (id_product, id_warehouse, quantity, product_name, product_description, product_type, wharehouse_name) AS
SELECT stock.id_product,
       stock.id_warehouse,
       stock.quantity,
       products.name        as product_name,
       products.description as product_description,
       products.type        as product_type,
       warehouses.name      as warehouse_name
FROM stock
         INNER JOIN products USING (id_product)
         INNER JOIN warehouses USING (id_warehouse);

-- ProcArmazenado	stock	PA_InsertLine_Stock(id_warehouse,id_product,quantity)	Insere linha no stock
CREATE OR REPLACE FUNCTION FN_Create_Product(
    _name TEXT,
    _description TEXT,
    _type products_type,
    _weight REAL,
    _vat INT,
    _profit_margin REAL
)
    RETURNS INT
    LANGUAGE plpgsql
AS
$$
DECLARE
    _id_product INT;
BEGIN
    INSERT INTO products (name, description, type, weight, vat, profit_margin)
    VALUES (_name, _description, _type, _weight, _vat, _profit_margin)
    RETURNING id_product INTO _id_product;

    RETURN _id_product;
END;
$$;

-- ProcArmazenado	stock	PA_Update_Product(id_product,name,description TEXT,type products_type,weight,vat,profit_margin)	Atualiza um produto
CREATE OR REPLACE PROCEDURE PA_Update_Product(
    _id_product INT,
    _name TEXT,
    _description TEXT,
    _weight REAL,
    _vat INT,
    _profit_margin REAL
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    UPDATE products
    SET name          = _name,
        description   = _description,
        weight        = _weight,
        vat           = _vat,
        profit_margin = _profit_margin
    WHERE id_product = _id_product;
END;
$$;
-- View	products	V_Products	Listar todos os produtos
DROP VIEW IF EXISTS V_Products CASCADE;
CREATE OR REPLACE VIEW V_Products
            (id_product, name, description, weight, type, profit_margin, vat, price_cost, price_base, pvp) AS
SELECT id_product,
       name,
       description,
       weight,
       type,
       profit_margin,
       vat,
       price_cost,
       price_base,
       pvp
FROM products;


-- Function	stock	FN_AddProductToStock(id_warehouse,id_product,quantity,reason,id_reason)	Adiciona produto ao stock --REVER ESTA FUNCTION
CREATE OR REPLACE FUNCTION FN_AddProductToStock(
    _id_warehouse INT,
    _id_product INT,
    _quantity INT,
    _type movement_stock_type,
    _reason TEXT,
    id_reason INT
)
    RETURNS VOID AS
$$
DECLARE
    _previous_quantity INT;
    _pos_quantity      INT;
BEGIN

    SELECT s.quantity
    INTO _previous_quantity
    FROM stock s
    WHERE s.id_warehouse = _id_warehouse
      AND s.id_product = _id_product;

    IF _previous_quantity IS NULL THEN
        _previous_quantity := 0;
    END IF;

    _pos_quantity := _previous_quantity + _quantity;


    INSERT INTO stock_movements (id_warehouse, id_product, quantity, type, reason, id_reason, prev_quantity,
                                 pos_quantity)
    VALUES (_id_warehouse, _id_product, _quantity, _type, _reason, id_reason, _previous_quantity, _pos_quantity);

    IF _previous_quantity = 0 THEN
        INSERT INTO stock (id_warehouse, id_product, quantity)
        VALUES (_id_warehouse, _id_product, _quantity);
    ELSE
        UPDATE stock
        SET quantity = _pos_quantity
        WHERE id_warehouse = _id_warehouse
          AND id_product = _id_product;

    END IF;

END;
$$
    LANGUAGE plpgsql;


-- Function	stock	FN_RemoveProductFromStock(id_warehouse,id_product,quantity,reason,id_reason)	Remove produto do stock --REVER ESTA FUNCTION
CREATE OR REPLACE FUNCTION FN_RemoveProductFromStock(
    _id_warehouse INT,
    _id_product INT,
    _quantity INT,
    _type movement_stock_type,
    _reason TEXT,
    id_reason INT
)
    RETURNS INT AS
$$
DECLARE
    _previous_quantity INT;
    _pos_quantity      INT;
BEGIN

    IF _id_warehouse = 0 THEN
        -- Se não for especificado o armazém, então vamos buscar o primeiro armazém onde exista stock e verificamos se tem quantidade suficiente se não houver stock suficiente, então lançamos uma exceção
        SELECT s.id_warehouse
        INTO _id_warehouse
        FROM stock s
        WHERE s.id_product = _id_product
          AND s.quantity >= _quantity
        LIMIT 1;

        IF _id_warehouse IS NULL THEN
            RAISE EXCEPTION 'Não existe stock suficiente';
        END IF;

    END IF;

    SELECT s.quantity
    INTO _previous_quantity
    FROM stock s
    WHERE s.id_warehouse = _id_warehouse
      AND s.id_product = _id_product;

    _pos_quantity := _previous_quantity - _quantity;

    INSERT INTO stock_movements (id_warehouse, id_product, quantity, type, reason, id_reason, prev_quantity,
                                 pos_quantity)
    VALUES (_id_warehouse, _id_product, _quantity, _type, _reason, id_reason, _previous_quantity, _pos_quantity);

    IF _pos_quantity < 0 THEN
        RAISE EXCEPTION 'Não existe stock suficiente';
    ELSE
        UPDATE stock
        SET quantity = _pos_quantity
        WHERE id_warehouse = _id_warehouse
          AND id_product = _id_product;

    END IF;

    RETURN _pos_quantity;
END;
$$
    LANGUAGE plpgsql;

-- ProcArmazenado	stock	PA_InsertLine_Stock(id_warehouse,id_product,quantity)	Insere linha no stock

CREATE OR REPLACE PROCEDURE PA_InsertLine_SupplierInvoice(
    _id_supplier_invoice INT,
    _id_product INT,
    _quantity INT,
    _price_base MONEY,
    _vat INT,
    _discount REAL DEFAULT 0
)
AS
$$
BEGIN
    INSERT INTO supplier_invoice_components (id_supplier_invoice, id_product, quantity, price_base, vat, discount)
    VALUES (_id_supplier_invoice, _id_product, _quantity, _price_base, _vat, _discount);
END;
$$
    LANGUAGE plpgsql;


-- View	stock_movements	V_StockPerProduct	Listar movimentos de stock
DROP VIEW IF EXISTS V_StockPerProduct;
CREATE OR REPLACE VIEW V_StockPerProduct
            (
             id_product,
             product_name,
             id_warehouse,
             warehouse_name,
             total_quantity,
             product_type,
             product_weight
                )
AS
SELECT p.id_product,
       p.name     AS product_name,
       s.id_warehouse,
       w.name     AS warehouse_name,
       s.quantity AS total_quantity,
       p.type     AS product_type,
       p.weight   AS product_weight
FROM stock s
         INNER JOIN warehouses w ON s.id_warehouse = w.id_warehouse
         RIGHT JOIN products p ON s.id_product = p.id_product;

-- View stock_movements V_Stock

DROP VIEW IF EXISTS V_Movements;
CREATE OR REPLACE VIEW V_Movements
            (
             id_stock_movement,
             quantity,
             type,
             reason,
             id_reason,
             prev_quantity,
             pos_quantity,
             created_at,
             id_product,
             product_name,
             id_warehouse,
             warehouse_name
                )
AS
SELECT sm.id_stock_movement,
       sm.quantity,
       sm.type,
       sm.reason,
       sm.id_reason,
       sm.prev_quantity,
       sm.pos_quantity,
       sm.created_at,
       p.id_product,
       p.name AS product_name,
       w.id_warehouse,
       w.name AS warehouse_name
FROM stock_movements sm
         INNER JOIN products p USING (id_product)
         INNER JOIN warehouses w USING (id_warehouse);


-- View FN_ExistsStock(id_product,id_warehouse) Verifica se existe stock de um produto num armazém
CREATE OR REPLACE FUNCTION FN_ExistsStock(
    _id_warehouse INT,
    _id_product INT
)
    RETURNS INT AS
$$
DECLARE
    _quantity INT;
BEGIN
    SELECT COALESCE(SUM(s.quantity), 0)
    INTO _quantity
    FROM stock s
    WHERE s.id_warehouse = _id_warehouse
      AND s.id_product = _id_product;

    RETURN _quantity;
END;
$$
    LANGUAGE plpgsql;


-- ====================== MÓDULO COMPRAS ======================

-- Criar um fornecedor
CREATE OR REPLACE PROCEDURE PA_Create_Supplier(
    _name TEXT,
    _email TEXT,
    _nif TEXT,
    _phone TEXT,
    _address TEXT,
    _locality TEXT,
    _postal_code TEXT
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO suppliers (name, email, nif, phone, address, locality, postal_code)
    VALUES (_name, _email, _nif, _phone, _address, _locality, _postal_code);
END;
$$;

-- Atualizar um fornecedor
CREATE OR REPLACE PROCEDURE PA_Update_Supplier(
    _id_supplier INT,
    _name TEXT,
    _email TEXT,
    _nif TEXT,
    _phone TEXT,
    _address TEXT,
    _locality TEXT,
    _postal_code TEXT
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    UPDATE suppliers
    SET name        = _name,
        email       = _email,
        nif         = _nif,
        phone       = _phone,
        address     = _address,
        locality    = _locality,
        postal_code = _postal_code
    WHERE id_supplier = _id_supplier;
END;
$$;

-- Listar todos os fornecedores
DROP VIEW IF EXISTS V_Suppliers;
CREATE OR REPLACE VIEW V_Suppliers
            (
             id_supplier,
             name,
             email,
             nif,
             phone,
             address,
             locality,
             postal_code
                )
AS
SELECT id_supplier,
       name,
       email,
       nif,
       phone,
       address,
       locality,
       postal_code
FROM suppliers;

-- Function	purchasing_orders	FN_Create_PurchasingOrder(id_supplier,id_user,delivery_date,obs<O>) : id_purchasing_order	Criar cabeçalho Pedido de compra, devolve id do pedido
CREATE OR REPLACE FUNCTION FN_Create_PurchasingOrder(
    _id_supplier INT,
    _id_user INT,
    _delivery_date DATE,
    _obs TEXT = NULL
)
    RETURNS INT
    LANGUAGE plpgsql
AS
$$
DECLARE
    _id_purchasing_order INT;
BEGIN
    INSERT INTO purchasing_orders (id_supplier, id_user, delivery_date, obs)
    VALUES (_id_supplier, _id_user, _delivery_date, _obs)
    RETURNING id_purchasing_order INTO _id_purchasing_order;

    RETURN _id_purchasing_order;
END;
$$;

-- ProcArmazenado	purchasing_order_components	PA_InsertLine_PurchasingOrder(id_purchasing_order,id_product,quantity,price_base,VAT,discount)	Insere componente no pedido de compra
CREATE OR REPLACE PROCEDURE PA_InsertLine_PurchasingOrder(
    _id_purchasing_order INT,
    _id_product INT,
    _quantity INT,
    _price_base MONEY,
    _vat INT,
    _discount INT = 0
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO purchasing_order_components (id_purchasing_order, id_product, quantity, price_base, vat, discount)
    VALUES (_id_purchasing_order, _id_product, _quantity, _price_base, _vat, _discount);
END;
$$;

/**
    Antes de inserir a linha de uma ordem de compra, temos de atualizar os valores totais da própria linha e depois atualizar os valores totais da ordem de compra
*/
DROP FUNCTION IF EXISTS TR_purchasing_order_components_PRE_INS() CASCADE;
CREATE OR REPLACE FUNCTION TR_purchasing_order_components_PRE_INS() RETURNS TRIGGER AS
$$
DECLARE
    _vat_value      MONEY;
    _discount_value MONEY;
    _line_total     MONEY;
    _total_base     MONEY;
    _vat_total      MONEY;
    _discount_total MONEY;
    _total          MONEY;
BEGIN
    _vat_value := NEW.price_base * (NEW.vat / 100.0) * NEW.quantity;
    _discount_value := NEW.price_base * (NEW.discount / 100.0) * NEW.quantity;
    _line_total := (NEW.price_base * NEW.quantity) + _vat_value - _discount_value;


    NEW.vat_value := _vat_value;
    NEW.discount_value := _discount_value;
    NEW.line_total := _line_total;

    _total_base := (SELECT COALESCE(SUM(price_base * quantity), 0::MONEY)
                    FROM purchasing_order_components
                    WHERE id_purchasing_order = NEW.id_purchasing_order) + NEW.price_base * NEW.quantity;
    _vat_total := (SELECT COALESCE(SUM(vat_value), 0::MONEY)
                   FROM purchasing_order_components
                   WHERE id_purchasing_order = NEW.id_purchasing_order) + _vat_value;
    _discount_total := (SELECT COALESCE(SUM(discount_value), 0::MONEY)
                        FROM purchasing_order_components
                        WHERE id_purchasing_order = NEW.id_purchasing_order) + _discount_value;
    _total := _total_base + _vat_total - _discount_total;

    UPDATE purchasing_orders
    SET total_base     = _total_base,
        vat_total      = _vat_total,
        discount_total = _discount_total,
        total          = _total
    WHERE id_purchasing_order = NEW.id_purchasing_order;


    IF
            (SELECT COUNT(*)
             FROM purchasing_order_components
             WHERE id_purchasing_order = NEW.id_purchasing_order
               AND id_product = NEW.id_product)
            > 0
    THEN

        UPDATE purchasing_order_components
        SET quantity       = quantity + NEW.quantity,
            vat_value      = _vat_total,
            discount_value = _discount_total,
            line_total     = (quantity + NEW.quantity) * price_base
        WHERE id_purchasing_order = NEW.id_purchasing_order
          AND id_product = NEW.id_product;

        RETURN NULL;
    END IF;


    RETURN NEW;
END;

$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER TR_purchasing_order_components_PRE_INS
    BEFORE INSERT
    ON purchasing_order_components
    FOR EACH ROW
EXECUTE PROCEDURE TR_purchasing_order_components_PRE_INS();


-- ProcArmazenado	purchasing_order_components	PA_InsertLine_PurchasingOrder(id_purchasing_order,id_product,quantity,price_base,VAT,discount)	Insere componente no pedido de compra
CREATE OR REPLACE PROCEDURE PA_InsertLine_PurchasingOrder(
    _id_purchasing_order INT,
    _id_product INT,
    _quantity INT,
    _price_base MONEY,
    _vat INT,
    _discount INT = 0
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO purchasing_order_components (id_purchasing_order, id_product, quantity, price_base, vat, discount)
    VALUES (_id_purchasing_order, _id_product, _quantity, _price_base, _vat, _discount);
END;
$$;


-- View	purchasing_orders	V_PurchasingOrders	Listar as ordens de compra (cabeçalho)
DROP VIEW IF EXISTS V_PurchasingOrders;
CREATE OR REPLACE VIEW V_PurchasingOrders
            (
             id_purchasing_order,
             id_supplier,
             supplier_name,
             id_user,
             user_name,
             delivery_date,
             created_at,
             obs,
             total_base,
             vat_total,
             discount_total,
             total
                )
AS
SELECT po.id_purchasing_order,
       po.id_supplier,
       s.name     AS supplier_name,
       po.id_user,
       u.username AS user_name,
       po.delivery_date,
       po.created_at,
       po.obs,
       po.total_base,
       po.vat_total,
       po.discount_total,
       po.total
FROM purchasing_orders po
         INNER JOIN suppliers s USING (id_supplier)
         INNER JOIN auth_user u ON po.id_user = u.id;

-- View	purchasing_order_components	V_PurchasingOrderComponents	Listar as linhas das ordens de compra
DROP VIEW IF EXISTS V_PurchasingOrderComponents CASCADE;

CREATE OR REPLACE VIEW V_PurchasingOrderComponents
            (
             id_purchasing_order_components,
             id_product,
             product_name,
             quantity,
             price_base,
             total_unit,
             vat,
             vat_value,
             discount,
             discount_value,
             line_total,
             id_purchasing_order
                )
AS
SELECT poc.id_purchasing_order_components,
       poc.id_product,
       p.name                        as product_name,
       poc.quantity,
       poc.price_base,
       poc.quantity * poc.price_base as total_unit,
       poc.vat,
       poc.vat_value,
       poc.discount,
       poc.discount_value,
       poc.line_total,
       poc.id_purchasing_order
FROM purchasing_order_components poc
         INNER JOIN products p USING (id_product);

-- Function	material_receipts	FN_Create_MaterialReceipts(id_user,id_purchasing_order,n_delivery_note,obs<O>) : id_material_receipt	Criar cabeçalho Receção de material, devolve id da receção
CREATE OR REPLACE FUNCTION FN_Create_MaterialReceipts(
    _id_user INT,
    _id_purchasing_order INT,
    _n_delivery_note TEXT,
    _obs TEXT = NULL
)
    RETURNS INT
    LANGUAGE plpgsql
AS
$$
DECLARE
    _id_material_receipt INT;
BEGIN
    INSERT INTO material_receipts (id_user, id_purchasing_order, n_delivery_note, obs)
    VALUES (_id_user, _id_purchasing_order, _n_delivery_note, _obs)
    RETURNING id_material_receipt INTO _id_material_receipt;

    RETURN _id_material_receipt;
END;
$$;
-- ProcArmazenado	material_receipt_components	PA_InsertLine_MaterialReceipt(id_material_receipt,id_product,quantity,price_base,VAT,discount)	Insere componente na receção de material
CREATE OR REPLACE PROCEDURE PA_InsertLine_MaterialReceipt(
    _id_material_receipt INT,
    _id_product INT,
    _id_warehouse INT,
    _quantity INT,
    _price_base MONEY,
    _vat INT,
    _discount REAL DEFAULT 0
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO material_receipt_components (id_material_receipt,
                                             id_product,
                                             id_warehouse,
                                             quantity,
                                             price_base,
                                             vat,
                                             discount)
    VALUES (_id_material_receipt,
            _id_product,
            _id_warehouse,
            _quantity,
            _price_base,
            _vat,
            _discount);
END;
$$;

/**
    Função que dado um id de um produto, vai procurar todas as linhas de receções de material com esse produto e calcula o preço médio do produto
*/

CREATE OR REPLACE FUNCTION FN_GetProductAveragePriceByMaterialReceipts(
    _id_product INT
)
    RETURNS MONEY AS
$$
DECLARE
    _total_quantity INT;
    _total_price    MONEY;
    _average_price  MONEY;
BEGIN
    SELECT COALESCE(SUM(quantity), 0)::int
    INTO _total_quantity
    FROM material_receipt_components
    WHERE id_product = _id_product;

    SELECT COALESCE(SUM(price_base * quantity), 0::money)::money
    INTO _total_price
    FROM material_receipt_components
    WHERE id_product = _id_product;

    IF _total_quantity = 0 THEN
        RETURN 0::money;
    END IF;

    _average_price := _total_price::money / _total_quantity;

    RETURN _average_price::money;
END;
$$
    LANGUAGE plpgsql;


/**
    Depois de inserir/atualizar/eliminar a linha de uma receção de material, temos de atualizar os valores totais da própria linha e depois atualizar os valores totais da receção de material, e dar entrada nos movimentos de stock (stock_movements)
*/
DROP FUNCTION IF EXISTS TR_material_receipt_components_PRE_INS() CASCADE;
CREATE OR REPLACE FUNCTION TR_material_receipt_components_PRE_INS() RETURNS TRIGGER AS
$$
DECLARE
    _vat_value         MONEY;
    _discount_value    MONEY;
    _line_total        MONEY;
    _total_base        MONEY;
    _vat_total         MONEY;
    _discount_total    MONEY;
    _total             MONEY;
    _new_product_price MONEY;
BEGIN
    _vat_value := NEW.price_base * (NEW.vat / 100.0) * NEW.quantity;
    _discount_value := NEW.price_base * (NEW.discount / 100.0) * NEW.quantity;
    _line_total := (NEW.price_base * NEW.quantity) + _vat_value - _discount_value;


    NEW.vat_value := _vat_value;
    NEW.discount_value := _discount_value;
    NEW.line_total := _line_total;

    _total_base := (SELECT COALESCE(SUM(price_base * quantity), 0::MONEY)
                    FROM material_receipt_components
                    WHERE id_material_receipt = NEW.id_material_receipt) + NEW.price_base * NEW.quantity;

    _vat_total := (SELECT COALESCE(SUM(vat_value), 0::MONEY)
                   FROM material_receipt_components
                   WHERE id_material_receipt = NEW.id_material_receipt) + _vat_value;

    _discount_total := (SELECT COALESCE(SUM(discount_value), 0::MONEY)
                        FROM material_receipt_components
                        WHERE id_material_receipt = NEW.id_material_receipt) + _discount_value;

    _total := _total_base + _vat_total - _discount_total;

    UPDATE material_receipts
    SET total_base     = _total_base,
        vat_total      = _vat_total,
        discount_total = _discount_total,
        total          = _total
    WHERE id_material_receipt = NEW.id_material_receipt;


    SELECT FN_GetProductAveragePriceByMaterialReceipts(NEW.id_product) INTO _new_product_price;

    RAISE NOTICE 'Novo preço médio: %', _new_product_price;

    UPDATE products
    SET price_cost = _new_product_price
    WHERE id_product = NEW.id_product;

    IF
            (SELECT COUNT(*)
             FROM material_receipt_components
             WHERE id_material_receipt = NEW.id_material_receipt
               AND id_product = NEW.id_product
               AND id_warehouse = NEW.id_warehouse)
            > 0
    THEN

        UPDATE material_receipt_components
        SET quantity       = quantity + NEW.quantity,
            vat_value      = _vat_total,
            discount_value = _discount_total,
            line_total     = (quantity + NEW.quantity) * price_base
        WHERE id_material_receipt = NEW.id_material_receipt
          AND id_product = NEW.id_product
          AND id_warehouse = NEW.id_warehouse;

        PERFORM FN_AddProductToStock(NEW.id_warehouse, NEW.id_product, NEW.quantity, 'IN', 'material_receipt',
                                 NEW.id_material_receipt);

        RETURN NULL;
    END IF;

    -- Entrada no stock
    PERFORM FN_AddProductToStock(NEW.id_warehouse, NEW.id_product, NEW.quantity, 'IN', 'material_receipt',
                                 NEW.id_material_receipt);
    RETURN NEW;

END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TR_material_receipt_components_PRE_INS
    BEFORE INSERT
    ON material_receipt_components
    FOR EACH ROW
EXECUTE FUNCTION TR_material_receipt_components_PRE_INS();


-- View	material_receipts	V_MaterialReceipts	Listar as receções de material (cabeçalho) --REVER ESTA VIEW
DROP VIEW IF EXISTS V_MaterialReceipts CASCADE;
CREATE OR REPLACE VIEW V_MaterialReceipts
            (
             id_material_receipt,
             id_purchasing_order,
             id_supplier,
             supplier_name,
             id_user,
             user_name,
             n_delivery_note,
             obs,
             created_at,
             total_base,
             vat_total,
             discount_total,
             total
                )
AS
SELECT mr.id_material_receipt,
       mr.id_purchasing_order,
       s.id_supplier,
       s.name     AS supplier_name,
       u.id       AS id_user,
       u.username AS user_name,
       mr.n_delivery_note,
       mr.obs,
       mr.created_at,
       mr.total_base,
       mr.vat_total,
       mr.discount_total,
       mr.total
FROM material_receipts mr
         INNER JOIN
     purchasing_orders po ON mr.id_purchasing_order = po.id_purchasing_order
         INNER JOIN
     suppliers s USING (id_supplier)
         INNER JOIN
     auth_user u ON mr.id_user = u.id;

-- View	material_receipt_components	V_MaterialReceiptComponents	Listar as linhas das receções de material
DROP VIEW IF EXISTS V_MaterialReceiptComponents CASCADE;
CREATE OR REPLACE VIEW V_MaterialReceiptComponents
            (
             id_material_receipt_component,
             id_product,
             product_name,
             id_warehouse,
             warehouse_name,
             quantity,
             price_base,
             total_unit,
             vat,
             vat_value,
             discount,
             discount_value,
             line_total,
             id_material_receipt
                )
AS
SELECT mrc.id_material_receipt_component,
       mrc.id_product,
       p.name                        AS product_name,
       w.id_warehouse,
       w.name                        AS warehouse_name,
       mrc.quantity,
       mrc.price_base,
       mrc.quantity * mrc.price_base AS total_unit,
       mrc.vat,
       mrc.vat_value,
       mrc.discount,
       mrc.discount_value,
       mrc.line_total,
       mrc.id_material_receipt
FROM material_receipt_components mrc
         INNER JOIN products p USING (id_product)
         INNER JOIN warehouses w USING (id_warehouse);

-- ProcArmazenado	supplier_invoices	PA_Create_SupplierInvoice(id_material_receipt[],id_supplier,invoice_id,invoice_date,expire_date,obs<O>) : id_supplier_invoice	Criar cabeçalho Fatura de fornecedor, devolve id da fatura
CREATE OR REPLACE FUNCTION FN_Create_SupplierInvoice(
    _id_material_receipt INT[],
    _id_supplier INT,
    _invoice_id TEXT,
    _invoice_date DATE,
    _expire_date DATE,
    _obs TEXT DEFAULT NULL
)
    RETURNS INT AS
$$
DECLARE
    _id_supplier_invoice INT;
    _id                  INT;
BEGIN
    INSERT INTO supplier_invoices (id_supplier,invoice_id, invoice_date, expire_date, obs)
    VALUES (_id_supplier, _invoice_id, _invoice_date, _expire_date, _obs)
    RETURNING id_supplier_invoice INTO _id_supplier_invoice;

    FOR _id IN SELECT unnest(_id_material_receipt)
        LOOP
            UPDATE material_receipts
            SET id_supplier_invoice = _id_supplier_invoice
            WHERE id_material_receipt = _id;
        END LOOP;

    RETURN _id_supplier_invoice;
END;
$$
    LANGUAGE plpgsql;

-- Trigger	supplier_invoice_components	TR_supplier_invoice_components_PRE_INS	Depois de inserir/atualizar/eliminar a linha de uma fatura de fornecedor, temos de atualizar os valores totais da própria linha e depois atualizar os valores totais da fatura de fornecedor
DROP FUNCTION IF EXISTS TR_supplier_invoice_components_PRE_INS() CASCADE;
CREATE OR REPLACE FUNCTION TR_supplier_invoice_components_PRE_INS() RETURNS TRIGGER AS
$$
DECLARE
    _vat_value      MONEY;
    _discount_value MONEY;
    _line_total     MONEY;
    _total_base     MONEY;
    _vat_total      MONEY;
    _discount_total MONEY;
    _total          MONEY;
BEGIN
    _vat_value := NEW.price_base * (NEW.vat / 100.0) * NEW.quantity;
    _discount_value := NEW.price_base * (NEW.discount / 100.0) * NEW.quantity;
    _line_total := (NEW.price_base * NEW.quantity) + _vat_value - _discount_value;


    NEW.vat_value := _vat_value;
    NEW.discount_value := _discount_value;
    NEW.line_total := _line_total;

    _total_base := (SELECT COALESCE(SUM(price_base * quantity), 0::MONEY)
                    FROM supplier_invoice_components
                    WHERE id_supplier_invoice = NEW.id_supplier_invoice) + NEW.price_base * NEW.quantity;

    _vat_total := (SELECT COALESCE(SUM(vat_value), 0::MONEY)
                   FROM supplier_invoice_components
                   WHERE id_supplier_invoice = NEW.id_supplier_invoice) + _vat_value;

    _discount_total := (SELECT COALESCE(SUM(discount_value), 0::MONEY)
                        FROM supplier_invoice_components
                        WHERE id_supplier_invoice = NEW.id_supplier_invoice) + _discount_value;

    _total := _total_base + _vat_total - _discount_total;

    UPDATE supplier_invoices
    SET total_base     = _total_base,
        vat_total      = _vat_total,
        discount_total = _discount_total,
        total          = _total
    WHERE id_supplier_invoice = NEW.id_supplier_invoice;

    IF
            (SELECT COUNT(*)
             FROM supplier_invoice_components
             WHERE id_supplier_invoice = NEW.id_supplier_invoice
               AND id_product = NEW.id_product)
            > 0
    THEN

        UPDATE supplier_invoice_components
        SET quantity       = quantity + NEW.quantity,
            vat_value      = _vat_total,
            discount_value = _discount_total,
            line_total     = (quantity + NEW.quantity) * price_base
        WHERE id_supplier_invoice = NEW.id_supplier_invoice
          AND id_product = NEW.id_product;

        RETURN NULL;

    END IF;

    RETURN NEW;

END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TR_supplier_invoice_components_PRE_INS
    BEFORE INSERT
    ON supplier_invoice_components
    FOR EACH ROW
EXECUTE FUNCTION TR_supplier_invoice_components_PRE_INS();

-- View	supplier_invoices	V_SupplierInvoices	Listar as faturas de fornecedor (cabeçalho)
DROP VIEW IF EXISTS V_SupplierInvoices CASCADE;

CREATE OR REPLACE VIEW V_SupplierInvoices
            (
             id_supplier_invoice,
             id_supplier,
             supplier_name,
             supplier_address,
             supplier_locality,
             supplier_postal_code,
             supplier_nif,
             material_receptions,
             invoice_id,
             invoice_date,
             expire_date,
             obs,
             total_base,
             vat_total,
             discount_total,
             total,
             created_at
                )
AS
SELECT si.id_supplier_invoice,
       si.id_supplier,
       s.name                            AS supplier_name,
       s.address                         AS supplier_address,
       s.locality                        AS supplier_locality,
       s.postal_code                     AS supplier_postal_code,
       s.nif                             AS supplier_nif,
       ARRAY_AGG(mr.id_material_receipt) AS material_receptions,
       si.invoice_id,
       si.invoice_date,
       si.expire_date,
       si.obs,
       si.total_base,
       si.vat_total,
       si.discount_total,
       si.total,
       si.created_at
FROM supplier_invoices si
         INNER JOIN
     suppliers s USING (id_supplier)
         INNER JOIN
     material_receipts mr ON si.id_supplier_invoice = mr.id_supplier_invoice
GROUP BY si.id_supplier_invoice,
         si.id_supplier,
         s.name,
         s.address,
         s.locality,
         s.postal_code,
         s.nif,
         si.invoice_id,
         si.invoice_date,
         si.expire_date,
         si.obs;

-- View	supplier_invoice_components	V_SupplierInvoiceComponents	Listar as linhas das faturas de fornecedor
DROP VIEW IF EXISTS V_SupplierInvoiceComponents CASCADE;
CREATE OR REPLACE VIEW V_SupplierInvoiceComponents
            (
             id_supplier_invoice_component,
             id_supplier_invoice,
             id_product,
             product_name,
             quantity,
             price_base,
             total_unit,
             vat,
             vat_value,
             discount,
             discount_value,
             line_total
                )
AS
SELECT sic.id_supplier_invoice_component,
       sic.id_supplier_invoice,
       sic.id_product,
       p.name                        AS product_name,
       sic.quantity,
       sic.price_base,
       sic.quantity * sic.price_base AS total_unit,
       sic.vat,
       sic.vat_value,
       sic.discount,
       sic.discount_value,
       sic.line_total
FROM supplier_invoice_components sic
         INNER JOIN products p USING (id_product);


-- ====================== MÓDULO PRODUÇÃO ======================

-- Criar mão de obra
CREATE OR REPLACE PROCEDURE PA_Create_Labor(
    IN _title TEXT,
    IN _cost MONEY
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO labors (title, cost)
    VALUES (_title, _cost);
END;
$$;

--Atualiza uma mão de obra
CREATE OR REPLACE PROCEDURE PA_Update_Labor(
    IN _id_labor INTEGER,
    IN _title TEXT,
    IN _cost MONEY
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    UPDATE labors
    SET title = _title,
        cost  = _cost
    WHERE id_labor = _id_labor;
END;
$$;

--Listar as mão de obra
CREATE OR REPLACE VIEW V_Labors
            (
             id_labor,
             title,
             cost
                )
AS
SELECT id_labor,
       title,
       cost
FROM labors;

-- Function production_orders FN_Create_ProductionOrder(id_labor,id_product,id_django,equipment_quantity,obs<O>):id_production_order Cria o cabeçalho de uma ordem de produção, devolve id_produção

CREATE OR REPLACE FUNCTION FN_Create_ProductionOrder(
    IN _id_labor INTEGER,
    IN _id_user INTEGER,
    IN _id_product INTEGER,
    IN _equipment_quantity INTEGER,
    IN _id_warehouse INTEGER DEFAULT NULL, --Não existe nenhum armazém associado à ordem de produção só aos produtos que a compõem
    IN _obs TEXT DEFAULT NULL
)
    RETURNS INTEGER
    LANGUAGE plpgsql
AS
$$
DECLARE
    _id_order_production INTEGER;
BEGIN
    INSERT INTO production_orders (id_labor, id_user, id_product, equipment_quantity, id_warehouse, obs)
    VALUES (_id_labor, _id_user, _id_product, _equipment_quantity, _id_warehouse, _obs)
    RETURNING id_order_production INTO _id_order_production;

    RETURN _id_order_production;
END;
$$;
-- ProcArmazenado production_order_components PA_InsertLine_ProductionOrder(id_production_order,id_product,quantity,price_base,VAT,discount) Insere componente na ordem de produção
CREATE OR REPLACE PROCEDURE PA_InsertLine_ProductionOrder(
    IN _id_production_order INTEGER,
    IN _id_product INTEGER,
    IN _id_warehouse INTEGER,
    IN _quantity INTEGER
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO production_order_components (id_order_production, id_product, id_warehouse, quantity)
    VALUES (_id_production_order, _id_product, _id_warehouse, _quantity);
END;
$$;
-- Trigger production_order_components TR_production_order_components_PRE_INS Depois de inserir/atualizar/eliminar a linha de uma ordem de produção, temos de atualizar os valores totais da própria linha e depois atualizar os valores totais da ordem de produção e dar saída nos movimentos de stock (stock_movements)
DROP FUNCTION IF EXISTS TR_production_order_components_PRE_INS() CASCADE;
CREATE OR REPLACE FUNCTION TR_production_order_components_PRE_INS() RETURNS TRIGGER AS
$$
DECLARE
    _line_total      MONEY;
    _production_cost MONEY;
    _unit_cost       MONEY;
    _quantity        INTEGER;
BEGIN
    -- Obter o preço base do produto
    SELECT price_base
    INTO NEW.price_base
    FROM products
    WHERE id_product = NEW.id_product;

    --Obter quantidade antiga caso o componente já esteja na tabela
    _quantity := (SELECT COALESCE(quantity, 0)
                  FROM production_order_components
                  WHERE id_order_production = NEW.id_order_production
                    AND id_product = NEW.id_product);

    -- Se _quantity for NULL, define como 0
    IF _quantity IS NULL THEN
        _quantity := 0;
    END IF;
    --quantidade total a contar com a nova que vai entrar
    _quantity = _quantity + NEW.quantity;

    RAISE NOTICE 'quantity: %',_quantity;

    -- Calcular o total da linha (price_base * _quantity) quantidade total
    NEW.line_total := NEW.price_base * _quantity;
    RAISE NOTICE 'NEW.line_total: %', NEW.line_total;

    -- Calcular o custo de produção por componente
    _unit_cost := (SELECT SUM(price_base * quantity)
                   FROM production_order_components
                   WHERE id_order_production = NEW.id_order_production);

    -- Se _unit_cost for NULL, define como preço_base * quantidade, se não apenas adiciona ao custo unitário preço_base * quantidade
    IF _unit_cost IS NULL THEN
        _unit_cost := (NEW.quantity * NEW.price_base);
    ELSE
        _unit_cost := _unit_cost + (NEW.quantity * NEW.price_base);
    END IF;


    RAISE NOTICE '_unit_cost: %', _unit_cost;

    -- Atualizar o custo unitário na tabela de ordens de produção
    UPDATE production_orders
    SET unit_cost = _unit_cost
    WHERE id_order_production = NEW.id_order_production;
    RAISE NOTICE 'Unit cost updated';

    -- Atualizar o custo total de produção na tabela de ordens de produção
    UPDATE production_orders
    SET production_cost = unit_cost * equipment_quantity
    WHERE id_order_production = NEW.id_order_production;
    RAISE NOTICE 'Production cost updated';

    -- Verificar se o componente já existe na ordem de produção
    IF EXISTS (SELECT 1
               FROM production_order_components
               WHERE id_order_production = NEW.id_order_production
                 AND id_product = NEW.id_product
                 AND id_warehouse = NEW.id_warehouse) THEN
        -- Atualizar a quantidade e o total da linha do componente existente
        UPDATE production_order_components
        SET quantity = _quantity
        WHERE id_order_production = NEW.id_order_production
          AND id_product = NEW.id_product
          AND id_warehouse = NEW.id_warehouse;
        RAISE NOTICE 'Component quantity and line total updated';

        RETURN NULL;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER TR_production_order_components_PRE_INS
    BEFORE INSERT
    ON production_order_components
    FOR EACH ROW
EXECUTE FUNCTION TR_production_order_components_PRE_INS();



DROP FUNCTION IF EXISTS TR_production_order_PRE_UPD() CASCADE;
CREATE OR REPLACE FUNCTION TR_production_order_PRE_UPD() RETURNS TRIGGER AS
$$
DECLARE
    _line RECORD;
BEGIN

    IF (NEW.status = 'COMPLETED') THEN
        FOR _line IN SELECT * FROM production_order_components WHERE id_order_production = NEW.id_order_production
            LOOP
                PERFORM FN_RemoveProductFromStock(_line.id_warehouse, _line.id_product, _line.quantity, 'OUT',
                                                  'production_order', NEW.id_order_production);
            END LOOP;
        PERFORM FN_AddProductToStock(NEW.id_warehouse, NEW.id_product, NEW.equipment_quantity, 'IN', 'production_order',
                                     NEW.id_order_production);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER TR_production_order_PRE_UDP
    BEFORE UPDATE
    ON production_orders
    FOR EACH ROW
EXECUTE FUNCTION TR_production_order_PRE_UPD();

-- ProcArmazenado pa_update_production_order_status(id_production_order,status) Atualiza o estado de uma ordem de produção
CREATE OR REPLACE PROCEDURE PA_Update_ProductionOrderStatus(
    IN _id_production_order INTEGER,
    IN _status production_order_status
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    UPDATE production_orders
    SET status = _status
    WHERE id_order_production = _id_production_order;
END;
$$;

-- View production_orders V_ProductionOrders Listar as ordens de produção (cabeçalho)
DROP VIEW IF EXISTS V_ProductionOrders CASCADE;
CREATE OR REPLACE VIEW V_ProductionOrders
            (
             id_order_production,
             id_labor,
             labor_cost,
             id_user,
             user_name,
             id_product,
             product_name,
             equipment_quantity,
             production_cost,
             unit_cost,
             status,
             created_at,
             last_updated,
             obs
                )
AS
SELECT po.id_order_production,
       po.id_labor,
       l.cost     AS labor_cost,
       po.id_user,
       u.username AS user_name,
       po.id_product,
       p.name     AS product_name,
       po.equipment_quantity,
       po.production_cost,
       po.unit_cost,
       po.status,
       po.created_at,
       po.last_updated,
       po.obs
FROM production_orders po
         INNER JOIN
     labors l USING (id_labor)
         INNER JOIN
     products p USING (id_product)
         INNER JOIN
     auth_user u ON po.id_user = u.id;

-- View production_order_components V_ProductionOrderComponents Listar as linhas das ordens de produção
DROP VIEW IF EXISTS V_ProductionOrderComponents CASCADE;
CREATE OR REPLACE VIEW V_ProductionOrderComponents
            (
             id_production_order_components,
             id_order_production,
             id_product,
             product_name,
             id_warehouse,
             warehouse_name,
             quantity,
             price_base,
             total_unit,
             line_total
                )
AS
SELECT poc.id_production_order_components,
       poc.id_order_production,
       poc.id_product,
       p.name                        AS product_name,
       poc.id_warehouse,
       w.name                        AS warehouse_name,
       poc.quantity,
       poc.price_base,
       poc.quantity * poc.price_base AS total_unit,
       poc.line_total
FROM production_order_components poc
         INNER JOIN
     products p USING (id_product)
         INNER JOIN
     warehouses w USING (id_warehouse);

-- ====================== MÓDULO VENDAS ======================

--Criar um Cliente
CREATE OR REPLACE PROCEDURE PA_Create_Client(
    IN _name TEXT,
    IN _email TEXT,
    IN _nif TEXT,
    IN _phone TEXT,
    IN _address TEXT,
    IN _locality TEXT,
    IN _postal_code TEXT
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO clients (name, email, nif, phone, address, locality, postal_code)
    VALUES (_name, _email, _nif, _phone, _address, _locality, _postal_code);
END;
$$;


--Atualizar Cliente
CREATE OR REPLACE PROCEDURE PA_Update_Client(
    IN _id_client INT,
    IN _name TEXT,
    IN _email TEXT,
    IN _nif TEXT,
    IN _phone TEXT,
    IN _address TEXT,
    IN _locality TEXT,
    IN _postal_code TEXT
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    UPDATE clients
    SET name        = _name,
        email       = _email,
        nif         = _nif,
        phone       = _phone,
        address     = _address,
        locality    = _locality,
        postal_code = _postal_code
    WHERE id_client = _id_client;
END;
$$;

--Listar Clientes
CREATE OR REPLACE VIEW V_Clients AS
SELECT id_client,
       name,
       email,
       nif,
       phone,
       address,
       locality,
       postal_code
FROM clients;

--FN_Create_SalesOrder(id_client_order[],obs<O>) : id_sales_order Criar cabeçalho Pedido de venda, devolve id do pedido de venda
CREATE OR REPLACE FUNCTION FN_Create_SalesOrder(
    IN _id_user INT,
    IN _id_client_order INT[],
    IN _obs TEXT DEFAULT NULL
)
    RETURNS INT
    LANGUAGE plpgsql
AS
$$
DECLARE
    _id_sale_order INT;
BEGIN
    INSERT INTO sales_orders (id_user, obs)
    VALUES (_id_user, _obs)
    RETURNING id_sale_order INTO _id_sale_order;

    UPDATE client_orders
    SET id_sale_order = _id_sale_order
    WHERE id_client_order = ANY (_id_client_order);

    RETURN _id_sale_order;
END;
$$;



--Insere componente no pedido de venda
CREATE OR REPLACE PROCEDURE PA_InsertLine_SalesOrder(
    IN _id_sale_order INT,
    IN _id_product INT,
    IN _quantity INT,
    IN _price_base MONEY,
    IN _vat INT,
    IN _discount REAL
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO sales_order_components (id_sale_order, id_product, quantity, price_base, vat, discount)
    VALUES (_id_sale_order, _id_product, _quantity, _price_base, _vat, _discount);
END;
$$;


-- Trigger sales_order_components TR_sales_order_components_PRE_INS Depois de inserir/atualizar/eliminar a linha de uma ordem de venda, temos de atualizar os valores totais da própria linha e depois atualizar os valores totais da ordem de venda e dar saída nos movimentos de stock (stock_movements)

DROP FUNCTION IF EXISTS TR_sales_order_components_PRE_INS() CASCADE;
CREATE OR REPLACE FUNCTION TR_sales_order_components_PRE_INS() RETURNS TRIGGER AS
$$
DECLARE
    _vat_value      MONEY;
    _discount_value MONEY;
    _line_total     MONEY;
    _total_base     MONEY;
    _vat_total      MONEY;
    _discount_total MONEY;
    _total          MONEY;
BEGIN
    _vat_value := NEW.price_base * (NEW.vat / 100.0) * NEW.quantity;
    _discount_value := NEW.price_base * (NEW.discount / 100.0) * NEW.quantity;
    _line_total := (NEW.price_base * NEW.quantity) + _vat_value - _discount_value;


    NEW.vat_value := _vat_value;
    NEW.discount_value := _discount_value;
    NEW.line_total := _line_total;

    _total_base := (SELECT COALESCE(SUM(price_base * quantity), 0::MONEY)
                    FROM sales_order_components
                    WHERE id_sale_order = NEW.id_sale_order) + NEW.price_base * NEW.quantity;

    _vat_total := (SELECT COALESCE(SUM(vat_value), 0::MONEY)
                   FROM sales_order_components
                   WHERE id_sale_order = NEW.id_sale_order) + _vat_value;

    _discount_total := (SELECT COALESCE(SUM(discount_value), 0::MONEY)
                        FROM sales_order_components
                        WHERE id_sale_order = NEW.id_sale_order) + _discount_value;

    _total := _total_base + _vat_total - _discount_total;

    UPDATE sales_orders
    SET total_base     = _total_base,
        vat_total      = _vat_total,
        discount_total = _discount_total,
        total          = _total
    WHERE id_sale_order = NEW.id_sale_order;


    IF
            (SELECT COUNT(*)
             FROM sales_order_components
             WHERE id_sale_order = NEW.id_sale_order
               AND id_product = NEW.id_product)
            > 0
    THEN

        UPDATE sales_order_components
        SET quantity       = quantity + NEW.quantity,
            vat_value      = _vat_total,
            discount_value = _discount_total,
            line_total     = (quantity + NEW.quantity) * price_base
        WHERE id_sale_order = NEW.id_sale_order
          AND id_product = NEW.id_product;

        PERFORM FN_RemoveProductFromStock(0, NEW.id_product, NEW.quantity, 'OUT', 'sales_order', NEW.id_sale_order);

        RETURN NULL;

    END IF;

    RETURN NEW;

END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER TR_sales_order_components_PRE_INS
    BEFORE INSERT
    ON sales_order_components
    FOR EACH ROW
EXECUTE FUNCTION TR_sales_order_components_PRE_INS();


--Lista as ordens de venda (cabeçalho)
DROP VIEW IF EXISTS V_SalesOrders CASCADE;
CREATE OR REPLACE VIEW V_SalesOrders
            (
             id_sale_order,
             id_user,
             user_name,
             client_orders,
             client_names,
             created_at,
             obs,
             total_base
                )
AS
SELECT so.id_sale_order,
       so.id_user,
       u.username                    AS user_name,
       ARRAY_AGG(co.id_client_order) AS client_orders,
       ARRAY_AGG(c.name)             AS client_names,
       so.created_at,
       so.obs,
       so.total_base
FROM sales_orders so
         INNER JOIN auth_user u ON so.id_user = u.id
         INNER JOIN client_orders co ON so.id_sale_order = co.id_sale_order
         INNER JOIN clients c ON co.id_client = c.id_client
GROUP BY so.id_sale_order, so.id_user, u.username, so.created_at, so.obs, so.total_base;


--Lista as linhas das ordens de venda
DROP VIEW IF EXISTS V_SalesOrderComponents CASCADE;
CREATE OR REPLACE VIEW V_SalesOrderComponents
            (
             id_sales_order_component,
             id_sale_order,
             id_product,
             product_name,
             quantity,
             price_base,
             total_unit,
             vat,
             vat_value,
             discount,
             discount_value,
             line_total
                )
AS
SELECT soc.id_sales_order_component,
       soc.id_sale_order,
       soc.id_product,
       p.name                        AS product_name,
       soc.quantity,
       soc.price_base,
       soc.quantity * soc.price_base AS total_unit,
       soc.vat,
       soc.vat_value,
       soc.discount,
       soc.discount_value,
       soc.line_total
FROM sales_order_components soc
         INNER JOIN products p USING (id_product);



--FN_Create_ClientOrders(id_client,obs<O>) : id_client_order Criar cabeçalho da encomenda do cliente, devolve id da encomenda do cliente

CREATE OR REPLACE FUNCTION FN_Create_ClientOrders(
    IN _id_client INT,
    IN _obs TEXT DEFAULT NULL
)
    RETURNS INT
    LANGUAGE plpgsql
AS
$$
DECLARE
    _id_client_order INT;
BEGIN
    -- Inserir cabeçalho da encomenda do cliente
    INSERT INTO client_orders (id_client, obs)
    VALUES (_id_client, _obs)
    RETURNING id_client_order INTO _id_client_order;

    RETURN _id_client_order;
END;
$$;


--Insere componente na encomenda dos clientes
CREATE OR REPLACE PROCEDURE PA_InsertLine_ClientOrders(
    IN _id_client_order INT,
    IN _id_product INT,
    IN _quantity INT,
    IN _price_base MONEY,
    IN _vat INTEGER,
    IN _discount REAL
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO client_order_components (id_client_order, id_product, quantity, price_base, vat, discount)
    VALUES (_id_client_order, _id_product, _quantity, _price_base, _vat, _discount);
END;
$$;

-- Trigger client_order_components TR_client_order_components_PRE_INS Depois de inserir/atualizar/eliminar a linha de uma encomenda de cliente, temos de atualizar os valores totais da própria linha e depois atualizar os valores totais da encomenda de cliente
DROP FUNCTION IF EXISTS TR_client_order_components_PRE_INS() CASCADE;
CREATE OR REPLACE FUNCTION TR_client_order_components_PRE_INS() RETURNS TRIGGER AS
$$
DECLARE
    _vat_value      MONEY;
    _discount_value MONEY;
    _line_total     MONEY;
    _total_base     MONEY;
    _vat_total      MONEY;
    _discount_total MONEY;
    _total          MONEY;
BEGIN
    _vat_value := NEW.price_base * (NEW.vat / 100.0) * NEW.quantity;
    _discount_value := NEW.price_base * (NEW.discount / 100.0) * NEW.quantity;
    _line_total := (NEW.price_base * NEW.quantity) + _vat_value - _discount_value;


    NEW.vat_value := _vat_value;
    NEW.discount_value := _discount_value;
    NEW.line_total := _line_total;

    _total_base := (SELECT COALESCE(SUM(price_base * quantity), 0::MONEY)
                    FROM client_order_components
                    WHERE id_client_order = NEW.id_client_order) + NEW.price_base * NEW.quantity;

    _vat_total := (SELECT COALESCE(SUM(vat_value), 0::MONEY)
                   FROM client_order_components
                   WHERE id_client_order = NEW.id_client_order) + _vat_value;

    _discount_total := (SELECT COALESCE(SUM(discount_value), 0::MONEY)
                        FROM client_order_components
                        WHERE id_client_order = NEW.id_client_order) + _discount_value;

    _total := _total_base + _vat_total - _discount_total;

    UPDATE client_orders
    SET total_base     = _total_base,
        vat_total      = _vat_total,
        discount_total = _discount_total,
        total          = _total
    WHERE id_client_order = NEW.id_client_order;

    IF
            (SELECT COUNT(*)
             FROM client_order_components
             WHERE id_client_order = NEW.id_client_order
               AND id_product = NEW.id_product)
            > 0
    THEN

        UPDATE client_order_components
        SET quantity       = quantity + NEW.quantity,
            vat_value      = _vat_total,
            discount_value = _discount_total,
            line_total     = (quantity + NEW.quantity) * price_base
        WHERE id_client_order = NEW.id_client_order
          AND id_product = NEW.id_product;

        RETURN NULL;

    END IF;

    RETURN NEW;

END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER TR_client_order_components_PRE_INS
    BEFORE INSERT
    ON client_order_components
    FOR EACH ROW
EXECUTE FUNCTION TR_client_order_components_PRE_INS();


--Lista as encomendas do cliente (cabeçalho)
DROP VIEW IF EXISTS V_ClientOrders CASCADE;
CREATE OR REPLACE VIEW V_ClientOrders
            (
             id_client_order,
             id_client,
             client_name,
             obs,
             total_base,
             created_at
                )
AS
SELECT co.id_client_order,
       co.id_client,
       c.name AS client_name,
       co.obs,
       co.total_base,
       co.created_at
FROM client_orders co
         INNER JOIN clients c USING (id_client);

--Lista as linhas das encomendas do clientes
DROP VIEW IF EXISTS V_ClientOrdersComponents CASCADE;
CREATE OR REPLACE VIEW V_ClientOrdersComponents
            (
             id_client_order_components,
             id_client_order,
             id_product,
             product_name,
             quantity,
             price_base,
             total_unit,
             vat,
             vat_value,
             discount,
             discount_value,
             line_total
                )
AS
SELECT coc.id_client_order_components,
       coc.id_client_order,
       coc.id_product,
       p.name                        AS product_name,
       coc.quantity,
       coc.price_base,
       coc.quantity * coc.price_base AS total_unit,
       coc.vat,
       coc.vat_value,
       coc.discount,
       coc.discount_value,
       coc.line_total
FROM client_order_components coc
         INNER JOIN products p USING (id_product);


--FN_Create_ClientInvoice(id_sale_order[], id_client,invoice_id,invoice_date,expire_date,obs):id_client_invoice Criar cabeçalho da fatura, juntamente envia os ids das encomendas dos clientes para lhes dar update com o novo id da fatura criada

CREATE OR REPLACE FUNCTION FN_Create_ClientInvoice(
    IN _id_sale_orders INT[],
    IN _id_client INT,
    IN _expire_date TIMESTAMPTZ,
    IN _invoice_date TIMESTAMPTZ,
    IN _obs TEXT DEFAULT NULL
)
    RETURNS INT
    LANGUAGE plpgsql
AS
$$
DECLARE
    _id_client_invoice INT;
BEGIN
    INSERT INTO client_invoices (id_client, obs, invoice_date, expire_date)
    VALUES (_id_client, _obs, _invoice_date, _expire_date)
    RETURNING id_client_invoice INTO _id_client_invoice;

    UPDATE sales_orders
    SET id_client_invoice = _id_client_invoice
    WHERE id_sale_order = ANY (_id_sale_orders);

    RETURN _id_client_invoice;
END;
$$;



--Insere componente na fatura
CREATE OR REPLACE PROCEDURE PA_InsertLine_ClientInvoice(
    IN _id_client_invoice INT,
    IN _id_product INT,
    IN _quantity INT,
    IN _price_base MONEY,
    IN _vat INT,
    IN _discount REAL
)
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO client_invoice_components (id_client_invoice, id_product, quantity, price_base, vat, discount)
    VALUES (_id_client_invoice, _id_product, _quantity, _price_base, _vat, _discount);
END;
$$;

-- Trigger client_invoice_components TR_client_invoice_components_PRE_INS Depois de inserir/atualizar/eliminar a linha de uma fatura de cliente, temos de atualizar os valores totais da própria linha e depois atualizar os valores totais da fatura de cliente
DROP FUNCTION IF EXISTS TR_client_invoice_components_PRE_INS() CASCADE;
CREATE OR REPLACE FUNCTION TR_client_invoice_components_PRE_INS() RETURNS TRIGGER AS
$$
DECLARE
    _vat_value      MONEY;
    _discount_value MONEY;
    _line_total     MONEY;
    _total_base     MONEY;
    _vat_total      MONEY;
    _discount_total MONEY;
    _total          MONEY;
BEGIN
    _vat_value := NEW.price_base * (NEW.vat / 100.0) * NEW.quantity;
    _discount_value := NEW.price_base * (NEW.discount / 100.0) * NEW.quantity;
    _line_total := (NEW.price_base * NEW.quantity) + _vat_value - _discount_value;


    NEW.vat_value := _vat_value;
    NEW.discount_value := _discount_value;
    NEW.line_total := _line_total;

    _total_base := (SELECT COALESCE(SUM(price_base * quantity), 0::MONEY)
                    FROM client_invoice_components
                    WHERE id_client_invoice = NEW.id_client_invoice) + NEW.price_base * NEW.quantity;

    _vat_total := (SELECT COALESCE(SUM(vat_value), 0::MONEY)
                   FROM client_invoice_components
                   WHERE id_client_invoice = NEW.id_client_invoice) + _vat_value;

    _discount_total := (SELECT COALESCE(SUM(discount_value), 0::MONEY)
                        FROM client_invoice_components
                        WHERE id_client_invoice = NEW.id_client_invoice) + _discount_value;

    _total := _total_base + _vat_total - _discount_total;

    UPDATE client_invoices
    SET total_base     = _total_base,
        vat_total      = _vat_total,
        discount_total = _discount_total,
        total          = _total
    WHERE id_client_invoice = NEW.id_client_invoice;

    IF
            (SELECT COUNT(*)
             FROM client_invoice_components
             WHERE id_client_invoice = NEW.id_client_invoice
               AND id_product = NEW.id_product)
            > 0
    THEN

        UPDATE client_invoice_components
        SET quantity       = quantity + NEW.quantity,
            vat_value      = _vat_total,
            discount_value = _discount_total,
            line_total     = (quantity + NEW.quantity) * price_base
        WHERE id_client_invoice = NEW.id_client_invoice
          AND id_product = NEW.id_product;

        RETURN NULL;

    END IF;

    RETURN NEW;

END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER TR_client_invoice_components_PRE_INS
    BEFORE INSERT
    ON client_invoice_components
    FOR EACH ROW
EXECUTE FUNCTION TR_client_invoice_components_PRE_INS();

--Lista todas as faturas do cliente
DROP VIEW IF EXISTS V_ClientInvoices CASCADE;
CREATE OR REPLACE VIEW V_ClientInvoices
            (
             id_client_invoice,
             id_client,
             client_name,
             client_address,
             client_locality,
             client_postal_code,
             client_nif,
             sales_orders,
             invoice_date,
             expire_date,
             obs,
             total_base,
             vat_total,
             discount_total,
             total,
             created_at
                )
AS
SELECT ci.id_client_invoice,
       ci.id_client,
       c.name                      AS client_name,
       c.address                   AS client_address,
       c.locality                  AS client_locality,
       c.postal_code               AS client_postal_code,
       c.nif                       AS client_nif,
       ARRAY_AGG(so.id_sale_order) AS sales_orders,

       ci.invoice_date,
       ci.expire_date,
       ci.obs,
       ci.total_base,
       ci.vat_total,
       ci.discount_total,
       ci.total,
       ci.created_at
FROM client_invoices ci
         INNER JOIN clients c USING (id_client)
         INNER JOIN sales_orders so ON ci.id_client_invoice = so.id_client_invoice
GROUP BY ci.id_client_invoice, ci.id_client, c.name, c.address, c.locality, c.postal_code, c.nif,
         ci.invoice_date, ci.expire_date, ci.obs;


--Lista as linhas das faturas
DROP VIEW IF EXISTS V_ClientInvoicesComponents CASCADE;
CREATE OR REPLACE VIEW V_ClientInvoicesComponents
            (
             id_client_invoice_component,
             id_client_invoice,
             id_product,
             product_name,
             quantity,
             price_base,
             total_unit,
             vat,
             vat_value,
             discount,
             discount_value,
             line_total
                )
AS
SELECT cic.id_client_invoice_component,
       cic.id_client_invoice,
       cic.id_product,
       p.name                        AS product_name,
       cic.quantity,
       cic.price_base,
       cic.quantity * cic.price_base AS total_unit,
       cic.vat,
       cic.vat_value,
       cic.discount,
       cic.discount_value,
       cic.line_total
FROM client_invoice_components cic
         INNER JOIN products p USING (id_product);

