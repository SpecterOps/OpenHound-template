-- Keep only the organization properties needed for asset enrichment.
CREATE OR REPLACE TABLE __SCHEMA__.organization_names AS
SELECT DISTINCT id, name
FROM __SCHEMA__.organizations;
