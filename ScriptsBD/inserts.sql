-- =================================== DADOS PARA BASE DE DADOS ===================================

-- Declarar variáveis
DO
$$
    DECLARE
        id_admin    int = 1;
        id_compras  int = 2;
        id_vendas   int = 3;
        id_stock    int = 4;
        id_producao int = 5;
    BEGIN

        --=================================== STOCK ===================================
        -- Inserir Produtos
        PERFORM fn_create_product(
                'Intel Core i7-8700K',
                'Intel Core i7-8700K 3.7GHz 12MB Skt1151',
                'COMPONENT',
                150,
                23,
                20);

        PERFORM fn_create_product(
                'Intel Core i5-8600K',
                'Intel Core i5-8600K 3.6GHz 9MB Skt1151',
                'COMPONENT',
                100,
                23,
                20);

        PERFORM fn_create_product(
                'NVIDIA GeForce GTX 1080 Ti',
                'NVIDIA GeForce GTX 1080 Ti 11GB GDDR5X',
                'COMPONENT',
                300,
                23,
                20);

        PERFORM fn_create_product(
                'NVIDIA GeForce RTX 3070 Ti',
                'NVIDIA GeForce RTX 3070 Ti 8GB GDDR6X',
                'COMPONENT',
                400,
                23,
                20);

        PERFORM fn_create_product(
                'Memory DDR4 16GB',
                'Memory DDR4 16GB 3200MHz',
                'COMPONENT',
                100,
                23,
                20);

        PERFORM fn_create_product(
                'Memory DDR4 32GB',
                'Memory DDR4 32GB 3200MHz',
                'COMPONENT',
                200,
                23,
                20);

        PERFORM fn_create_product(
                'SSD 1TB',
                'SSD 1TB 2.5" SATA3',
                'COMPONENT',
                100,
                23,
                20);

        PERFORM fn_create_product(
                'SSD 2TB',
                'SSD 2TB 2.5" SATA3',
                'COMPONENT',
                200,
                23,
                20);

        PERFORM fn_create_product(
                'Motherboard ASUS ROG STRIX',
                'Motherboard ASUS ROG STRIX Z390-E GAMING',
                'COMPONENT',
                400,
                23,
                20);

        PERFORM fn_create_product(
                'Motherboard MSI MPG',
                'Motherboard MSI MPG Z390 GAMING EDGE AC',
                'COMPONENT',
                500,
                23,
                20);

        PERFORM fn_create_product(
                'Power Supply 750W',
                'Power Supply 750W 80 Plus Gold',
                'COMPONENT',
                100,
                23,
                20);

        PERFORM fn_create_product(
                'Power Supply 850W',
                'Power Supply 850W 80 Plus Gold',
                'COMPONENT',
                200,
                23,
                20);

        PERFORM fn_create_product(
                'Case',
                'Case ATX',
                'COMPONENT',
                100,
                23,
                20);

        PERFORM fn_create_product(
                'Case',
                'Case ATX',
                'COMPONENT',
                100,
                23,
                20);

        PERFORM fn_create_product(
                'Cooler Master MasterBox',
                'Cooler Master MasterBox MB511 RGB',
                'COMPONENT',
                300,
                23,
                20);

        PERFORM fn_create_product(
                'Cooler Noctua NH-D15',
                'Cooler Noctua NH-D15',
                'COMPONENT',
                300,
                23,
                20);

        PERFORM fn_create_product(
                'VortexEdge Gaming Builds',
                'VortexEdge Gaming Builds',
                'EQUIPMENT',
                7000,
                23,
                20);

        PERFORM fn_create_product(
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
        --=================================== FIM STOCK ===================================

        --=================================== COMPRAS ===================================

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

        /*Inserir ordem de compra*/

        PERFORM fn_create_purchasingorder(
                1,
                id_compras,
                '03-01-2024',
                'Encomenda das placas gráficas e motherboards'
                );

        PERFORM fn_create_purchasingorder(
                2,
                id_compras,
                '03-01-2024',
                'Encomenda das RAM e discos SSD'
                );

        PERFORM fn_create_purchasingorder(
                3,
                id_compras,
                '03-01-2024',
                'Encomenda das fontes de alimentação e caixas'
                );

        PERFORM fn_create_purchasingorder(
                4,
                id_compras,
                '03-01-2024',
                'Encomenda dos processadores'
                );

        PERFORM fn_create_purchasingorder(
                5,
                id_compras,
                '03-01-2024',
                'Encomenda dos coolers'
                );

        /*Inserir componentes de ordem de compra*/

        CALL pa_insertline_purchasingorder(
                1,
                3,
                10,
                300::money,
                23,
                0);

        CALL pa_insertline_purchasingorder(
                1,
                4,
                10,
                2000::money,
                23,
                40);

        CALL pa_insertline_purchasingorder(
                1,
                9,
                10,
                180::money,
                23,
                10);

        CALL pa_insertline_purchasingorder(
                1,
                10,
                10,
                200::money,
                23,
                20);

        CALL pa_insertline_purchasingorder(
                2,
                5,
                15,
                70::money,
                23,
                0);

        CALL pa_insertline_purchasingorder(
                2,
                6,
                15,
                110::money,
                23,
                10);

        CALL pa_insertline_purchasingorder(
                2,
                7,
                20,
                100::money,
                23,
                0);

        CALL pa_insertline_purchasingorder(
                2,
                8,
                20,
                170::money,
                23,
                10);

        CALL pa_insertline_purchasingorder(
                3,
                11,
                7,
                170::money,
                23,
                0);

        CALL pa_insertline_purchasingorder(
                3,
                12,
                7,
                230::money,
                23,
                50);

        CALL pa_insertline_purchasingorder(
                3,
                13,
                8,
                100::money,
                23,
                0);

        CALL pa_insertline_purchasingorder(
                3,
                14,
                8,
                130::money,
                23,
                10);

        CALL pa_insertline_purchasingorder(
                4,
                1,
                10,
                300::money,
                23,
                15);

        CALL pa_insertline_purchasingorder(
                4,
                2,
                10,
                200::money,
                23,
                0);

        CALL pa_insertline_purchasingorder(
                5,
                15,
                10,
                100::money,
                23,
                10);

        CALL pa_insertline_purchasingorder(
                5,
                16,
                10,
                120::money,
                23,
                20);

        /*Inserir receção de material*/

        PERFORM fn_create_materialreceipts(
                id_compras,
                1,
                'FXJQU',
                'Receção de material para a encomenda do pedido de compra de placas gráficas e motherboards, chegou metade de cada um'
                );

        PERFORM fn_create_materialreceipts(
                id_compras,
                1,
                'FXJQU',
                'Receção de material para a encomenda do pedido de compra de placas gráficas e motherboards, chegou o resto'
                );

        PERFORM fn_create_materialreceipts(
                id_compras,
                2,
                'FZPTA',
                'Receção de material para a encomenda do pedido de compra de RAM e discos SSD, chegou as RAM todas e metade dos discos SSD'
                );

        PERFORM fn_create_materialreceipts(
                id_compras,
                2,
                'FZPTA',
                'Receção de material para a encomenda do pedido de compra de RAM e discos SSD, chegou o resto dos discos SSD'
                );

        PERFORM fn_create_materialreceipts(
                id_compras,
                3,
                'FLQEWH',
                'Receção de material para a encomenda do pedido de compra de fontes de alimentação e caixas,chegou tudo'
                );

        PERFORM fn_create_materialreceipts(
                id_compras,
                4,
                'FZPTA',
                'Receção de material para a encomenda do pedido de compra de processadores, chegou um quarto'
                );

        PERFORM fn_create_materialreceipts(
                id_compras,
                4,
                'FZPTA',
                'Receção de material para a encomenda do pedido de compra de processadores, chegou outro quarto'
                );

        PERFORM fn_create_materialreceipts(
                id_compras,
                4,
                'FZPTA',
                'Receção de material para a encomenda do pedido de compra de processadores, chegou o resto'
                );

        PERFORM fn_create_materialreceipts(
                id_compras,
                5,
                'FPTJSD',
                'Receção de material para a encomenda do pedido de compra de coolers, chegou tudo'
                );

        /*Inserir componentes de receção de material*/

        CALL pa_insertline_materialreceipt(
                1,
                3,
                1,
                5,
                300::money,
                23);

        CALL pa_insertline_materialreceipt(
                1,
                4,
                2,
                5,
                2000::money,
                23);

        CALL pa_insertline_materialreceipt(
                1,
                9,
                1,
                5,
                180::money,
                23);

        CALL pa_insertline_materialreceipt(
                1,
                10,
                1,
                5,
                200::money,
                23);

        CALL pa_insertline_materialreceipt(
                2,
                3,
                1,
                5,
                300::money,
                23);

        CALL pa_insertline_materialreceipt(
                2,
                4,
                2,
                5,
                2000::money,
                23);

        CALL pa_insertline_materialreceipt(
                2,
                9,
                1,
                5,
                180::money,
                23);

        CALL pa_insertline_materialreceipt(
                2,
                10,
                1,
                5,
                200::money,
                23);

        CALL pa_insertline_materialreceipt(
                3,
                5,
                1,
                15,
                70::money,
                23);

        CALL pa_insertline_materialreceipt(
                3,
                6,
                2,
                15,
                110::money,
                23);

        CALL pa_insertline_materialreceipt(
                3,
                7,
                2,
                10,
                100::money,
                23);

        CALL pa_insertline_materialreceipt(
                3,
                8,
                3,
                10,
                170::money,
                23);

        CALL pa_insertline_materialreceipt(
                4,
                7,
                1,
                10,
                100::money,
                23);

        CALL pa_insertline_materialreceipt(
                4,
                8,
                3,
                10,
                170::money,
                23);

        CALL pa_insertline_materialreceipt(
                5,
                11,
                1,
                10,
                170::money,
                23);

        CALL pa_insertline_materialreceipt(
                5,
                12,
                1,
                10,
                230::money,
                23);

        CALL pa_insertline_materialreceipt(
                5,
                13,
                1,
                10,
                100::money,
                23);

        CALL pa_insertline_materialreceipt(
                5,
                14,
                1,
                10,
                130::money,
                23);

        CALL pa_insertline_materialreceipt(
                6,
                1,
                5,
                3,
                300::money,
                23);

        CALL pa_insertline_materialreceipt(
                6,
                2,
                4,
                2,
                200::money,
                23);

        CALL pa_insertline_materialreceipt(
                7,
                1,
                5,
                2,
                300::money,
                23);

        CALL pa_insertline_materialreceipt(
                7,
                2,
                4,
                3,
                200::money,
                23);

        CALL pa_insertline_materialreceipt(
                8,
                1,
                5,
                5,
                300::money,
                23);

        CALL pa_insertline_materialreceipt(
                8,
                2,
                4,
                5,
                200::money,
                23);

        CALL pa_insertline_materialreceipt(
                9,
                15,
                5,
                10,
                300::money,
                23);

        CALL pa_insertline_materialreceipt(
                9,
                16,
                3,
                10,
                200::money,
                23);

        /*Inserir faturas*/

        PERFORM fn_create_supplierinvoice(
                ARRAY [1,2],
                1,
                'F4812FV81',
                '2024-01-01',
                '2024-12-31',
                'Fatura para a encomenda do pedido de compra de placas gráficas e motherboards'
                );

        PERFORM fn_create_supplierinvoice(
                ARRAY [3,4],
                2,
            'F82187LK81',
                '2024-01-01',
                '2024-12-31',
                'Fatura para a encomenda do pedido de compra de RAM e discos SSD'
                );

        PERFORM fn_create_supplierinvoice(
                ARRAY [5],
                3,
                'F54647PQ81',
                '2024-01-01',
                '2024-12-31',
                'Fatura para a encomenda do pedido de compra de fontes de alimentação e caixas'
                );

        PERFORM fn_create_supplierinvoice(
                ARRAY [6,7,8],
                4,
                'F39486734HG1',
                '2024-01-01',
                '2024-12-31',
                'Fatura para a encomenda do pedido de compra de processadores'
                );

        PERFORM fn_create_supplierinvoice(
                ARRAY [9],
                5,
                'F39487ZK81',
                '2024-01-01',
                '2024-12-31',
                'Fatura para a encomenda do pedido de compra de coolers'
                );

        /*Inserir componentes de faturas*/

        CALL pa_insertline_supplierinvoice(
                1,
                3,
                10,
                300::money,
                23,
                0);

        CALL pa_insertline_supplierinvoice(
                1,
                4,
                10,
                2000::money,
                23,
                40);

        CALL pa_insertline_supplierinvoice(
                1,
                9,
                10,
                180::money,
                23,
                10);

        CALL pa_insertline_supplierinvoice(
                1,
                10,
                10,
                200::money,
                23,
                20);

        CALL pa_insertline_supplierinvoice(
                2,
                5,
                15,
                70::money,
                23,
                0);

        CALL pa_insertline_supplierinvoice(
                2,
                6,
                15,
                110::money,
                23,
                10);

        CALL pa_insertline_supplierinvoice(
                2,
                7,
                20,
                100::money,
                23,
                0);

        CALL pa_insertline_supplierinvoice(
                2,
                8,
                20,
                170::money,
                23,
                10);

        CALL pa_insertline_supplierinvoice(
                3,
                11,
                7,
                170::money,
                23,
                0);

        CALL pa_insertline_supplierinvoice(
                3,
                12,
                7,
                230::money,
                23,
                50);

        CALL pa_insertline_supplierinvoice(
                3,
                13,
                8,
                100::money,
                23,
                0);

        CALL pa_insertline_supplierinvoice(
                3,
                14,
                8,
                130::money,
                23,
                10);

        CALL pa_insertline_supplierinvoice(
                4,
                1,
                10,
                300::money,
                23,
                15);

        CALL pa_insertline_supplierinvoice(
                4,
                2,
                10,
                200::money,
                23,
                0);

        CALL pa_insertline_supplierinvoice(
                5,
                15,
                10,
                100::money,
                23,
                10);

        CALL pa_insertline_supplierinvoice(
                5,
                16,
                10,
                120::money,
                23,
                20);


-- ==================================== FIM COMPRAS ===================================

-- ==================================== PRODUÇÃO ======================================
        /*criar mão de obra*/

        CALL PA_Create_Labor(
                'Montagem de Computador',
                80::money);
        CALL PA_Create_Labor(
                'Instalação de Componentes',
                50::money);
        CALL PA_Create_Labor(
                'Serviço de Manutenção',
                65::money);
        CALL PA_Create_Labor(
                'Serviço de Limpeza',
                30::money);
        CALL PA_Create_Labor(
                'Serviço de Reparação',
                50::money);

        /*Inserir ordem de produção*/

        PERFORM fn_create_productionorder(
                1,
                id_producao,
                17,
                1,
                3,
                'Ordem de Produção para a encomenda do cliente Pedro: 1 equipamento'
                );

        PERFORM fn_create_productionorder(
                1,
                id_producao,
                18,
                1,
                1,
                'Ordem de Produção para a encomenda do cliente João: 1 equipamento'
                );

        PERFORM fn_create_productionorder(
                1,
                id_producao,
                17,
                1,
                1,
                'Ordem de Produção para a encomenda do cliente Duarte: 1 equipamentos, equipamentos  diferentes nos componentes'
                );

        PERFORM fn_create_productionorder(
                1,
                id_producao,
                17,
                1,
                1,
                'Ordem de Produção para a encomenda do cliente Duarte: 1 equipamentos, equipamentos por diferentes nos componentes'
                );

        /*Inserir componentes de ordem de produção*/

        CALL pa_insertline_productionorder(
                1,
                2,
                3,
                1
             );

        CALL pa_insertline_productionorder(
                1,
                3,
                1,
                1
             );

        CALL pa_insertline_productionorder(
                1,
                5,
                1,
                1
             );

        CALL pa_insertline_productionorder(
                1,
                7,
                2,
                1
             );

        CALL pa_insertline_productionorder(
                1,
                9,
                1,
                1
             );

        CALL pa_insertline_productionorder(
                1,
                11,
                4,
                1
             );

        CALL pa_insertline_productionorder(
                1,
                13,
                3,
                1
             );

        CALL pa_insertline_productionorder(
                1,
                15,
                5,
                1
             );

        CALL pa_insertline_productionorder(
                2,
                1,
                5,
                1
             );

        CALL pa_insertline_productionorder(
                2,
                2,
                4,
                1
             );

        CALL pa_insertline_productionorder(
                2,
                4,
                2,
                1
             );

        CALL pa_insertline_productionorder(
                2,
                6,
                2,
                1
             );

        CALL pa_insertline_productionorder(
                2,
                8,
                3,
                1
             );

        CALL pa_insertline_productionorder(
                2,
                10,
                5,
                1
             );

        CALL pa_insertline_productionorder(
                2,
                12,
                3,
                1
             );

        CALL pa_insertline_productionorder(
                2,
                14,
                4,
                1
             );
        /*caso do Duarte*/
        CALL pa_insertline_productionorder(
                4,
                2,
                3,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                3,
                1,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                5,
                1,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                7,
                1,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                9,
                4,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                11,
                4,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                13,
                3,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                15,
                5,
                1
             );

        /*caso do Duarte*/

        CALL pa_insertline_productionorder(
                4,
                2,
                3,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                3,
                1,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                5,
                1,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                7,
                1,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                9,
                1,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                11,
                4,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                13,
                3,
                1
             );

        CALL pa_insertline_productionorder(
                4,
                15,
                5,
                1
             );
        -- ==================================== FIM PRODUÇÃO ======================================

-- ==================================== VENDAS ============================================

        /*Inserir Clientes*/

        CALL PA_Create_Client(
                'João',
                'joao@gmail.com',
                '736467821',
                '916432789',
                'Rua do João',
                'Porto',
                '4000-000');

        CALL PA_Create_Client(
                'Pedro',
                'pedro@outlook.com',
                '423483489',
                '916432789',
                'Rua do Pedro',
                'Lisboa',
                '4000-200');

        CALL PA_Create_Client(
                'Duarte',
                'duarte@gmail.com',
                '873498234',
                '951289123',
                'Rua do Duarte',
                'Viseu',
                '4000-400');
        CALL PA_Create_Client(
                'Guilherme',
                'guilherme@yahoo.com',
                '723164789',
                '981367612',
                'Rua do Guilherme',
                'Braga',
                '4000-500');

        CALL PA_Create_Client(
                'Simão',
                'simao@icloud.pt',
                '334567456',
                '912345678',
                'Rua do irresponsável',
                'Coimbra',
                '4000-600');

        /*Inserir encomendas de Cliente*/

        PERFORM fn_create_clientorders(
                2,
                'Encomenda de 2 componentes e 1 equipamento'
                );

        PERFORM fn_create_clientorders(
                1,
                'Encomenda  1 equipamento'
                );

        PERFORM fn_create_clientorders(
                4,
                'Encomenda de 1 componentes'
                );

        PERFORM fn_create_clientorders(
                4,
                'Encomenda de 3 componentes'
                );

        PERFORM fn_create_clientorders(
                4,
                'Encomenda de 1 componentes e 1 equipamento'
                );

        PERFORM fn_create_clientorders(
                3,
                'Encomenda de 3 componentes e 2 equipamentos'
                );

        /*Inserir componentes de encomenda de cliente*/


        /*Encomenda realizada por Pedro 2 componentes e 1 equipamento*/

        CALL pa_insertline_clientorders(
                1,
                2,
                2,
                200::money,
                23,
                0);

        CALL pa_insertline_clientorders(
                1,
                3,
                1,
                300::money,
                23,
                0);

        CALL pa_insertline_clientorders(
                1,
                17,
                1,
                2000::money,
                23,
                10);

        /*Encomenda realizada por João 1 equipamento*/

        CALL pa_insertline_clientorders(
                2,
                18,
                1,
                3000::money,
                23,
                30);

        /*Encomenda realizada por Guilherme 1 componente*/

        CALL pa_insertline_clientorders(
                4,
                8,
                1,
                200::money,
                23,
                0);

        /*Encomenda realizada por Guilherme 3 componentes*/

        CALL pa_insertline_clientorders(
                5,
                13,
                3,
                100::money,
                23,
                0);

        /*Encomenda realizada por Duarte 3 componentes */

        CALL pa_insertline_clientorders(
                6,
                10,
                3,
                180::money,
                23,
                0);

        /*Encomenda realizada por Duarte 2 equipamentos*/

        CALL pa_insertline_clientorders(
                6,
                17,
                2,
                2000::money,
                23,
                30);

        /*Inserir guias de remessas*/

        PERFORM fn_create_salesorder(
                id_vendas,
                ARRAY [1],
                'Guia de Remessa  para a encomenda do cliente Pedro com 2 componentes e 1 equipamento'
                );

        PERFORM fn_create_salesorder(
                id_vendas,
                ARRAY [2],
                'Guia de Remessa  para a encomenda do cliente João com 1 equipamento'
                );

        PERFORM fn_create_salesorder(
                id_admin,
                ARRAY [3],
                'Guia de Remessa  para a encomenda do cliente Guilherme com 1 componente'
                );

        PERFORM fn_create_salesorder(
                id_admin,
                ARRAY [4],
                'Guia de Remessa  para a encomenda do cliente Guilherme com 3 componentes'
                );

        PERFORM fn_create_salesorder(
                id_vendas,
                ARRAY [5],
                'Guia de Remessa  para a encomenda do cliente Duarte com 2 componente e 1 equipamento'
                );

        PERFORM fn_create_salesorder(
                id_vendas,
                ARRAY [5],
                'Guia de Remessa  para a encomenda do cliente Duarte com resto:  1 componentes e 1 equipamentos'
                );

        /*Inserir componentes de guias de remessas*/

        CALL pa_insertline_salesorder(
                1,
                2,
                2,
                200::money,
                23,
                0);

        CALL pa_insertline_salesorder(
                1,
                3,
                1,
                300::money,
                23,
                0);

        CALL pa_insertline_salesorder(
                1,
                17,
                1,
                2000::money,
                23,
                10);

        CALL pa_insertline_salesorder(
                2,
                18,
                1,
                3000::money,
                23,
                30);

        CALL pa_insertline_salesorder(
                3,
                8,
                1,
                200::money,
                23,
                0);

        CALL pa_insertline_salesorder(
                4,
                13,
                3,
                100::money,
                23,
                0);

        CALL pa_insertline_salesorder(
                5,
                10,
                2,
                180::money,
                23,
                0);

        CALL pa_insertline_salesorder(
                5,
                17,
                1,
                2000::money,
                23,
                30);

        CALL pa_insertline_salesorder(
                6,
                10,
                1,
                180::money,
                23,
                0);

        CALL pa_insertline_salesorder(
                6,
                17,
                1,
                2000::money,
                23,
                30);

        /*Inserir faturas*/

        PERFORM fn_create_clientinvoice(
                ARRAY [1],
                2,
                '2024-06-01',
                '2023-12-31',
                'Fatura para a encomenda do cliente Pedro com 2 componentes e 1 equipamento'
                );

        PERFORM fn_create_clientinvoice(
                ARRAY [2],
                1,

                '2024-06-01',
                '2023-12-31',
                'Fatura para a encomenda do cliente João com 1 equipamento'
                );

        PERFORM fn_create_clientinvoice(
                ARRAY [3],
                4,

                '2024-06-01',
                '2023-12-31',
                'Fatura para a encomenda do cliente Guilherme com 1 componente'
                );

        PERFORM fn_create_clientinvoice(
                ARRAY [4],
                4,

                '2024-06-01',
                '2023-01-01',
                'Fatura para a encomenda do cliente Guilherme com 3 componentes'
                );

        PERFORM fn_create_clientinvoice(
                ARRAY [5,6],
                3,
                '2024-06-01',
                '2023-12-31',
                'Fatura para a encomenda do cliente Duarte com 3 componente e 2 equipamento'
                );

        /*Inserir componentes de faturas*/

        CALL pa_insertline_clientinvoice(
                1,
                2,
                2,
                200::money,
                23,
                0);

        CALL pa_insertline_clientinvoice(
                1,
                3,
                1,
                300::money,
                23,
                0);

        CALL pa_insertline_clientinvoice(
                1,
                17,
                1,
                2000::money,
                23,
                10);

        CALL pa_insertline_clientinvoice(
                2,
                18,
                1,
                3000::money,
                23,
                30);

        CALL pa_insertline_clientinvoice(
                3,
                8,
                1,
                200::money,
                23,
                0);

        CALL pa_insertline_clientinvoice(
                4,
                13,
                3,
                100::money,
                23,
                0);

        CALL pa_insertline_clientinvoice(
                5,
                10,
                3,
                180::money,
                23,
                0);

        CALL pa_insertline_clientinvoice(
                5,
                17,
                2,
                2000::money,
                23,
                30);





    END
$$;









