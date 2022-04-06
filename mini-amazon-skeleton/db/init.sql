-- Initialize the average ratings of all the produce reviews
WITH ProductReviewSum AS (
    SELECT
        pid,
        AVG(star) as avg_star
    FROM
        ProductReviews
    GROUP BY
        pid
)
UPDATE
    Products
SET
    overall_star = PRS.avg_star
FROM
    Products P, ProductReviewSum PRS
WHERE 
    Products.id = PRS.pid;

-- Initialize the average ratings of all the seller reviews
WITH SellerReviewSum AS (
    SELECT
        seller_id,
        AVG(star) as avg_star
    FROM
        SellerReviews
    GROUP BY
        seller_id
)
UPDATE
    Sellers
SET
    overall_star = SRS.avg_star
FROM
    SellerReviewSum SRS
WHERE 
    Sellers.id = SRS.seller_id;