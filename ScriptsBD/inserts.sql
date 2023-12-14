/*
    @author: Duarte Santos
    @brief: Este ficheiro serve para colocar dados de teste para os triggers e para os procedimentos armazenados
*/


-- ================ DADOS PARA TESTAR TRIGGER  TR_purchasing_order_components_PRE_INS ==================
/*Inserir Produtos*/
INSERT INTO products (name, description, weight,type,price_cost,profit_margin,vat) 
VALUES ('Intel Core i7-8700K', 'Intel Core i7-8700K 3.7GHz 12MB Skt1151', 120, 'COMPONENT', 350, 30, 23);

INSERT INTO products (name, description, weight,type,price_cost,profit_margin,vat)
VALUES ('Intel Core i5-8600K', 'Intel Core i5-8600K 3.6GHz 9MB Skt1151', 120, 'COMPONENT', 250, 30, 23);


/*Inserir Fornecedores*/
INSERT INTO suppliers (name, email, nif, phone, address, locality, postal_code)
VALUES ('PcDiga', 'pcdiga@pcdiga.com', '123456789', '123456789', 'Rua do PC', 'Porto', '4000-000');

INSERT INTO suppliers (name, email, nif, phone, address, locality, postal_code)
VALUES ('PCComponents', 'pccomponents@pcdiga.com', '123456789', '123456789', 'Rua do PCcomponents', 'Madrid', '4000-200');

/*Criar Purchasing Order*/
INSERT INTO purchasing_orders (id_supplier, id_user, delivery_date)
VALUES (1, 1, '2023-02-12');

/*Inserir Linha na Purchasing Order Components*/
INSERT INTO purchasing_order_components (id_purchasing_order, id_product, quantity, price_base, vat, discount)
VALUES (1, 1, 2, 350, 23, 0);

INSERT INTO purchasing_order_components (id_purchasing_order, id_product, quantity, price_base, vat, discount)
VALUES (1, 2, 10, 350, 23, 10);

/*Criar Warehouses*/

CALL PA_Create_Warehouse('Armazem A','Porto');
CALL PA_Create_Warehouse('Armazem B','Lisboa');
CALL PA_Create_Warehouse('Armazem C','Faro');

/*criar receção de material*/
CALL FN_Create_MaterialReceipts(1,1,'1');

/*criar components de receção de material*/
-- PA_InsertLine_MaterialReceipt(_id_material_receipt INT,_id_product INT,_id_warehouse INT,_quantity INT,_price_base MONEY,_vat INT,_discount REAL DEFAULT 0)
CALL PA_InsertLine_MaterialReceipt(1,1,1,20,350,23,0);

/*criar fatura do fornecedor*/

SELECT FN_Create_SupplierInvoice(
    ARRAY[1], -- Seus IDs de material_receipt
    3, -- ID do fornecedor
    4, -- ID da fatura
    '2023-12-01'::DATE, -- Data da fatura
    '2024-01-01'::DATE, -- Data de expiração
    'Observações sobre a fatura' -- Observações
);

/*criar mão de obra*/
INSERT INTO labors (title, cost)
VALUES
    ('Montagem de Computador', 80.00),
    ('Instalação de Componentes', 50.00),
    ('Serviço de Manutenção', 65.00);


-- ================================================================================================