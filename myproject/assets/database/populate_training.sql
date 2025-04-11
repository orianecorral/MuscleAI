-- Création de la table Training si elle n'existe pas
CREATE TABLE IF NOT EXISTS training (
    id SERIAL PRIMARY KEY,
    training_name VARCHAR(200) NOT NULL,
    training_type VARCHAR(200) NOT NULL,
    training_duration INTEGER NOT NULL,
    training_calories INTEGER NOT NULL,
    training_date DATE NOT NULL
);

-- Insertion des 10 entrées de test
INSERT INTO training (training_name, training_type, training_duration, training_calories, training_date)
VALUES 
('Morning Cardio Blast', 'Cardio', 45, 400, CURRENT_DATE - INTERVAL '1 day'),
('Upper Body Strength', 'Musculation', 60, 500, CURRENT_DATE - INTERVAL '2 days'),
('Leg Day Challenge', 'Musculation', 75, 600, CURRENT_DATE - INTERVAL '3 days'),
('Yoga Flow', 'Yoga', 40, 200, CURRENT_DATE - INTERVAL '4 days'),
('HIIT Burner', 'HIIT', 30, 350, CURRENT_DATE - INTERVAL '5 days'),
('Pilates Core', 'Pilates', 50, 300, CURRENT_DATE - INTERVAL '6 days'),
('Back and Biceps', 'Musculation', 65, 550, CURRENT_DATE - INTERVAL '7 days'),
('Evening Run', 'Cardio', 55, 450, CURRENT_DATE - INTERVAL '8 days'),
('Mobility Routine', 'Mobilité', 35, 180, CURRENT_DATE - INTERVAL '9 days'),
('Full Body Circuit', 'Circuit Training', 60, 520, CURRENT_DATE - INTERVAL '10 days');
