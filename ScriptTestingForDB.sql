CREATE DATABASE datos_regulatorios_reco
use datos_regulatorios_reco
 
CREATE TABLE [Centro MTBT] ( id INT IDENTITY(1,1) PRIMARY KEY,
[Código Centro de transformación MT/BT] NVARCHAR(100),
[KVA instalado por transformador] DECIMAL (6,4),
[Equipo aguas arriba] NVARCHAR(100),
[Propietario] NVARCHAR(100),
[UTM Centro MT/BT Norte] INT,
[UTM Centro MT/BT Oeste] INT
);

CREATE TABLE [Equipos de maniobras] ( id INT IDENTITY(1,1) PRIMARY KEY,
[Código de equipo] NVARCHAR(100),
[Tipo de equipo] NVARCHAR(100),
[Código de subestación] NVARCHAR(50),
[Codigo de Equipo Aguas Arriba] NVARCHAR(100),
[Nivel de tensión] DECIMAL (3,2),
[Corriente máxima] INT,
[UTM Equipo Norte] INT,
[UTM Equipo Oeste] INT);

CREATE TABLE [Interrupciones] (id INT IDENTITY(1,1) PRIMARY KEY,
[ID_Interrupcion] NVARCHAR(50),
[Fecha y Hora_Inicio] DATETIME,
[Fecha y Hora_Cierre] DATETIME,
[Causa] NVARCHAR(255),
[Fecha Notificacion al Usuario] DATE,
[Origen del evento] NVARCHAR(100),
[Codigo de Equipo] NVARCHAR(100),
[Enlace Medio de Notificacion a los Usuarios]  NVARCHAR(255),
[Observaciones] NVARCHAR(255),
[Primer Codigo de Equipo] NVARCHAR(100),
);

ALTER TABLE [Interrupciones] 
ADD [Código de Equipo] NVARCHAR(255) NULL;

ALTER TABLE [Interrupciones] 
ADD [CódigoDePrimerEquipo] NVARCHAR(255) NULL;

SELECT *FROM [Equipos de maniobras]

SELECT *FROM [Centro MTBT]




SELECT default_schema_name 
FROM sys.database_principals 
WHERE name = USER_NAME();



--Testing the Centro MTBT and Equipos de maniobras Tables DataTypes
-- Check current data type
EXEC sp_help 'Centro MTBT';

-- Fix UTM columns
ALTER TABLE [Centro MTBT]
ALTER COLUMN [UTM Centro MT/BT Norte] BIGINT NULL;

ALTER TABLE [Centro MTBT]
ALTER COLUMN [UTM Centro MT/BT Oeste] BIGINT NULL;

-- Check current data type
EXEC sp_help 'Equipos de maniobras';

-- Fix UTM columns
ALTER TABLE [Equipos de maniobras]
ALTER COLUMN [UTM Equipo Norte] BIGINT NULL;

ALTER TABLE [Equipos de maniobras]
ALTER COLUMN [UTM Equipo Oeste] BIGINT NULL;


-- Fix KVA overflow (currently DECIMAL(6,4), needs DECIMAL(10,2))
ALTER TABLE [Centro MTBT]
ALTER COLUMN [KVA instalado por transformador] DECIMAL(10,2) NULL;

-- Fix Nivel de tensión overflow (currently DECIMAL(3,2), needs DECIMAL(6,2))
ALTER TABLE [Equipos de maniobras]
ALTER COLUMN [Nivel de tensión] DECIMAL(6,2) NULL;


--Script para el arreglo de los tamaños de las columnas
USE datos_regulatorios_reco;
GO

PRINT 'Increasing column sizes for Centro MTBT...';

-- Increase Equipo aguas arriba from VARCHAR(100) to VARCHAR(500)
ALTER TABLE [Centro MTBT]
ALTER COLUMN [Equipo aguas arriba] VARCHAR(500) NULL;

-- Also increase other string columns to be safe
ALTER TABLE [Centro MTBT]
ALTER COLUMN [Código Centro de transformación MT/BT] VARCHAR(100) NULL;

ALTER TABLE [Centro MTBT]
ALTER COLUMN [Propietario] VARCHAR(100) NULL;

PRINT '✓ Centro MTBT columns increased';

PRINT 'Increasing column sizes for Equipos de maniobras...';

-- Increase Codigo de Equipo Aguas Arriba from VARCHAR(100) to VARCHAR(500)
ALTER TABLE [Equipos de maniobras]
ALTER COLUMN [Codigo de Equipo Aguas Arriba] VARCHAR(500) NULL;

-- Also increase other string columns
ALTER TABLE [Equipos de maniobras]
ALTER COLUMN [Código de equipo] VARCHAR(100) NULL;

ALTER TABLE [Equipos de maniobras]
ALTER COLUMN [Tipo de equipo] VARCHAR(100) NULL;

ALTER TABLE [Equipos de maniobras]
ALTER COLUMN [Código de subestación] VARCHAR(100) NULL;

PRINT '✓ Equipos de maniobras columns increased';

PRINT 'All string columns updated successfully!';
GO