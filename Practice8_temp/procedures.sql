-- Upsert (insert or update)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- Bulk insert with phone validation
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(p_names VARCHAR[], p_phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT := 1;
    invalid_data TEXT[] := '{}';
BEGIN
    WHILE i <= array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^\d{10}$' THEN
            CALL upsert_contact(p_names[i], p_phones[i]);
        ELSE
            invalid_data := array_append(invalid_data, p_names[i] || ':' || p_phones[i]);
        END IF;
        i := i + 1;
    END LOOP;

    IF array_length(invalid_data, 1) > 0 THEN
        RAISE NOTICE 'Invalid entries: %', invalid_data;
    END IF;
END;
$$;

-- Delete procedure
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts WHERE name = p_value OR phone = p_value;
END;
$$;
