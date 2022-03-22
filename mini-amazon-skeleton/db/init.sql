-- Initialize the average ratings of all the reviews
WITH Review_Sum AS (
    SELECT
        pid,
        AVG(star) as avg_star
    FROM
        ProductReviews
    GROUP BY
        pid
)
UPDATE
    Products Up_P
SET
    overall_star = RS.avg_star
FROM
    Products P
    JOIN Review_Sum RS ON P.id = RS.pid
WHERE 
    Up_P.id = RS.pid;