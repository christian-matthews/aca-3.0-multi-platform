# 🧪 TESTING - ACA 3.0

Esta carpeta contiene todos los archivos de testing, verificación y scripts temporales del proyecto ACA 3.0.

## 📁 **Estructura de Carpetas**

### **🗄️ `/database/`**
Scripts de inspección, análisis y setup de base de datos:
- `check_database.py` - Verificación general de BD
- `database_inspector.py` - Inspector detallado de estructura
- `database_schema_analyzer.py` - Análisis completo de esquema
- `inspect_supabase_complete.py` - Inspección completa Supabase
- `setup_database.sql` - Script inicial de BD
- `setup_reportes_database.py` - Setup tablas de reportes
- `reset_database.py` - Reset completo de BD
- `verify_database.sql` - Verificación de estructura
- `DATABASE_INSPECTION_README.md` - Guía de inspección

### **🔒 `/security/`**
Scripts de corrección y verificación de seguridad:
- `fix_security_critical.py` - Script corrección automática
- `fix_security_manual.sql` - SQL corrección manual  
- `verify_security_fix.py` - Verificación corrección
- `fix_critical_*.sql` - Scripts de correcciones críticas
- `fix_critical_issues.py` - Corrector automático de issues
- `GUIA_CORRECCIONES_CRITICAS.md` - Guía de correcciones

### **🧪 `/system/`**
Scripts de testing del sistema completo:
- `test_admin.py` - Testing bot administración
- `test_bots.py` - Testing bots Telegram
- `test_database.py` - Testing conexión BD
- `test_system.py` - Testing sistema completo
- `validate_supabase.py` - Validación Supabase
- `verify_fixes.py` - Verificación de fixes
- `quick_test.py` - Tests rápidos

### **📊 `/reports/`**
Reportes JSON generados por scripts de análisis:
- `database_check_report_*.json` - Reportes de verificación BD
- `database_schema_analysis_*.json` - Análisis de esquema
- `database_inspection_*.json` - Reportes de inspección
- `supabase_inspection_*.json` - Inspecciones Supabase

### **📝 `/scripts/`**
Scripts auxiliares y guías:
- `VENV_GUIDE.md` - Guía de entorno virtual
- Otros scripts de utilidad

---

## 📋 **Propósito**

**Esta carpeta mantiene el proyecto principal limpio** separando:
- ✅ Código de testing y verificación
- ✅ Reportes temporales de análisis  
- ✅ Scripts de corrección de problemas
- ✅ Documentación técnica de testing

## ⚠️ **Nota Importante**

Los archivos en esta carpeta son **para desarrollo y testing**. 
El código de producción está en:
- `/app/` - Aplicación principal
- `/docs/` - Documentación del proyecto
- `run.py` - Script principal de ejecución
- `requirements.txt` - Dependencias
- `env.example` - Variables de entorno

---

**📅 Última organización**: 2025-08-05