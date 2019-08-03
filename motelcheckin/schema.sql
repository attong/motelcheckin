CREATE TABLE Customers(
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    birth_date date NOT NULL,
    driving_license_number varchar(20) NULL UNIQUE,
    notes text NULL,
    PRIMARY KEY (first_name, last_name, birth_date)
);
CREATE TABLE Rooms(
    room int NOT NULL PRIMARY KEY,
    occupied BOOLEAN NOT NULL,
    type text NOT NULL
);
CREATE TABLE Stays(
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    birth_date date NOT NULL,
    check_in_date date NOT NULL,
    scheduled_check_out_date date NOT NULL,
    status varchar(50) NOT NULL,
    numadults int NOT NULL,
    numchildren int NOT NULL,
    room int NOT NULL,
    PRIMARY KEY (first_name, last_name, birth_date, check_in_date),
    FOREIGN KEY (first_name, last_name, birth_date) REFERENCES Customers (first_name, last_name, birth_date),
    FOREIGN KEY (room) REFERENCES Rooms (room)
);
CREATE TABLE Stayperiods(
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    birth_date date NOT NULL,
    check_in_date date NOT NULL,
    period_start_date date NOT NULL,
    period_end_date date NOT NULL,
    price float NOT NULL,
    PRIMARY KEY (first_name, last_name, birth_date, check_in_date,period_start_date),
    FOREIGN KEY (first_name, last_name, birth_date, check_in_date) REFERENCES Stays (first_name, last_name, birth_date, check_in_date)
);