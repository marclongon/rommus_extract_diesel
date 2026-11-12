SELECT
    data_coleta,
    estado_sigla,
    municipio,
    produto,
    bandeira,
    COUNT(*) AS quantidade
FROM `rommus.staging.diesel_s10`
GROUP BY
    data_coleta,
    estado_sigla,
    municipio,
    produto,
    bandeira
HAVING COUNT(*) > 1;