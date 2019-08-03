INSERT INTO Customers (first_name, last_name, birth_date, driving_license_number)
VALUES 
('derek','sun','9/12/93','F123456'),
('michael','feger','3/10/93','F543215'),
('matt','decaro','5/20/93','F547215');

INSERT INTO Customers (first_name, last_name, birth_date)
VALUES 
('eric','ho','3/15/93');

INSERT INTO Rooms VALUES (1, FALSE, 'single'),(2, FALSE, 'single'),
(3, FALSE, 'single'),(4, FALSE, 'single'),(5, FALSE, 'single'),(6, FALSE, 'double'),(7, FALSE, 'single'),
(8, FALSE, 'double'),(9, FALSE, 'double'),(10, FALSE, 'double');

INSERT INTO Stays VALUES
('derek','sun','9/12/93','1/1/2010','1/2/2010','checked out',3),
('matt','decaro','5/20/93','1/5/2010','1/3/2010','checked out',4);

INSERT INTO Stayperiods VALUES
('derek','sun','9/12/93','1/1/2010','1/1/2010','1/2/2010','65'),
('matt','decaro','5/20/93','1/5/2010','1/5/2010','1/3/2010','125');