create table if not exists prerequisite (
	id INT,
	name VARCHAR(50)
);
insert into prerequisite (id, name) values (0, 'None');
insert into prerequisite (id, name) values (1, 'High School Diploma or Equivalent');
insert into prerequisite (id, name) values (2, 'Associate''s Degree');
insert into prerequisite (id, name) values (3, 'Bachelor''s Degree');
insert into prerequisite (id, name) values (4, 'Course(s)');
insert into prerequisite (id, name) values (5, 'Combination of Education and Course(s)');
