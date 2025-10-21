USE [datos_regulatorios_reco]
GO

/****** Object:  Table [dbo].[Centro MTBT]    Script Date: 21/10/2025 15:05:55 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Centro MTBT](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Código Centro de transformación MT/BT] [varchar](100) NULL,
	[KVA instalado por transformador] [decimal](10, 2) NULL,
	[Equipo aguas arriba] [varchar](500) NULL,
	[Propietario] [varchar](100) NULL,
	[UTM Centro MT/BT Norte] [bigint] NULL,
	[UTM Centro MT/BT Oeste] [bigint] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


-- Tabla [dbo].[Centro MTBT] creada exitosamente.



USE [datos_regulatorios_reco]
GO

/****** Object:  Table [dbo].[Equipos de maniobras]    Script Date: 21/10/2025 15:06:47 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Equipos de maniobras](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Código de equipo] [varchar](100) NULL,
	[Tipo de equipo] [varchar](100) NULL,
	[Código de subestación] [varchar](100) NULL,
	[Codigo de Equipo Aguas Arriba] [varchar](500) NULL,
	[Nivel de tensión] [decimal](6, 2) NULL,
	[Corriente máxima] [int] NULL,
	[UTM Equipo Norte] [bigint] NULL,
	[UTM Equipo Oeste] [bigint] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
-- Tabla [dbo].[Equipos de maniobras] creada exitosamente.

USE [datos_regulatorios_reco]
GO

/****** Object:  Table [dbo].[Interrupciones]    Script Date: 21/10/2025 15:07:04 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Interrupciones](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[ID_Interrupcion] [nvarchar](50) NULL,
	[Fecha y Hora_Inicio] [datetime] NULL,
	[Fecha y Hora_Cierre] [datetime] NULL,
	[Causa] [nvarchar](255) NULL,
	[Fecha Notificacion al Usuario] [date] NULL,
	[Origen del evento] [nvarchar](100) NULL,
	[Codigo de Equipo] [nvarchar](100) NULL,
	[Enlace Medio de Notificacion a los Usuarios] [nvarchar](255) NULL,
	[Observaciones] [nvarchar](255) NULL,
	[Primer Codigo de Equipo] [nvarchar](100) NULL,
	[CódigoDePrimerEquipo] [nvarchar](255) NULL,
	[Código de Equipo] [nvarchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO




