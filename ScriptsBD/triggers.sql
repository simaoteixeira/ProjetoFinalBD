/**
    Antes de inserir a linha de uma ordem de compra, temos de atualizar os valores totais da própria linha e depois atualizar os valores totais da ordem de compra
*/
CREATE OR REPLACE FUNCTION TR_purchasing_order_components_PRE_INS() RETURNS TRIGGER AS $$
DECLARE
    _vat_value MONEY;
    _discount_value MONEY;
    _line_total MONEY;
    _total_base MONEY;
    _vat_total MONEY;
    _discount_total MONEY;
    _total MONEY;
BEGIN 
    _vat_value := NEW.price_base * (NEW.vat / 100.0) * NEW.quantity;
    _discount_value := NEW.price_base * (NEW.discount / 100.0) * NEW.quantity;
    _line_total := (NEW.price_base * NEW.quantity) + _vat_value - _discount_value;

    
    NEW.vat_value := _vat_value;
    NEW.discount_value := _discount_value;
    NEW.line_total := _line_total;

    _total_base := (SELECT COALESCE(SUM(price_base * quantity),0::MONEY) FROM purchasing_order_components WHERE id_purchasing_order = NEW.id_purchasing_order) + NEW.price_base * NEW.quantity;
    _vat_total := (SELECT COALESCE(SUM(vat_value),0::MONEY) FROM purchasing_order_components WHERE id_purchasing_order = NEW.id_purchasing_order) + _vat_value;
    _discount_total := (SELECT COALESCE(SUM(discount_value),0::MONEY) FROM purchasing_order_components WHERE id_purchasing_order = NEW.id_purchasing_order) + _discount_value;
    _total := _total_base + _vat_total - _discount_total;
    
    UPDATE purchasing_orders
    SET total_base = _total_base, vat_total = _vat_total, discount_total = _discount_total, total = _total
    WHERE id_purchasing_order = NEW.id_purchasing_order;
    
    RETURN NEW;
END;

$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER TR_purchasing_order_components_PRE_INS
BEFORE INSERT OR UPDATE ON purchasing_order_components
FOR EACH ROW
EXECUTE PROCEDURE TR_purchasing_order_components_PRE_INS();

