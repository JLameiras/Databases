SELECT name 
FROM reponsavel_por INNER JOIN retalhista ON responsavel_por.tin = retalhista.tin
WHERE COUNT(responsavel_por.nome_cat) >= ALL (
	SELECT COUNT(nome_cat)
FROM reponsavel_por INNER JOIN retalhista 
ON responsavel_por.tin = retalhista.tin
);

SELECT DISTINCT name 
FROM retalhista
WHERE NOT EXISTS (
SELECT nome
FROM categoria_simples
EXCEPT
SELECT nome_cat
FROM responsavel_por 
WHERE nome_cat IN (SELECT nome FROM categoria_simples)
AND responsavel_por.tin = retalhista.tin
);

SELECT ean FROM produto
WHERE ean NOT IN (
SELECT ean FROM evento_reposicao
);

SELECT ean 
FROM evento_reposicao
WHERE COUNT(DISTINCT tin) = 1 (
	SELECT ean, COUNT(DISTINCT tin) FROM evento_reposicao
);