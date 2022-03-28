-- Initialize the average ratings of all the reviews
WITH ReviewSum AS (
    SELECT
        pid,
        AVG(star) as avg_star
    FROM
        ProductReviews
    GROUP BY
        pid
)
UPDATE
    Products UpP
SET
    overall_star = RS.avg_star
FROM
    Products P
    JOIN ReviewSum RS ON P.id = RS.pid
WHERE 
    UpP.id = RS.pid;