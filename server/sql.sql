





CREATE TABLE Matiere  (code_mat  VARCHAR(8) NOT NULL,
                     	nom_mat integer,
                     	id_enseignant  integer,
                     	CONSTRAINT PK_Concerner PRIMARY KEY (code_mat),
			            CONSTRAINT FK_Id_Enseignant FOREIGN KEY (id_enseignant) REFERENCES Enseignant(id_enseignant)
					  );


                          
					



