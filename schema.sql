CREATE TABLE Customers(
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
	birth_date date NOT NULL,
	driving_license_number varchar(20) NULL,
	notes text NULL,
    PRIMARY KEY (first_name, last_name, birth_date)
);
CREATE TABLE Rooms(
	room int NOT NULL PRIMARY KEY
);
CREATE TABLE Stays(
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
	birth_date date NOT NULL,
	check_in_date date NOT NULL,
	scheduled_check_out_date date NOT NULL,
	status varchar(50) NOT NULL,
	room int NOT NULL,
    PRIMARY KEY (first_name, last_name, birth_date, check_in_date),
    FOREIGN KEY (first_name, last_name, birth_date) REFERENCES Customers (first_name, last_name, birth_date),
    FOREIGN KEY (room) REFERENCES Rooms (room)
);