INSERT INTO purchases(id, uid, pid, seller_id, quantity, fulfill_by_seller, time_purchased)
VALUES(1028, 2, 12, 5, 100, false, TIMESTAMP '2019-10-19 10:23:54')


-- Celia add the following:
-- user "a a" buy it, and user "Celia" sells it
INSERT INTO Purchases(id, uid, pid, seller_id, quantity, fulfill_by_seller, time_purchased)
VALUES (2001, 5, 3002, 6, 3, True, TIMESTAMP '2017-10-19 10:23:54')

INSERT INTO Products(id, name, price, available, seller_id, overall_star, cate, descr, inv, img)
VALUES (3002, 'Banana Bread', 20.21, True, 6, 4, None, 'It is a bread made with banana.', 9, None)