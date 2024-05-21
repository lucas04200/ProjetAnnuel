-- Création des tables dimension
CREATE TABLE DimDate (
  id_date DATE PRIMARY KEY,
  days TEXT,
  year TEXT,
  mounth TEXT
);

CREATE TABLE DimSourceType (
  id_sourceType INT PRIMARY KEY,
  sourceType TEXT
);

CREATE TABLE DimConversation (
  id_conversation INT PRIMARY KEY,
  conversation TEXT
);

-- Création de la table de faits
CREATE TABLE TableFait (
  id INT PRIMARY KEY,
  lienDate DATE REFERENCES DimDate(id_date),
  lienSourceType INT REFERENCES DimSourceType(id_sourceType),
  lienConversation INT REFERENCES DimConversation(id_conversation)
);
