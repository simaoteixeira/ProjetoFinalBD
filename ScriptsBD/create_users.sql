/*
1. Create different users:
        - admin
        - compras
        - vendas
        - stock
        - producao
2. Add privileges to users:
        - admin has all privileges
        - compras has objects related to purchases
        - vendas has objects related to sales
        - stock has objects related to stock
        - producao has objects related to production
*/

DROP USER IF EXISTS compras;
CREATE USER compras WITH PASSWORD 'compras';
GRANT USAGE ON SCHEMA public TO compras;


DROP USER IF EXISTS vendas;
CREATE USER vendas WITH PASSWORD 'vendas';
GRANT USAGE ON SCHEMA public TO vendas;

DROP USER IF EXISTS stock;
CREATE USER stock WITH PASSWORD 'stock';
GRANT USAGE ON SCHEMA public TO stock;

DROP USER IF EXISTS producao;
CREATE USER producao WITH PASSWORD 'producao';
GRANT USAGE ON SCHEMA public TO producao;


-- Block 'compras' from accessing everything
-- Allow 'compras' to access:
/*
Procedures: PA_Create_Supplier, PA_Update_Supplier, PA_InsertLine_PurchasingOrder, PA_InsertLine_MaterialReceipt, FN_Create_MaterialReceipts, FN_Create_PurchasingOrder, FN_Create_SupplierInvoice, FN_GetProductAveragePriceByMaterialReceipts
Functions: FN_GetProductAveragePriceByMaterialReceipts, FN_Create_MaterialReceipts, FN_Create_PurchasingOrder, FN_Create_SupplierInvoice
Views: V_Suppliers, V_PurchasingOrders, V_PurchasingOrderComponents, V_MaterialReceipts, V_MaterialReceiptComponents, V_SupplierInvoices, V_SupplierInvoiceComponents
*/
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM compras;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO compras;

GRANT EXECUTE ON PROCEDURE PA_Create_Supplier TO compras;
GRANT EXECUTE ON PROCEDURE PA_Update_Supplier TO compras;
GRANT EXECUTE ON PROCEDURE PA_InsertLine_PurchasingOrder TO compras;
GRANT EXECUTE ON PROCEDURE PA_InsertLine_MaterialReceipt TO compras;

GRANT EXECUTE ON FUNCTION FN_Create_MaterialReceipts TO compras;
GRANT EXECUTE ON FUNCTION FN_Create_PurchasingOrder TO compras;
GRANT EXECUTE ON FUNCTION FN_Create_SupplierInvoice TO compras;
GRANT EXECUTE ON FUNCTION FN_GetProductAveragePriceByMaterialReceipts TO compras;

GRANT SELECT ON V_Suppliers TO compras;
GRANT SELECT ON V_PurchasingOrders TO compras;
GRANT SELECT ON V_PurchasingOrderComponents TO compras;
GRANT SELECT ON V_MaterialReceipts TO compras;
GRANT SELECT ON V_MaterialReceiptComponents TO compras;
GRANT SELECT ON V_SupplierInvoices TO compras;
GRANT SELECT ON V_SupplierInvoiceComponents TO compras;

GRANT SELECT, INSERT, UPDATE ON TABLE suppliers TO compras;
GRANT SELECT, INSERT, UPDATE ON TABLE purchasing_orders TO compras;
GRANT SELECT, INSERT, UPDATE ON TABLE purchasing_order_components TO compras;
GRANT SELECT, INSERT, UPDATE ON TABLE material_receipts TO compras;
GRANT SELECT, INSERT, UPDATE ON TABLE material_receipt_components TO compras;
GRANT SELECT, INSERT, UPDATE ON TABLE products TO compras;
GRANT SELECT, INSERT, UPDATE ON TABLE warehouses TO compras;
GRANT SELECT, INSERT, UPDATE ON TABLE supplier_invoices TO compras;
GRANT SELECT, INSERT, UPDATE ON TABLE supplier_invoice_components TO compras;

-- Block 'vendas' from accessing everything
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM vendas;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO vendas;

-- Allow 'vendas' to access:
GRANT EXECUTE ON PROCEDURE PA_Create_Client TO vendas;
GRANT EXECUTE ON PROCEDURE PA_Update_Client TO vendas;
GRANT EXECUTE ON PROCEDURE PA_InsertLine_SalesOrder TO vendas;
GRANT EXECUTE ON PROCEDURE PA_InsertLine_ClientOrders TO vendas;
GRANT EXECUTE ON PROCEDURE PA_InsertLine_ClientInvoice TO vendas;

-- Grant execute on functions to vendas
GRANT EXECUTE ON FUNCTION FN_Create_SalesOrder TO vendas;
GRANT EXECUTE ON FUNCTION FN_Create_ClientOrders TO vendas;
GRANT EXECUTE ON FUNCTION FN_Create_ClientInvoice TO vendas;

-- Grant select on views to vendas
GRANT SELECT ON V_Clients TO vendas;
GRANT SELECT ON V_SalesOrders TO vendas;
GRANT SELECT ON V_SalesOrderComponents TO vendas;
GRANT SELECT ON V_ClientOrders TO vendas;
GRANT SELECT ON V_ClientOrdersComponents TO vendas;
GRANT SELECT ON V_ClientInvoices TO vendas;
GRANT SELECT ON V_ClientInvoicesComponents TO vendas;

-- Block 'stock' from accessing everything
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM stock;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO stock;

-- Allow 'stock' to access:
GRANT EXECUTE ON PROCEDURE PA_Create_Warehouse TO stock;
GRANT EXECUTE ON PROCEDURE PA_Update_Warehouse TO stock;
GRANT EXECUTE ON PROCEDURE PA_InsertLine_SupplierInvoice TO stock;
GRANT EXECUTE ON PROCEDURE PA_Update_Product TO stock;

-- Grant execute on functions to stock
GRANT EXECUTE ON FUNCTION FN_AddProductToStock TO stock;
GRANT EXECUTE ON FUNCTION FN_RemoveProductFromStock TO stock;
GRANT EXECUTE ON FUNCTION FN_Create_Product TO stock;
GRANT EXECUTE ON FUNCTION FN_ExistsStock TO stock;

-- Grant select on views to stock
GRANT SELECT ON TABLE V_Warehouses TO stock;
GRANT SELECT ON TABLE V_Stock TO stock;
GRANT SELECT ON TABLE V_StockPerProduct TO stock;
GRANT SELECT ON TABLE V_Products TO stock;

-- Block 'producao' from accessing everything
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM producao;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO producao;

-- Allow 'producao' to access:
GRANT EXECUTE ON PROCEDURE PA_Create_Labor TO producao;
GRANT EXECUTE ON PROCEDURE PA_Update_Labor TO producao;
GRANT EXECUTE ON PROCEDURE PA_InsertLine_ProductionOrder TO producao;
GRANT EXECUTE ON PROCEDURE PA_Update_ProductionOrderStatus TO producao;

-- Grant execute on functions to producao
GRANT EXECUTE ON FUNCTION FN_Create_ProductionOrder TO producao;

-- Grant select on views to producao
GRANT SELECT ON TABLE V_Labors TO producao;
GRANT SELECT ON TABLE V_ProductionOrders TO producao;
GRANT SELECT ON TABLE V_ProductionOrderComponents TO producao;


