CREATE TABLE categoria (
nome VARCHAR (100) PRIMARY KEY
);

CREATE TABLE super_categoria (
nome VARCHAR (100) PRIMARY KEY,
FOREIGN KEY (nome) REFERENCES categoria(nome),
CHECK (NOT is_super_in_simple(nome))
);

CREATE TABLE categoria_simples (
nome VARCHAR (100) PRIMARY KEY,
FOREIGN KEY (nome) REFERENCES categoria(nome),
CHECK (NOT is_simple_in_super(nome))
);

CREATE TABLE tem_outra (
super_categoria VARCHAR (100) ,
categoria VARCHAR (100) PRIMARY KEY,
FOREIGN KEY (categoria) REFERENCES categoria(nome),
FOREIGN KEY (super_categoria) REFERENCES super_categoria(nome),
UNIQUE(super_categoria, categoria),
CHECK(super_categoria != categoria)
);

CREATE TABLE produto (
ean INT PRIMARY KEY,
cat VARCHAR (100),
descr TEXT,
FOREIGN KEY (cat) REFERENCES categoria(nome) ON DELETE SET NULL
);
								
CREATE TABLE tem_categoria(
ean INT ,
nome VARCHAR ,
FOREIGN KEY (ean) REFERENCES produto(ean),
FOREIGN KEY (nome) REFERENCES categoria(nome)
);

CREATE TABLE IVM (
num_serie INT ,
fabricante VARCHAR (100) ,
PRIMARY KEY (num_serie, fabricante)
);

CREATE TABLE ponto_de_retalho (
nome VARCHAR (100) PRIMARY KEY,
distrito VARCHAR (100) ,
concelho VARCHAR (100) 
);

CREATE TABLE instalada_em (
num_serie INT ,
fabricante VARCHAR (100) ,
local VARCHAR (100) ,
FOREIGN KEY (num_serie,fabricante) REFERENCES IVM(num_serie,fabricante),
FOREIGN KEY (local) REFERENCES ponto_de_retalho(nome),
PRIMARY KEY (num_serie, fabricante)
);

CREATE TABLE prateleira (
nro INT ,
num_serie INT ,
fabricante VARCHAR (100) ,
altura INT ,
nome VARCHAR (100) ,
FOREIGN KEY (num_serie,fabricante) REFERENCES IVM(num_serie,fabricante),
FOREIGN KEY (nome) REFERENCES categoria(nome) ON DELETE SET NULL,
PRIMARY KEY (nro , num_serie, fabricante)
);

CREATE TABLE planograma (
ean INT ,
nro INT ,
num_serie INT ,
fabricante VARCHAR (100) ,
faces VARCHAR (100) ,
unidades INT ,
loc VARCHAR (100) ,
FOREIGN KEY (ean) REFERENCES produto(ean),
FOREIGN KEY (nro,num_serie,fabricante) REFERENCES prateleira(nro,num_serie,fabricante),
PRIMARY KEY (ean,nro,num_serie,fabricante)
);

CREATE TABLE retalhista (
tin INT PRIMARY KEY, 
name VARCHAR (100) ,
UNIQUE(name)
);

CREATE TABLE responsavel_por (
nome_cat VARCHAR(100) ,
tin int ,
num_serie int ,
fabricante VARCHAR(100) ,
FOREIGN KEY (num_serie,fabricante) REFERENCES IVM(num_serie,fabricante),
FOREIGN KEY (tin) REFERENCES retalhista(tin),
FOREIGN KEY (nome_cat) REFERENCES categoria(nome)
);

CREATE TABLE evento_reposicao (
ean INT ,
nro INT ,
num_serie INT ,
fabricante VARCHAR (100) ,
instante DATE ,
unidades INT ,
tin INT,
FOREIGN KEY (ean,nro,num_serie,fabricante) REFERENCES planograma(ean,nro, num_serie,fabricante),
FOREIGN KEY (tin) REFERENCES retalhista(tin) ON DELETE SET NULL,
PRIMARY KEY (ean,nro,num_serie,fabricante, instante),
CHECK(unidades <= count_units(ean, nro, num_serie, fabricante))
);

INSERT INTO super_categoria VALUES ('frio');
INSERT INTO super_categoria VALUES ('calor');
INSERT INTO categoria_simples VALUES ('muito frio');
INSERT INTO categoria_simples VALUES ('pouco frio');

INSERT INTO tem_outra VALUES ('frio','muito frio');
INSERT INTO tem_outra VALUES ('frio','pouco frio');

INSERT INTO produto VALUES ('1','pouco frio','iogurte');
INSERT INTO produto VALUES ('2','muito frio','gelo');
INSERT INTO produto VALUES ('3','calor','pao');
INSERT INTO produto VALUES ('4','frio','peixe');

INSERT INTO IVM VALUES ('0001','Bosch');
INSERT INTO IVM VALUES ('0002','Apple');
INSERT INTO IVM VALUES ('0002','Bosch');

INSERT INTO ponto_de_retalho VALUES ('BP', 'Lisboa','Lisboa');
INSERT INTO ponto_de_retalho VALUES ('PD', 'Guarda','Sabugal');

INSERT INTO instalada_em VALUES ('0001','Bosch','BP');
INSERT INTO instalada_em VALUES ('0002','Apple','PD');

INSERT INTO prateleira VALUES ('0','0001','Bosch','2','calor');
INSERT INTO prateleira VALUES ('1','0001','Bosch','2','muito frio');
INSERT INTO prateleira VALUES ('2','0002','Bosch','2','pouco frio');
INSERT INTO prateleira VALUES ('3','0002','Apple','3','muito frio');

INSERT INTO planograma VALUES ('1','2','0002','Bosch','3','20','blah');
INSERT INTO planograma VALUES ('2','1','0001','Bosch','3','20','blah');
INSERT INTO planograma VALUES ('3','0','0001','Bosch','3','20','blah');
INSERT INTO planograma VALUES ('4','3','0002','Apple','3','20','blah');

INSERT INTO retalhista VALUES ('0','Carlos');
INSERT INTO retalhista VALUES ('1','Ze');
INSERT INTO retalhista VALUES ('2','Luis');

INSERT INTO responsavel_por VALUES ('frio','0','0001','Bosch');
INSERT INTO responsavel_por VALUES ('pouco frio','1','0002','Apple');
INSERT INTO responsavel_por VALUES ('muito frio','1','0002','Apple');

INSERT INTO evento_reposicao VALUES ('1','2','0002','Bosch',DATE '2015-12-17','20','1');
INSERT INTO evento_reposicao VALUES ('1','2','0002','Bosch',DATE '2015-12-18','20','1');
INSERT INTO evento_reposicao VALUES ('1','2','0002','Bosch',DATE '2015-12-19','20','1');
