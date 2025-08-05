# 🔍 Scripts de Inspección de Base de Datos - ACA 3.0

## 📖 Descripción

Conjunto de scripts Python para revisar, analizar y verificar la consistencia de la base de datos Supabase del proyecto ACA 3.0.

## 🛠️ Scripts Disponibles

### 1. `check_database.py` ⚡ (RECOMENDADO)
**Script simple y rápido para verificación básica**

```bash
python check_database.py
```

**Características:**
- ✅ Verificación rápida de conectividad
- 📊 Conteo de registros por tabla
- 🎯 Análisis de consistencia básico
- 📈 Puntuación de salud (0-100)
- 💾 Reporte JSON básico
- ⏱️ Ejecución en ~10 segundos

**Ideal para:**
- Verificaciones rutinarias
- Monitoreo rápido del estado
- Primera evaluación del sistema

### 2. `database_inspector.py` 🔍 (AVANZADO)
**Inspector completo con análisis de estructura**

```bash
python database_inspector.py
```

**Características:**
- 🔍 Análisis detallado de estructura
- 🔗 Detección de relaciones
- ⚠️ Identificación de problemas de consistencia
- 💡 Recomendaciones de mejora
- 📋 Reporte completo en JSON
- 🏗️ Análisis de patrones de diseño

**Ideal para:**
- Auditorías completas
- Validación de estructura
- Análisis de calidad de datos

### 3. `database_schema_analyzer.py` 🧠 (EXPERTO)
**Analizador avanzado de esquema con SQL directo**

```bash
python database_schema_analyzer.py
```

**Características:**
- 🏗️ Análisis profundo de esquema
- 🔗 Mapeo completo de relaciones
- 🛡️ Verificación de seguridad (RLS)
- 📊 Estadísticas detalladas
- 🎯 Recomendaciones por categoría
- 📈 Métricas de calidad

**Ideal para:**
- Análisis técnico profundo
- Evaluación de arquitectura
- Planificación de mejoras

## 📊 Resultados de tu Base de Datos

### ✅ Resumen del Análisis Ejecutado

**Estado General: 💛 BUENO (80/100)**

```
📊 ESTADÍSTICAS:
   🗂️  Tablas encontradas: 10/11 (91%)
   📋 Columnas totales: 63
   📄 Registros totales: 26
   🔗 Relaciones detectadas: 6

📋 TABLAS ANALIZADAS:
   ✅ empresas          | 9 columnas  | 3 registros
   ✅ usuarios          | 10 columnas | 4 registros  
   ✅ conversaciones    | 7 columnas  | 4 registros
   ✅ reportes          | 9 columnas  | 3 registros
   ✅ pendientes        | 10 columnas | 4 registros
   ✅ cuentas_cobrar    | 9 columnas  | 4 registros
   ✅ cuentas_pagar     | 9 columnas  | 4 registros
   ⚪ citas             | Sin datos
   ⚪ security_logs     | Sin datos
   ⚪ archivos_reportes | Sin datos
   ❌ meses_reportes    | No existe
```

### 🔗 Relaciones Detectadas
```
📎 usuarios.empresa_id → empresas.id
📎 conversaciones.empresa_id → empresas.id
📎 reportes.empresa_id → empresas.id
📎 pendientes.empresa_id → empresas.id
📎 cuentas_cobrar.empresa_id → empresas.id
📎 cuentas_pagar.empresa_id → empresas.id
```

### ⚠️ Problemas Identificados

**🔴 CRÍTICOS (Requieren atención inmediata):**
- `citas`: Sin clave primaria (id)
- `citas`: Sin empresa_id para aislamiento
- `security_logs`: Sin clave primaria (id)
- `archivos_reportes`: Sin clave primaria (id)
- `archivos_reportes`: Sin empresa_id

**🟡 MEDIOS (Resolver cuando sea posible):**
- Varias tablas sin columna `activo` para soft delete
- Algunas tablas sin `created_at`

**🟢 BAJOS (Mejoras opcionales):**
- Algunas tablas sin `updated_at`

### 💡 Recomendaciones Principales

1. **🔴 CRÍTICO - Resolver problemas de estructura**
   - Agregar columnas `id` como clave primaria
   - Implementar `empresa_id` para aislamiento de datos

