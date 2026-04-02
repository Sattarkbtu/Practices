-- Pattern search
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT name, phone 
    FROM contacts 
    WHERE name ILIKE '%' || p || '%' OR phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;

-- Pagination
CREATE OR REPLACE FUNCTION get_contacts_paginated(limit_rows INT, offset_rows INT)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT name, phone 
    FROM contacts 
    ORDER BY name
    LIMIT limit_rows OFFSET offset_rows;
END;
$$ LANGUAGE plpgsql;
