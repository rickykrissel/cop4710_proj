CREATE TABLE Shelter (
    shelter_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    amount_of_animals INTEGER NOT NULL,
    PRIMARY KEY (shelter_name, location)
);

CREATE TABLE Pet (
    pet_id INTEGER AUTO_INCREMENT NOT NULL,
    pet_name VARCHAR(100) NOT NULL,
    species VARCHAR(50) NOT NULL,
    breed VARCHAR(50) NOT NULL,
    shelter_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    PRIMARY KEY (pet_id),
    FOREIGN KEY (shelter_name, location) REFERENCES Shelter(shelter_name, location)
);

CREATE TABLE Adopter (
    adopter_id INTEGER AUTO_INCREMENT NOT NULL,
    adopter_name VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    age INTEGER NOT NULL,
    PRIMARY KEY (adopter_id)
);

CREATE TABLE Staff (
    staff_id INTEGER AUTO_INCREMENT NOT NULL,
    position VARCHAR(100) NOT NULL,
    staff_name VARCHAR(100) NOT NULL,
    shelter_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    PRIMARY KEY (staff_id),
    FOREIGN KEY (shelter_name, location) REFERENCES Shelter(shelter_name, location)
);

CREATE TABLE AdoptionApplication (
    application_id INTEGER AUTO_INCREMENT NOT NULL,
    application_date DATE NOT NULL,
    application_status VARCHAR(20) NOT NULL,
    pet_id INTEGER NOT NULL,
    PRIMARY KEY (application_id),
    FOREIGN KEY (pet_id) REFERENCES Pet(pet_id)
);

CREATE TABLE Submits (
    application_id INTEGER NOT NULL,
    adopter_id INTEGER NOT NULL,
    PRIMARY KEY (application_id, adopter_id),
    FOREIGN KEY (application_id) REFERENCES AdoptionApplication(application_id),
    FOREIGN KEY (adopter_id) REFERENCES Adopter(adopter_id)
);

CREATE TABLE Reviews (
    staff_id INTEGER NOT NULL,
    application_id INTEGER NOT NULL,
    PRIMARY KEY (staff_id, application_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id),
    FOREIGN KEY (application_id) REFERENCES AdoptionApplication(application_id)
);
        