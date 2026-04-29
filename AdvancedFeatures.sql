DROP VIEW IF EXISTS vw_match_scores;
CREATE VIEW vw_match_scores AS
SELECT 
    a.adopter_id,
    p.pet_id,
    a.adopter_name,
    p.pet_name,
    a.age,
	CASE 
		WHEN p.species = 'Dog' AND a.age BETWEEN 25 AND 40 THEN 100
		WHEN p.species = 'Dog' AND a.age BETWEEN 41 AND 55 THEN 90
		WHEN p.species = 'Cat' AND a.age BETWEEN 20 AND 35 THEN 95
		WHEN p.species = 'Cat' AND a.age BETWEEN 36 AND 50 THEN 80
		ELSE 60
	END AS match_score
FROM Adopter a
JOIN Submits s ON a.adopter_id = s.adopter_id
JOIN AdoptionApplication aa ON s.application_id = aa.application_id
JOIN Pet p ON aa.pet_id = p.pet_id;