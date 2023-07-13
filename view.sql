CREATE VIEW Vendas (ean, cat, ano, trimestre, mes, dia_mes, dia_semana, distrito, concelho, unidades)
AS
SELECT p.ean,  p.cat, (EXTRACT (YEAR FROM e.instante)) AS ano, (EXTRACT (QUARTER FROM e.instante)) AS trimestre,  (EXTRACT (MONTH FROM e.instante)) AS mes,  (EXTRACT (DAY FROM e.instante)) AS dia_mes, (EXTRACT (DOW FROM e.instante)) AS dia_semana,  r.distrito, r.concelho, e.unidades
FROM evento_reposicao e
JOIN produto p
ON e.ean = p.ean
JOIN instalada_em as i
ON i.num_serie = e.num_serie
JOIN ponto_de_retalho r
ON r.nome = i.local;
