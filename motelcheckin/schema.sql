CREATE TABLE Customers(
    cu_id SERIAL,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    birth_date date NOT NULL,
    identification varchar(255) NOT NULL UNIQUE,
    id_type varchar(255) NOT NULL,
    blacklist BOOLEAN NOT NULL,
    notes text NULL,
    unique (first_name,last_name, birth_date),
    PRIMARY KEY (cu_id)
);
CREATE TABLE Rooms(
    room int NOT NULL PRIMARY KEY,
    occupied BOOLEAN NOT NULL,
    type text NOT NULL
);
CREATE TABLE Stays(
    stay_id SERIAL,
    cu_id int NOT NULL,
    check_in_date date NOT NULL,
    check_out_date date NOT NULL,
    status varchar(50) NOT NULL,
    numadults int NOT NULL,
    numchildren int NOT NULL,
    num_pets int NOT NULL,
    room int NOT NULL,
    PRIMARY KEY (stay_id, cu_id),
    FOREIGN KEY (cu_id) REFERENCES Customers (cu_id),
    FOREIGN KEY (room) REFERENCES Rooms (room)
);
CREATE TABLE Stayperiods(
    stay_id int NOT NULL,
    cu_id int NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    price float NOT NULL,
    notes text NULL,
    PRIMARY KEY (stay_id, cu_id, start_date),
    FOREIGN KEY (stay_id, cu_id) REFERENCES Stays (stay_id, cu_id)
);
CREATE TABLE Payments(
    stay_id int NOT NULL,
    cu_id int NOT NULL,
    payment_date timestamp NOT NULL,
    amount float NOT NULL,
    PRIMARY KEY (stay_id,cu_id,payment_date),
    FOREIGN KEY (stay_id, cu_id) REFERENCES Stays (stay_id, cu_id)
)