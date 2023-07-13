CREATE OR REPLACE FUNCTION is_super_in_simple(nome_in VARCHAR(100))
RETURNS BOOLEAN AS 
$$
DECLARE resultado BOOLEAN;
BEGIN
    SELECT (EXISTS (
        SELECT nome FROM categoria_simples
    	    WHERE nome_in = categoria_simples.nome
    ))
    INTO resultado;
    return resultado;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION is_simple_in_super(nome_in VARCHAR(100))
RETURNS BOOLEAN AS 
$$
DECLARE resultado BOOLEAN;
BEGIN
    SELECT (EXISTS (
        SELECT nome FROM super_categoria
    	    WHERE nome_in = super_categoria.nome
    ))
    INTO resultado;
    return resultado;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_tem_categoria()
RETURNS TRIGGER AS
$$
BEGIN
INSERT INTO tem_categoria VALUES (NEW.ean, NEW.cat);
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION count_units(ean_in INT, nro_in INT, num_serie_in INT, fabricante_in VARCHAR)
RETURNS INT AS 
$$
DECLARE units INT;
BEGIN
    SELECT SUM(unidades)
    FROM Planograma as P
    WHERE P.ean=ean_in AND P.nro=nro_in AND P.num_serie=num_serie_in AND P.fabricante=fabricante_in
    INTO units;
    RETURN units;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_evento_reposicao()
RETURNS TRIGGER AS
$$
BEGIN
IF NOT EXISTS (
    SELECT cat FROM produto
    WHERE ean = NEW.ean
    INTERSECT
    SELECT nome AS cat FROM prateleira 
    WHERE nro = NEW.nro
)
THEN
    RAISE EXCEPTION 'Um Produto só pode ser reposto numa Prateleira que apresente (pelo menos) uma das Categorias desse produto';
ELSE 
    RETURN NEW;
END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER novo_tem_categoria
AFTER INSERT
ON produto
FOR EACH ROW
EXECUTE PROCEDURE insert_tem_categoria();

CREATE TRIGGER repoe_prateleira
BEFORE UPDATE OR INSERT
ON evento_reposicao
FOR EACH ROW
EXECUTE PROCEDURE insert_evento_reposicao();

CREATE OR REPLACE FUNCTION insert_category()
RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO categoria VALUES (NEW.nome);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER nova_categoria_simples
BEFORE INSERT
ON categoria_simples
FOR EACH ROW
EXECUTE PROCEDURE insert_category();

CREATE TRIGGER nova_super_categoria
BEFORE INSERT
ON super_categoria
FOR EACH ROW
EXECUTE PROCEDURE insert_category();
  
CREATE OR REPLACE FUNCTION remove_category()
RETURNS TRIGGER AS
$$
BEGIN
    DELETE FROM categoria
    WHERE nome = OLD.nome;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER remove_categoria_simples
AFTER DELETE
ON categoria_simples 
FOR EACH ROW
EXECUTE PROCEDURE remove_category();

CREATE TRIGGER remove_super_categoria
AFTER DELETE
ON super_categoria 
FOR EACH ROW
EXECUTE PROCEDURE remove_category();
