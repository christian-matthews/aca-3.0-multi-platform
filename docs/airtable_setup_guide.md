# 📊 Guía de Configuración de Airtable para ACA 3.0

## 🎯 Objetivo
Configurar Airtable como sistema de gestión documental para que el contador pueda subir documentos de forma organizada y sincronizarlos automáticamente con Supabase.

---

## 📋 Paso 1: Crear Cuenta y Base de Airtable

### 1.1 Crear Cuenta
1. Ve a [airtable.com](https://airtable.com)
2. Crea una cuenta gratuita
3. Confirma tu email

### 1.2 Crear Base "ACA - Gestión Documental"
1. Haz clic en "**+ Create a base**"
2. Selecciona "**Start from scratch**"
3. Nombra la base: **"ACA - Gestión Documental"**

---

## 🗂️ Paso 2: Configurar Estructura de la Tabla

### 2.1 Renombrar Tabla Principal
1. Cambia el nombre de "Table 1" a **"Documentos"**

### 2.2 Configurar Campos (Columnas)

| Campo | Tipo | Descripción | Requerido |
|-------|------|-------------|-----------|
| **Empresa** | Single select | Nombre de la empresa | ✅ Sí |
| **Fecha subida** | Date | Fecha automática | ✅ Sí |
| **Tipo documento** | Single select | Categoría del documento | ✅ Sí |
| **Archivo adjunto** | Attachment | Archivo(s) subido(s) | ✅ Sí |
| **Estado subida** | Single select | Estado del procesamiento | ✅ Sí |
| **Comentarios** | Long text | Descripción adicional | ❌ No |
| **Fecha procesado** | Date | Cuándo se procesó | ❌ No |
| **Supabase ID** | Single line text | ID de referencia | ❌ No |

#### 2.3 Configurar Opciones de "Empresa"
Agrega las empresas que manejas:
- Empresa Ejemplo 1 Ltda.
- Empresa Ejemplo 2 Ltda.
- [Agrega tus empresas reales]

#### 2.4 Configurar Opciones de "Tipo documento"
```
- Balance General
- Estado de Resultados
- Flujo de Caja
- Declaración de Renta
- Documentos Legales
- Contratos
- Escrituras
- Información Tributaria
- Carpeta Tributaria
- Otros
```

#### 2.5 Configurar Opciones de "Estado subida"
```
- Pendiente
- Procesado
- Error
```

---

## 🔑 Paso 3: Obtener API Key y Base ID

### 3.1 Obtener API Key
1. Ve a [airtable.com/account](https://airtable.com/account)
2. En la sección "API", haz clic en "**Generate API key**"
3. Copia tu API key (empieza con `key...`)

### 3.2 Obtener Base ID
1. Ve a [airtable.com/api](https://airtable.com/api)
2. Selecciona tu base "ACA - Gestión Documental"
3. En la URL verás algo como: `https://airtable.com/api/show/appXXXXXXXXXXXXXX`
4. El Base ID es la parte `appXXXXXXXXXXXXXX`

---

## ⚙️ Paso 4: Configurar Variables de Entorno

### 4.1 Actualizar archivo `.env`
Copia el archivo `env.example` a `.env` y actualiza:

```bash
# Airtable - Gestión Documental
AIRTABLE_API_KEY=keyXXXXXXXXXXXXXX
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
AIRTABLE_TABLE_NAME=Documentos
AIRTABLE_VIEW_NAME=Grid view
```

---

## 🎨 Paso 5: Configurar Vistas y Permisos

### 5.1 Crear Vista por Empresa
1. Haz clic en "**+ Create**" junto a "Views"
2. Selecciona "**Grid**"
3. Nombra: "Vista por Empresa"
4. Agrega filtro: `Empresa = [Seleccionar empresa]`

### 5.2 Crear Vista de Pendientes
1. Crear nueva vista "**Pendientes**"
2. Filtro: `Estado subida = Pendiente`
3. Ordenar por: `Fecha subida (newest first)`

### 5.3 Configurar Permisos para Contador
1. Haz clic en "**Share**" (arriba derecha)
2. Invita al contador con email
3. Selecciona nivel "**Editor**"
4. Marca "**Can only access [specific view]**" si quieres limitar acceso

---

## 📱 Paso 6: Crear Formulario de Subida

### 6.1 Crear Formulario
1. Haz clic en "**+ Create**" → "**Form**"
2. Nombra: "**Subir Documentos**"
3. Incluye campos:
   - Empresa (requerido)
   - Tipo documento (requerido)
   - Archivo adjunto (requerido)
   - Comentarios (opcional)

### 6.2 Configurar Formulario
- Ocultar campos automáticos (Fecha subida, Estado, etc.)
- Agregar descripción: "Sube documentos de la empresa de forma organizada"
- Configurar mensaje de confirmación

### 6.3 Compartir Formulario
1. Haz clic en "**Share form**"
2. Copia el enlace
3. Envía al contador para facilitar subida

---

## 🧪 Paso 7: Probar Integración

### 7.1 Verificar Conexión
```bash
cd /ruta/a/aca_3
python3 testing/airtable/test_airtable_service.py
```

### 7.2 Probar Endpoints
```bash
# Verificar estado
curl http://localhost:8000/airtable/status

# Ver registros
curl http://localhost:8000/airtable/records

# Ver estadísticas
curl http://localhost:8000/airtable/statistics
```

---

## 🔄 Paso 8: Primera Sincronización

### 8.1 Subir Documento de Prueba
1. Usa el formulario o la base directamente
2. Sube un documento con:
   - Empresa: [Una de tus empresas]
   - Tipo: "Balance General"
   - Archivo: Un PDF de prueba
   - Estado: "Pendiente" (automático)

### 8.2 Ejecutar Sincronización
```bash
# Via API
curl -X POST http://localhost:8000/sync/airtable

# O via dashboard web
# Ve a http://localhost:8000/docs
```

### 8.3 Verificar en Supabase
1. Revisa que aparezca en `reportes_mensuales` o `info_compania`
2. Verifica que se creó registro en `archivos_reportes` o `archivos_info_compania`
3. Confirma que el estado en Airtable cambió a "Procesado"

---

## 📊 Estructura Recomendada para el Contador

### Flujo de Trabajo del Contador:
1. **Recibir documentos** del cliente (email, físico, etc.)
2. **Abrir formulario de Airtable** (enlace guardado)
3. **Seleccionar empresa** y tipo de documento
4. **Subir archivo(s)** con comentarios si es necesario
5. **Enviar formulario** (automáticamente queda "Pendiente")
6. **Verificar** en vista "Pendientes" que se subió correctamente

### Organización Mensual:
- **Balances**: Subir al final de cada mes
- **Estados de Resultados**: Junto con balances
- **Declaraciones**: Según calendario tributario
- **Documentos Legales**: Cuando se generen/reciban

---

## 🚨 Solución de Problemas

### Error: "Invalid API key"
- Verifica que copiaste correctamente el API key
- Asegúrate de que empiece con `key`

### Error: "Base not found"
- Verifica el Base ID (debe empezar con `app`)
- Confirma que el nombre de tabla sea exacto

### Error: "Permission denied"
- Verifica permisos de la cuenta
- Confirma que la base sea tuya o tengas acceso

### No aparecen registros
- Verifica que la tabla se llame exactamente "Documentos"
- Confirma que haya registros en la base

---

## 🎉 ¡Listo!

Una vez configurado correctamente:

1. **El contador** puede subir documentos fácilmente via formulario
2. **La sincronización** se ejecuta automáticamente cada 30 minutos
3. **Los documentos** aparecen organizados en Supabase
4. **Los bots de Telegram** pueden mostrar la información actualizada
5. **Tú puedes monitorear** todo via dashboard web

### Próximos Pasos:
- Configurar notificaciones automáticas
- Integrar con Notion para dashboard ejecutivo
- Configurar Slack para colaboración en equipo

---

**¿Necesitas ayuda con algún paso? ¡Pregúntame! 🚀**