2. **🛡️ SEGURIDAD - Implementar RLS**
   - Configurar Row Level Security en todas las tablas
   - Crear políticas de acceso por empresa

3. **📊 OPTIMIZACIÓN - Mejorar rendimiento**
   - Crear índices en columnas `empresa_id`
   - Implementar triggers para `updated_at`

## 🚀 Cómo Usar los Scripts

### Requisitos Previos
```bash
# Activar entorno virtual
source venv/bin/activate

# Variables de entorno configuradas
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
```

### Ejecución Básica
```bash
# Verificación rápida (recomendado para uso diario)
python check_database.py

# Análisis completo (una vez por semana)
python database_inspector.py

# Análisis experto (antes de cambios importantes)
python database_schema_analyzer.py
```

### Interpretación de Resultados

**Puntuación de Salud:**
- 🟢 90-100: Excelente
- 🟡 75-89: Bueno
- 🟠 50-74: Regular
- 🔴 0-49: Crítico

**Tipos de Problemas:**
- 🔴 **Critical**: Afecta funcionamiento del sistema
- 🟡 **Medium**: Mejoras recomendadas
- 🟢 **Low**: Optimizaciones opcionales

## 📁 Archivos Generados

Cada script genera reportes en formato JSON:

```
database_check_report_YYYYMMDD_HHMMSS.json
database_inspection_report_YYYYMMDD_HHMMSS.json  
database_schema_analysis_YYYYMMDD_HHMMSS.json
```

**Contenido de los reportes:**
- 📊 Estadísticas generales
- 📋 Detalles por tabla
- 🔗 Mapeo de relaciones
- ⚠️ Lista de problemas
- 💡 Recomendaciones específicas

## 🔄 Automatización

### Verificación Programada
```bash
# Crear cron job para verificación diaria
echo "0 9 * * * cd /path/to/aca_3 && python check_database.py >> db_check.log 2>&1" | crontab -
```

### Script de Monitoreo
```bash
#!/bin/bash
# monitor_db.sh
cd /path/to/aca_3
source venv/bin/activate
python check_database.py
if [ $? -ne 0 ]; then
    echo "Database issues detected!" | mail -s "ACA 3.0 DB Alert" admin@example.com
fi
```

## 🛡️ Seguridad

**Información Sensible:**
- Los scripts **NO** muestran datos reales de usuarios
- Solo analizan estructura y metadatos
- Reportes seguros para compartir

**Permisos Requeridos:**
- Acceso de lectura a tablas públicas
- `SUPABASE_KEY` con permisos básicos
- No requiere permisos de administrador

## 📈 Mejores Prácticas

### Frecuencia de Uso
- 📅 **Diario**: `check_database.py`
- 📅 **Semanal**: `database_inspector.py`
- 📅 **Mensual**: `database_schema_analyzer.py`
- 📅 **Antes de deploys**: Todos los scripts

### Interpretación de Tendencias
```bash
# Comparar reportes a lo largo del tiempo
ls -la database_check_report_*.json | tail -5
```

### Alertas Automáticas
- Puntuación < 75: Revisar problemas medios
- Puntuación < 50: Acción inmediata requerida
- Tablas críticas vacías: Verificar configuración

## 🔧 Solución de Problemas

### Error: "Connection failed"
```bash
# Verificar variables de entorno
echo $SUPABASE_URL
echo $SUPABASE_KEY

# Probar conexión
curl -H "apikey: $SUPABASE_KEY" "$SUPABASE_URL/rest/v1/empresas?limit=1"
```

### Error: "Table not found"
```bash
# Verificar permisos en Supabase Dashboard
# Ejecutar script de setup de base de datos
python setup_database.py
```

### Error: "Import failed"
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

## 📞 Soporte

Para problemas con los scripts:
1. Verificar variables de entorno
2. Comprobar permisos en Supabase
3. Revisar logs de error
4. Consultar documentación del proyecto

---

**✅ Los scripts están listos para usar y tu base de datos está en buen estado (80/100).**

**🎯 Próximo paso recomendado:** Ejecutar `check_database.py` semanalmente para monitoreo.