-- ==========================================
--  Script de creación de base de datos
--  Proyecto: Luz del Saber 📚
--  Descripción: Sistema de gestión de inventario y ventas
-- ==========================================

-- 1️⃣ Crear base de datos
CREATE DATABASE LuzDelSaberDB;
GO

-- 2️⃣ Usar la base de datos recién creada
USE LuzDelSaberDB;
GO

-- 3️⃣ Crear tabla de Libros
CREATE TABLE libros (
    id INT IDENTITY(1,1) PRIMARY KEY,
    titulo NVARCHAR(150) NOT NULL,
    autor NVARCHAR(100) NOT NULL,
    isbn NVARCHAR(20) UNIQUE NOT NULL,
    categoria NVARCHAR(50),
    stock INT NOT NULL CHECK (stock >= 0),
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0)
);
GO

-- 4️⃣ Crear tabla de Ventas
CREATE TABLE ventas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    libro_id INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
    fecha DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (libro_id) REFERENCES libros(id)
);
GO

-- 5️⃣ Índices para optimizar búsquedas
CREATE INDEX idx_libros_titulo ON libros(titulo);
CREATE INDEX idx_libros_categoria ON libros(categoria);
CREATE INDEX idx_ventas_fecha ON ventas(fecha);
GO

-- 6️⃣ Insertar algunos libros de ejemplo (opcional)
INSERT INTO libros (titulo, autor, isbn, categoria, stock, precio) VALUES
('Python para Todos', 'Raúl Martínez', '9781234567890', 'Programación', 15, 79.90),
('Aprendiendo SQL', 'Lucía Torres', '9789876543210', 'Bases de Datos', 10, 69.50),
('Introducción a la IA', 'Miguel Rojas', '9781111111111', 'Inteligencia Artificial', 5, 120.00),
('Java desde Cero', 'María López', '9782222222222', 'Programación', 8, 85.75);
GO

select*from libros
go

select *from ventas
go