INSERT INTO Customers (first_name, last_name, birth_date, identification, id_type,blacklist)
VALUES 
('derek','sun','9/12/93','F123456','drivers license','FALSE'),
('michael','feger','3/10/93','F543215','drivers license','FALSE'),
('matt','decaro','5/20/93','F547215','drivers license','FALSE');

INSERT INTO Rooms VALUES (1, FALSE, 'single'),(2, FALSE, 'single'),
(3, FALSE, 'single'),(4, FALSE, 'single'),(5, FALSE, 'single'),(6, FALSE, 'double'),(7, FALSE, 'single'),
(8, FALSE, 'double'),(9, FALSE, 'double'),(10, FALSE, 'double');

INSERT INTO Stays (cu_id,check_in_date,check_out_date,status,numadults,numchildren,num_pets, room) VALUES
(1,'1/1/2010','1/2/2010','checked out',1,0,1,3),
(2,'5/1/2010','5/2/2010','checked out',2,0,0,5);

INSERT INTO Stayperiods VALUES
(1,1,'1/1/2010','1/2/2010','65'),
(2,2,'5/1/2010','5/2/2010','125');