MERGE `rommus.reference.diesel_s10` AS destino

USING `rommus.staging.diesel_s10` AS origem

ON destino.data_coleta = origem.data_coleta
AND destino.estado_sigla = origem.estado_sigla
AND destino.municipio = origem.municipio
AND destino.produto = origem.produto
AND destino.bandeira IS NOT DISTINCT FROM origem.bandeira

WHEN NOT MATCHED THEN

    INSERT (
        anomes,
        regiao_sigla,
        estado_sigla,
        municipio,
        produto,
        data_coleta,
        valor_venda,
        bandeira
    )

    VALUES (
        origem.anomes,
        origem.regiao_sigla,
        origem.estado_sigla,
        origem.municipio,
        origem.produto,
        origem.data_coleta,
        origem.valor_venda,
        origem.bandeira
    );