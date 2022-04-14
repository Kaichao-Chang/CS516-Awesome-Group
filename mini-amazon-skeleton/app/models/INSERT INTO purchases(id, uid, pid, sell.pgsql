INSERT INTO purchases(id, uid, pid, seller_id, quantity, fulfill_by_seller, time_purchased)
VALUES(1010, 2, 12, 5, 10, false, TIMESTAMP '2019-10-19 10:23:54')


-- Celia add the following:
-- user "a a" buy it, and user "Celia" sells it
INSERT INTO Purchases(id, uid, pid, seller_id, quantity, fulfill_by_seller, time_purchased)
VALUES (1011, 5, 10, 5, 10, True, TIMESTAMP '2017-10-19 10:23:54')
