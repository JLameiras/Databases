SELECT dia_semana, concelho, COUNT(unidades) FROM VENDAS
WHERE (ano BETWEEN ‘2019’ AND ‘2021’)
AND (mes BETWEEN ‘1’ AND ‘6’)
AND (dia_mes BETWEEN ‘1’ AND ‘20’)
GROUP BY 
GROUPING SETS (
(dia_semana),
(concelho),
()
);

SELECT concelho, cat, dia_semana, COUNT(unidades) FROM Vendas
WHERE distrito = “Lisboa”
GROUP BY 
GROUPING SETS (
(concelho, cat, dia_semana),
()
);
