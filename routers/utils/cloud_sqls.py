read_tmp_without_dup = """
-- Step 1: Remove duplicates based on event_id from the temporary table
CREATE TEMP TABLE IF NOT EXISTS temp_table_no_duplicates AS 
SELECT 
    event_id, 
    MAX(request_id) AS request_id, 
    MAX(event_type) AS event_type, 
    MAX(event_timestamp) AS event_timestamp, 
    MAX(affected_assets) AS affected_assets, 
    MAX(anomaly_score) AS anomaly_score
FROM 
    cloud_events_tmp
GROUP BY 
    event_id;
"""

insert_tmp_into_target_sql = """
-- Step 2: Insert into the target table without duplicates 
INSERT INTO cloud_events (event_id, request_id, event_type, event_timestamp, affected_assets, anomaly_score)
SELECT 
    event_id, 
    request_id, 
    event_type, 
    event_timestamp, 
    affected_assets, 
    anomaly_score
FROM 
    temp_table_no_duplicates
WHERE 
    event_id NOT IN (SELECT event_id FROM cloud_events);
"""

truncate_tmp_table = "DELETE FROM cloud_events_tmp"
