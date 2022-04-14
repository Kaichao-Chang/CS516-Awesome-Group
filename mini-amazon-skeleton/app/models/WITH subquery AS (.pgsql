
WITH subquery AS (
    SELECT order_id as oid, o.uid AS uid, p.seller_id AS sid, CONCAT(u.firstname, ' ', u.lastname) AS sname, SUM(p.unit_price*p.quantity) AS total_price, SUM(p.quantity) AS total_quantity, o.completed_status, o.placed_datetime
    FROM Purchases AS p, Users AS u, Orders as o 
    WHERE o.pur_id = p.id
    AND p.seller_id = u.id
    GROUP BY order_id, o.uid, p.seller_id, u.firstname, u.lastname, o.completed_status, o.placed_datetime )

SELECT oid, uid, completed_status,  MIN(placed_datetime) AS placed_datetime, ARRAY_AGG(sid) AS sidList, ARRAY_AGG(sname) AS sellersList, SUM(total_price) AS total_price_all_sellers, SUM(total_quantity) AS total_quantity_all_sellers
FROM subquery
GROUP BY oid, uid, completed_status
ORDER BY placed_datetime DESC



 "WITH subquery AS (" \
                    "SELECT order_id as oid, o.uid AS uid, p.seller_id AS sid, CONCAT(u.firstname, ' ', u.lastname) AS sname, SUM(p.unit_price*p.quantity) AS total_price, SUM(p.quantity) AS total_quantity, o.completed_status, o.placed_datetime " \
                    "FROM Purchases AS p, Users AS u,  Orders as o " \
                    "WHERE o.uid = :uid " \
                        "AND o.pur_id = p.id " \
                        "AND u.id = p.seller_id " \
                        "AND ( ( o.placed_datetime >= :start_date AND o.placed_datetime <= :end_date ) )" \
                    "GROUP BY order_id, o.uid, p.seller_id, u.firstname, u.lastname, o.completed_status, o.placed_datetime ) "\
                "SELECT oid, uid, completed_status, MIN(placed_datetime) AS placed_datetime, ARRAY_AGG(sid) AS sidList, ARRAY_AGG(sname) AS sellersList, SUM(total_price) AS total_price_all_sellers, SUM(total_quantity) AS total_quantity_all_sellers "\
                "FROM subquery " \
                "GROUP BY oid, uid, completed_status "\
                "ORDER BY placed_datetime DESC "