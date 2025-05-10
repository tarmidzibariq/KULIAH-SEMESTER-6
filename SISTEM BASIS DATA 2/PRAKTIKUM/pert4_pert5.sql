-- Baru buat tabel
CREATE TABLE Users (
    id INT PRIMARY KEY,
    name CHAR(100),
    email CHAR(100),
    phone INT,
    address TEXT,
    role VARCHAR(10),
    created_at DATE
);

select * from users;
-- table cars

CREATE TYPE transmission_type AS ENUM ('manual', 'automatic');
CREATE TYPE sale_type_enum AS ENUM ('user', 'showroom');
CREATE TYPE status_car_enum AS ENUM ('available', 'sold', 'pending_check', 'under_review');


CREATE TABLE Cars (
    id INT PRIMARY KEY,
    user_id INT REFERENCES Users(id),
    brand CHAR(100),
    model CHAR(100),
    year INT,
    price INT,
    transmission transmission_type,
    service_history CHAR(100),
    fuel_type TEXT,
    mileage CHAR(100),
    description TEXT,
    sale_type sale_type_enum,
    status status_car_enum,
    created_at DATE
);

-- downPayments
CREATE TYPE payment_status_enum AS ENUM ('pending', 'confirmed', 'cancelled');

CREATE TABLE Down_Payments (
    id INT PRIMARY KEY,
    user_id INT REFERENCES Users(id),
    car_id INT REFERENCES Cars(id),
    amount INT,
    payment_status payment_status_enum,
    appointment_date DATE,
    payment_proof CHAR(100),
    created_at DATE
);

-- sales_records
CREATE TYPE status_sales_records_enum AS ENUM ('pending', 'confirmed', 'cancelled');

CREATE TABLE sales_records (
    id INT PRIMARY KEY,
    car_id INT REFERENCES Cars(id),
    buyer_id INT REFERENCES Users(id),
    saler_id INT REFERENCES Users(id),
    sale_price INT,
    sale_date DATE,
    status status_sales_records_enum,
    created_at DATE
);
select * from sales_records
-- reviews
CREATE TYPE status_review_enum AS ENUM ('pending', 'approved', 'rejected');

CREATE TABLE reviews (
    id INT PRIMARY KEY,
    car_id INT REFERENCES Cars(id),
    user_id INT REFERENCES Users(id),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    photo_review CHAR(255),
    status status_review_enum,
    created_at DATE
);
select * from reviews
-- offers
CREATE TABLE offers (
    id INT PRIMARY KEY,
    user_id INT REFERENCES Users(id),
    brand CHAR(100),
    mileage CHAR(50),
    status status_review_enum,
    transmission transmission_type,
    offered_price INT,
    year INT,
    model CHAR(100),
    condition TEXT,
    inspection_date DATE,
    created_at DATE
);
select * from offers

INSERT INTO Users (id, name, email, phone, address, role, created_at)
VALUES (2, 'Tarmidzi Bariq', 'bariq@example.com', 081224331, 'Depok', 'user', '2025-06-11');
select * from users;


INSERT INTO Cars (id, user_id, brand, model, year, price, transmission, service_history, fuel_type, mileage, description, sale_type, status, created_at)
VALUES (1, 1, 'Toyota', 'Avanza', 2020, 180000000, 'automatic', 'Yes', 'Petrol', '25000 km', 'Well-maintained family car', 'showroom', 'available', '2025-05-10');
select * from cars;

INSERT INTO Down_Payments (id, user_id, car_id, amount, payment_status, appointment_date, payment_proof, created_at)
VALUES (1, 1, 1, 50000000, 'confirmed', '2025-05-15', 'proof_001.jpg', '2025-05-10');
select * from down_payments;

INSERT INTO sales_records (id, car_id, buyer_id, saler_id, sale_price, sale_date, status, created_at)
VALUES (1, 1, 1, 1, 180000000, '2025-05-20', 'confirmed', '2025-05-10');
select * from sales_records;

INSERT INTO reviews (id, car_id, user_id, rating, comment, photo_review, status, created_at)
VALUES (1, 1, 1, 5, 'Excellent car, just as described!', 'review_001.jpg', 'approved', '2025-05-10');
select * from reviews;

INSERT INTO offers (id, user_id, brand, mileage, status, transmission, offered_price, year, model, condition, inspection_date, created_at)
VALUES (1, 1, 'Honda', '32000 km', 'pending', 'manual', 150000000, 2019, 'Brio', 'Very good condition, minor scratches', '2025-05-12', '2025-05-10');
select * from offers;

SELECT u.id AS user_id, u.name, c.id AS car_id, c.brand, c.model
FROM Users u
LEFT JOIN Cars c ON u.id = c.user_id;

SELECT u.id AS user_id, u.name, c.id AS car_id, c.brand, c.model
FROM Users u
RIGHT JOIN Cars c ON u.id = c.user_id;

SELECT u.id AS user_id, u.name, c.id AS car_id, c.brand, c.model
FROM Users u
FULL JOIN Cars c ON u.id = c.user_id;

SELECT c.id AS car_id, c.brand, r.rating, r.comment
FROM Cars c
LEFT JOIN Reviews r ON c.id = r.car_id;

update users set phone=628122052 where id = 2;
select * from users;

delete from users  where id = 2;
select * from users;