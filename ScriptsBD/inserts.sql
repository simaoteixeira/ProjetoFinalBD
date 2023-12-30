-- =================================== DADOS PARA BASE DE DADOS ===================================

-- Inserir Produtos
SELECT *
FROM fn_create_product(
        'Intel Core i7-8700K',
        'Intel Core i7-8700K 3.7GHz 12MB Skt1151',
        'COMPONENT',
        150,
        23,
        20);
SELECT *
FROM fn_create_product(
        'Intel Core i5-8600K',
        'Intel Core i5-8600K 3.6GHz 9MB Skt1151',
        'COMPONENT',
        100,
        23,
        20);
SELECT *
FROM fn_create_product(
        'NVIDIA GeForce GTX 1080 Ti',
        'NVIDIA GeForce GTX 1080 Ti 11GB GDDR5X',
        'COMPONENT',
        300,
        23,
        20);

SELECT *
FROM fn_create_product(
        'NVIDIA GeForce RTX 3070 Ti',
        'NVIDIA GeForce RTX 3070 Ti 8GB GDDR6X',
        'COMPONENT',
        400,
        23,
        20);

SELECT *
FROM fn_create_product(
        'Memory DDR4 16GB',
        'Memory DDR4 16GB 3200MHz',
        'COMPONENT',
        100,
        23,
        20);

SELECT *
FROM fn_create_product(
        'Memory DDR4 32GB',
        'Memory DDR4 32GB 3200MHz',
        'COMPONENT',
        200,
        23,
        20);

SELECT *
FROM fn_create_product(
        'SSD 1TB',
        'SSD 1TB 2.5" SATA3',
        'COMPONENT',
        100,
        23,
        20);

SELECT *
FROM fn_create_product(
        'SSD 2TB',
        'SSD 2TB 2.5" SATA3',
        'COMPONENT',
        200,
        23,
        20);

SELECT *
FROM fn_create_product(
        'Motherboard ASUS ROG STRIX',
        'Motherboard ASUS ROG STRIX Z390-E GAMING',
        'COMPONENT',
        400,
        23,
        20);

SELECT *
FROM fn_create_product(
        'Motherboard MSI MPG',
        'Motherboard MSI MPG Z390 GAMING EDGE AC',
        'COMPONENT',
        500,
        23,
        20);

SELECT *
FROM fn_create_product(
        'Power Supply 750W',
        'Power Supply 750W 80 Plus Gold',
        'COMPONENT',
        100,
        23,
        20);

SELECT *
FROM fn_create_product(
        'Power Supply 850W',
        'Power Supply 850W 80 Plus Gold',
        'COMPONENT',
        200,
        23,
        20);

SELECT *
FROM fn_create_product(
        'Case',
        'Case ATX',
        'COMPONENT',
        100,
        23,
        20);

SELECT *
FROM fn_create_product(
        'Case',
        'Case ATX',
        'COMPONENT',
        100,
        23,
        20);

SELECT *
FROM fn_create_product(
        'Cooler Master MasterBox',
        'Cooler Master MasterBox MB511 RGB',
        'COMPONENT',
        300,
        23,
        20);

SELECT *
FROM fn_create_product(
        'Cooler Noctua NH-D15',
        'Cooler Noctua NH-D15',
        'COMPONENT',
        300,
        23,
        20);

SELECT *
FROM fn_create_product(
        'VortexEdge Gaming Builds',
        'VortexEdge Gaming Builds',
        'EQUIPMENT',
        7000,
        23,
        20);

SELECT *
FROM fn_create_product(
        'TitanForge Gaming Series',
        'TitanForge Gaming Series',
        'EQUIPMENT',
        5000,
        23,
        20);

/*Criar Warehouses*/

CALL PA_Create_Warehouse(
    'Armazem A',
    'Porto');
CALL PA_Create_Warehouse(
    'Armazem B',
    'Lisboa');
CALL PA_Create_Warehouse(
    'Armazem C',
    'Viseu');
CALL PA_Create_Warehouse(
    'Armazem D',
    'Braga');
CALL PA_Create_Warehouse(
    'Armazem E',
    'Coimbra');

/*criar mão de obra*/

CALL  PA_Create_Labor(
    'Montagem de Computador',
    '80');
CALL  PA_Create_Labor(
    'Instalação de Componentes',
    '50');
CALL  PA_Create_Labor(
    'Serviço de Manutenção',
    '65');
CALL  PA_Create_Labor(
    'Serviço de Limpeza',
    '30');
CALL  PA_Create_Labor(
    'Serviço de Reparação',
    '50');

/*Inserir Fornecedores*/

CALL PA_Create_Supplier(
    'PcDiga',
    'pcdiga@pcdiga.com',
    '123456789',
    '9623565172',
    'Rua do PC',
    'Porto',
    '4000-000');

CALL PA_Create_Supplier(
    'PCComponents',
    'pccomponents@pcdiga.com',
    '478942893',
    '965354713',
    'Rua do PCcomponents',
    'Madrid',
    '4000-200');

CALL PA_Create_Supplier(
    'TechData',
    'techdata@techdata.com',
    '904792835',
    '976512311',
    'Rua do TechData',
    'Lisboa',
    '4000-300');

CALL PA_Create_Supplier(
    'Inforlandia',
    'inforlandia@inforlandia.com',
    '827389163',
    '912763245',
    'Rua do Inforlandia',
    'Viseu',
    '4000-400');

CALL PA_Create_Supplier(
    'Globaldata',
    'globaldata@globaldata.com',
    '123456789',
    '941237981',
    'Rua do Globaldata',
    'Braga',
    '4000-500');





