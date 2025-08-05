# 🔧 Guía para Corregir Problemas Críticos - ACA 3.0

## 🎯 Resumen de Problemas Encontrados

**Total de correcciones necesarias: 11**

### **🔴 Problemas Críticos Identificados:**

1. **`citas`** - Falta clave primaria (id) y empresa_id
2. **`security_logs`** - Falta clave primaria (id)
3. **`archivos_reportes`** - Falta clave primaria (id) y empresa_id
4. **`meses_reportes`** - Tabla no existe

---

## 📋 Opción 1: CORRECCIÓN AUTOMÁTICA (Recomendada)

### **Paso 1: Ir a Supabase Dashboard**
1. 🌐 Abre [supabase.com](https://supabase.com)
2. 🔑 Inicia sesión en tu cuenta
3. 📊 Selecciona tu proyecto ACA 3.0

### **Paso 2: Abrir SQL Editor**
1. 📝 En el panel izquierdo, haz clic en **"SQL Editor"**
2. ➕ Haz clic en **"New Query"**

### **Paso 3: Ejecutar Script Automático**
Copia y pega el siguiente script:

```sql
-- 🔧 CORRECCIÓN AUTOMÁTICA DE PROBLEMAS CRÍTICOS - ACA 3.0

-- 1. Crear tabla meses_reportes
CREATE TABLE IF NOT EXISTS meses_reportes (
    id SERIAL PRIMARY KEY,
    mes INTEGER NOT NULL UNIQUE,
    nombre VARCHAR(20) NOT NULL,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insertar meses si la tabla está vacía
INSERT INTO meses_reportes (mes, nombre) 
SELECT mes, nombre FROM (VALUES
    (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
    (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
    (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
) AS months(mes, nombre)
WHERE NOT EXISTS (SELECT 1 FROM meses_reportes);

-- 2. Corregir tabla citas
ALTER TABLE citas ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY;
ALTER TABLE citas ADD COLUMN IF NOT EXISTS empresa_id UUID REFERENCES empresas(id);
ALTER TABLE citas ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();
ALTER TABLE citas ADD COLUMN IF NOT EXISTS activo BOOLEAN DEFAULT true;

-- 3. Corregir tabla security_logs
ALTER TABLE security_logs ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY;
ALTER TABLE security_logs ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();

-- 4. Corregir tabla archivos_reportes
ALTER TABLE archivos_reportes ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY;
ALTER TABLE archivos_reportes ADD COLUMN IF NOT EXISTS empresa_id UUID REFERENCES empresas(id);
ALTER TABLE archivos_reportes ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();
ALTER TABLE archivos_reportes ADD COLUMN IF NOT EXISTS activo BOOLEAN DEFAULT true;

-- 5. Verificación final
SELECT 'Correcciones aplicadas exitosamente' as status;
```

### **Paso 4: Ejecutar**
1. ▶️ Haz clic en **"Run"** o presiona **Ctrl+Enter**
2. ✅ Verifica que aparezca "Correcciones aplicadas exitosamente"

---

## 📋 Opción 2: CORRECCIÓN MANUAL (Paso a Paso)

### **Problema 1: Crear tabla `meses_reportes`**
```sql
CREATE TABLE meses_reportes (
    id SERIAL PRIMARY KEY,
    mes INTEGER NOT NULL UNIQUE,
    nombre VARCHAR(20) NOT NULL,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO meses_reportes (mes, nombre) VALUES
(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
(5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
(9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre');
```

### **Problema 2: Corregir tabla `citas`**
```sql
ALTER TABLE citas ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE citas ADD COLUMN empresa_id UUID REFERENCES empresas(id);
ALTER TABLE citas ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
ALTER TABLE citas ADD COLUMN activo BOOLEAN DEFAULT true;
```

### **Problema 3: Corregir tabla `security_logs`**
```sql
ALTER TABLE security_logs ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE security_logs ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
```

### **Problema 4: Corregir tabla `archivos_reportes`**
```sql
ALTER TABLE archivos_reportes ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE archivos_reportes ADD COLUMN empresa_id UUID REFERENCES empresas(id);
ALTER TABLE archivos_reportes ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
ALTER TABLE archivos_reportes ADD COLUMN activo BOOLEAN DEFAULT true;
```

---

## ✅ Verificación de Correcciones

### **En Supabase (SQL Editor):**
```sql
-- Verificar estructura de tablas críticas
SELECT table_name, column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_schema = 'public' 
  AND table_name IN ('citas', 'security_logs', 'archivos_reportes', 'meses_reportes')
ORDER BY table_name, ordinal_position;

-- Verificar datos en meses_reportes
SELECT COUNT(*) as total_meses FROM meses_reportes;
```

### **En tu Terminal (Recomendado):**
```bash
# Verificar que todo esté corregido
python check_database.py
```

**Resultado esperado:** 
- ✅ Puntuación de salud: 95-100/100
- ✅ 11/11 tablas encontradas
- ✅ 0 problemas críticos

---

## 🚨 Solución de Problemas

### **Error: "column already exists"**
**Solución:** Ignora este error, significa que la columna ya existe.

### **Error: "relation does not exist"**
**Solución:** 
1. Verifica que estés en el proyecto correcto
2. Ejecuta las correcciones en orden (crear tablas primero)

### **Error: "permission denied"**
**Solución:**
1. Verifica que tengas permisos de administrador en Supabase
2. Usa la clave de servicio si es necesario

### **Error al referenciar empresas(id)**
**Solución:**
```sql
-- Verificar tipo de dato de empresas.id
SELECT data_type FROM information_schema.columns 
WHERE table_name = 'empresas' AND column_name = 'id';

-- Si es SERIAL en lugar de UUID, usar:
ALTER TABLE citas ADD COLUMN empresa_id INTEGER REFERENCES empresas(id);
```

---

## 📊 Antes y Después

### **❌ ANTES (Problemas):**
- `citas`: Sin id, sin empresa_id
- `security_logs`: Sin id
- `archivos_reportes`: Sin id, sin empresa_id
- `meses_reportes`: No existe
- **Puntuación de salud:** 80/100

### **✅ DESPUÉS (Corregido):**
- `citas`: ✅ Con id, empresa_id, created_at, activo
- `security_logs`: ✅ Con id, created_at
- `archivos_reportes`: ✅ Con id, empresa_id, created_at, activo
- `meses_reportes`: ✅ Existe con 12 meses
- **Puntuación de salud:** 95-100/100

---

## 🎯 Próximos Pasos Después de las Correcciones

1. **✅ Verificar:** `python check_database.py`
2. **🔄 Reiniciar sistema:** `python run.py`
3. **🧪 Probar funcionalidades:** Usar los bots de Telegram
4. **📊 Monitoreo:** `python quick_db_check.py` (diario)

---

## 💡 Mejoras Opcionales (No Críticas)

Después de aplicar las correcciones críticas, considera estas mejoras:

```sql
-- Agregar columna updated_at donde falte
ALTER TABLE reportes ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
ALTER TABLE cuentas_cobrar ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
ALTER TABLE cuentas_pagar ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();

-- Crear triggers para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar triggers
CREATE TRIGGER update_empresas_updated_at 
    BEFORE UPDATE ON empresas 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

**🎉 ¡Con estas correcciones tu base de datos estará en excelente estado!**

**⏱️ Tiempo estimado:** 5-10 minutos
**🔧 Complejidad:** Fácil (copiar y pegar)
**💪 Resultado:** Base de datos robusta y segura