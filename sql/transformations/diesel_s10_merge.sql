MERGE `gen-lang-client-0722386172.rommus_staging_diesel_s10_raw.diesel_s10` AS destino

USING `gen-lang-client-0722386172.rommus_staging_diesel_s10_raw_staging.diesel_s10` AS origem

    ON destino.captured_on = origem.captured_on
    AND destino.legal_name = origem.legal_name
    AND destino.cnpj = origem.cnpj
    AND destino.address = origem.address
    AND destino.address_complement = origem.address_complement
    AND destino.neighborhood = origem.neighborhood
    AND destino.postal_code = origem.postal_code
    AND destino.region = origem.region
    AND destino.state = origem.state
    AND destino.municipality_name = origem.municipality_name
    AND destino.product = origem.product
    AND destino.sell_value = origem.sell_value
    AND destino.purchase_value = origem.purchase_value
    AND destino.measurement_unit = origem.measurement_unit
    AND destino.brand = origem.brand
    AND destino.source_id = origem.source_id
    AND destino.source_type = origem.source_type

WHEN NOT MATCHED THEN

    INSERT (
        captured_on,
        ingested_at,
        legal_name,
        cnpj,
        address,
        address_complement,
        neighborhood,
        postal_code,
        region,
        state,
        municipality_name,
        product,
        sell_value,
        purchase_value,
        measurement_unit,
        brand,
        source_id,
        source_type
    )

    VALUES (
        origem.captured_on,
        origem.ingested_at,
        origem.legal_name,
        origem.cnpj,
        origem.address,
        origem.address_complement,
        origem.neighborhood,
        origem.postal_code,
        origem.region,
        origem.state,
        origem.municipality_name,
        origem.product,
        origem.sell_value,
        origem.purchase_value,
        origem.measurement_unit,
        origem.brand,
        origem.source_id,
        origem.source_type
    );