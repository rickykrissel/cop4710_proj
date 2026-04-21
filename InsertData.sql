INSERT INTO Shelter (shelter_name, location, amount_of_animals) VALUES
('Happy Tails Shelter', 'Tallahassee, FL', 3),
('Safe Haven Shelter', 'Orlando, FL', 2);

INSERT INTO Pet (pet_name, species, breed, shelter_name, location) VALUES
('Max', 'Dog', 'Labrador', 'Happy Tails Shelter', 'Tallahassee, FL'),
('Bella', 'Cat', 'Siamese', 'Happy Tails Shelter', 'Tallahassee, FL'),
('Charlie', 'Dog', 'Beagle', 'Safe Haven Shelter', 'Orlando, FL'),
('Luna', 'Cat', 'Persian', 'Safe Haven Shelter', 'Orlando, FL'),
('Rocky', 'Dog', 'Bulldog', 'Happy Tails Shelter', 'Tallahassee, FL');

INSERT INTO Staff (position, staff_name, shelter_name, location) VALUES
('Manager', 'Alice Johnson', 'Happy Tails Shelter', 'Tallahassee, FL'),
('Vet Technician', 'Mark Rivera', 'Happy Tails Shelter', 'Tallahassee, FL'),
('Coordinator', 'Lisa Chen', 'Safe Haven Shelter', 'Orlando, FL'),
('Assistant', 'James Patel', 'Safe Haven Shelter', 'Orlando, FL');

INSERT INTO Adopter (adopter_name, email, age) VALUES
('John Smith', 'john.smith@gmail.com', 25),
('Maria Lopez', 'maria.lopez@gmail.com', 34),
('Kevin Brown', 'kevin.brown@gmail.com', 29),
('Sarah Davis', 'sarah.davis@gmail.com', 41),
('Emily Wilson', 'emily.w@gmail.com', 22);

INSERT INTO AdoptionApplication (application_date, application_status, pet_id) VALUES
('2026-04-01', 'Pending', 1),
('2026-04-03', 'Approved', 2),
('2026-04-05', 'Rejected', 3),
('2026-04-07', 'Pending', 4),
('2026-04-10', 'Approved', 5);

INSERT INTO Submits (application_id, adopter_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

INSERT INTO Reviews (staff_id, application_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(1, 5);