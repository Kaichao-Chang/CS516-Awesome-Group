INSERT INTO order_fulfill(id, time_fulfilled)
VALUES (1021, TIMESTAMP '2018-10-19 10:23:54')



INSERT INTO Purchases(id, uid, pid, seller_id, quantity, fulfill_by_seller, time_purchased)
VALUES (3000, 5, 1, 6, 3, , True, TIMESTAMP '2018-10-19 10:23:54')

INSERT INTO SellerReviews(VALUES (3000, 6, 5, 6, 3, , True, TIMESTAMP '2018-10-19 10:23:54'))
VALUES (3000, 6, 5, 1, 0, TIMESTAMP '2018-10-19 10:23:54')