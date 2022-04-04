-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.
CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(12, 2) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    seller_id INT NOT NULL REFERENCES Users(id),
    overall_star FLOAT NOT NULL DEFAULT 0,
    cate VARCHAR(1),
    descr VARCHAR(255),
    inv INT NOT NULL
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE ProductReviews (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    content TEXT NOT NULL,
    star INT NOT NULL,
    UNIQUE (uid, pid),
    CHECK (star in (0, 1, 2, 3, 4, 5))
);

CREATE TABLE SellerReviews (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    customer_id INT NOT NULL REFERENCES Users(id),
    seller_id INT NOT NULL REFERENCES Users(id),
    content TEXT NOT NULL,
    star INT NOT NULL,
    UNIQUE (customer_id, seller_id),
    CHECK (star in (0, 1, 2, 3, 4, 5))
);

CREATE TABLE Sellers (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id)
);

CREATE TABLE Sales (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    sale_status TEXT NOT NULL
);

