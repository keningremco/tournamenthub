CREATE TABLE test (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    naam VARCHAR(100) NOT NULL,
    onzin VARCHAR(255),
    getal INT,
    actief BOOLEAN NOT NULL DEFAULT TRUE,
    aangemaakt_op TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id)
) ENGINE=InnoDB;

INSERT INTO test (naam, onzin, getal)
VALUES
    ('Pietje', 'blabla', 42),
    ('Henkie', 'super onzin', 123),
    ('Test', 'dit is een test', 999);