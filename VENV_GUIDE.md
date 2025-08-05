# 🐍 Guía del Entorno Virtual - ACA 3.0

## ¿Qué es un entorno virtual?

Un entorno virtual es un espacio aislado donde puedes instalar paquetes Python específicos para tu proyecto sin afectar el sistema global.

## 🚀 Activación Rápida

### Opción 1: Script automático
```bash
./activate.sh
```

### Opción 2: Activación manual
```bash
source venv/bin/activate
```

## 📋 Comandos Útiles

### Activar entorno virtual
```bash
source venv/bin/activate
```

### Desactivar entorno virtual
```bash
deactivate
```

### Verificar que está activado
```bash
which python
# Debería mostrar: /path/to/aca_3/venv/bin/python
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar la aplicación
```bash
python run.py
```

### Ejecutar directamente
```bash
python -m app.main
```

## 🔧 Configuración en Nuevos Terminales

### Para cada nuevo terminal:

1. **Navegar al proyecto:**
   ```bash
   cd /path/to/aca_3
   ```

2. **Activar entorno virtual:**
   ```bash
   source venv/bin/activate
   ```

3. **Verificar activación:**
   ```bash
   which python
   # Debería mostrar la ruta del venv
   ```

4. **Ejecutar aplicación:**
   ```bash
   python run.py
   ```

## 📁 Estructura del Entorno Virtual

```
aca_3/
├── venv/                    # Entorno virtual
│   ├── bin/                 # Ejecutables
│   ├── lib/                 # Librerías
│   └── pyvenv.cfg          # Configuración
├── activate.sh              # Script de activación
├── requirements.txt         # Dependencias
└── .env                    # Variables de entorno
```

## ⚠️ Notas Importantes

- **Siempre activa el entorno virtual** antes de trabajar en el proyecto
- **No committees el directorio `venv/`** al repositorio
- **Usa `pip` dentro del entorno virtual** para instalar paquetes
- **El archivo `.env`** debe configurarse con tus credenciales

## 🐛 Troubleshooting

### Error: "venv/bin/activate: No such file or directory"
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "Permission denied"
```bash
chmod +x activate.sh
```

## 🎯 Flujo de Trabajo Recomendado

1. **Abrir nuevo terminal**
2. **Navegar al proyecto:** `cd /path/to/aca_3`
3. **Activar entorno:** `source venv/bin/activate`
4. **Configurar variables:** Editar `.env`
5. **Ejecutar aplicación:** `python run.py`
6. **Desactivar al terminar:** `deactivate`

## 📚 Recursos Adicionales

- [Documentación de venv](https://docs.python.org/3/library/venv.html)
- [Guía de pip](https://pip.pypa.io/en/stable/)
- [Variables de entorno](docs/variables.md) 