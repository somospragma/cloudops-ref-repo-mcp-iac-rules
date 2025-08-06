# MCP CloudOps - Reglas IaC Completas

Un servidor MCP (Model Context Protocol) avanzado construido con Flask, especializado en validación y generación de Infrastructure as Code (IaC) con Terraform según las reglas de Pragma CloudOps.

## 🚀 Características Principales

### 🏗️ Reglas Básicas (B1-B5)
- **Estructura de 16 elementos obligatorios**: Validación exacta de archivos y directorios
- **Convenciones de nomenclatura**: `{client}-{project}-{environment}-{type}-{key}`
- **Variables obligatorias**: client, project, environment con validaciones
- **Sistema de etiquetado de 2 niveles**: default_tags + Name + additional_tags
- **Directorio sample/ funcional**: Ejemplos completamente funcionales

### ⚙️ Reglas Avanzadas (A1-A7)
- **Tipos de datos inteligentes**: map(object()), list(object()), map(string), list(string)
- **for_each obligatorio**: Nunca usar count para recursos múltiples
- **Validaciones de variables**: Validaciones críticas con contains(), regex()
- **Transformaciones simples en locals**: Máximo 2 niveles, sin flatten() complejo
- **Outputs descriptivos**: Descriptions obligatorios y estructura correcta

### 🔒 Reglas de Seguridad (S1-S6)
- **Cifrado obligatorio**: Habilitado por defecto en todos los recursos
- **Acceso público bloqueado**: Configuración segura por defecto
- **Force SSL/TLS**: Conexiones seguras obligatorias
- **Políticas de menor privilegio**: Estructura dinámica de políticas
- **Logging y monitoreo**: Auditoría completa habilitada

### 📄 Reglas de Documentación (D1-D7)
- **README.md con 12 secciones obligatorias**: Estructura completa y ordenada
- **CHANGELOG.md**: Formato Keep a Changelog con Semantic Versioning
- **sample/README.md**: Documentación completa de ejemplos
- **terraform-docs**: Configuración automática y generación
- **Descriptions obligatorios**: En variables y outputs

## 📁 Estructura del Proyecto

```
mcp-flask-server/
├── venv/                           # Entorno virtual de Python
├── reglas/                         # Archivos de reglas originales
│   ├── terraform_rules_basicas_final.md
│   ├── terraform_rules_avanzadas_final.md
│   ├── terraform_rules_seguridad_final.md
│   ├── terraform_rules_documentacion_final.md
│   └── terraform_prompt_maestro_final.md
├── reglas_personalizadas.py       # Implementación completa de reglas IaC
├── mcp_stdio_server.py            # Servidor MCP principal con todas las herramientas
├── mcp_server.py                  # Servidor HTTP (versión original)
├── test_iac_mcp.py               # Script de pruebas para funcionalidades IaC
├── test_mcp.py                   # Script de pruebas básicas
├── requirements.txt              # Dependencias de Python
└── README.md                     # Esta documentación
```

## 🛠️ Instalación y Configuración

### 1. Preparar el entorno
```bash
cd /Users/cristian.noguera/mcp-flask-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar Amazon Q CLI
Agregar a `/Users/cristian.noguera/.aws/amazonq/mcp.json`:
```json
{
  "mcpServers": {
    "mcp-cloudops": {
      "command": "/Users/cristian.noguera/mcp-flask-server/venv/bin/python",
      "args": ["/Users/cristian.noguera/mcp-flask-server/mcp_stdio_server.py"],
      "env": {
        "PYTHONPATH": "/Users/cristian.noguera/mcp-flask-server"
      }
    }
  }
}
```

### 3. Reiniciar Amazon Q CLI
```bash
# Cerrar Q CLI actual y reiniciar
q chat
```

## 🔧 Herramientas Disponibles

### 🏗️ Reglas Básicas

#### `validar_estructura_modulo`
Valida que el módulo tenga exactamente 16 elementos obligatorios.
```
Valida la estructura de mi módulo Terraform en /ruta/al/modulo
```

#### `validar_variables_obligatorias`
Verifica que estén presentes client, project, environment con descriptions.
```
Valida las variables obligatorias de mi archivo variables.tf
```

#### `validar_convenciones_nomenclatura`
Verifica el patrón {client}-{project}-{environment}-{type}-{key}.
```
Valida las convenciones de nomenclatura en mi módulo
```

### ⚙️ Reglas Avanzadas

#### `validar_tipos_datos`
Valida el uso correcto de map(object()), list(object()), etc.
```
Valida los tipos de datos en mis variables de Terraform
```

#### `validar_for_each`
Verifica que se use for_each en lugar de count.
```
Valida el uso de for_each en mi archivo main.tf
```

#### `validar_transformaciones_locals`
Verifica que las transformaciones en locals sean simples.
```
Valida las transformaciones en mi archivo locals.tf
```

### 🔒 Reglas de Seguridad

#### `validar_cifrado_obligatorio`
Verifica que el cifrado esté habilitado por defecto.
```
Valida que el cifrado esté configurado correctamente en mi módulo
```

#### `validar_acceso_publico`
Verifica que el acceso público esté bloqueado.
```
Valida la configuración de acceso público en mi módulo S3
```

#### `validar_force_ssl`
Verifica que SSL/TLS esté forzado.
```
Valida la configuración SSL/TLS en mi módulo
```

### 📄 Reglas de Documentación

#### `validar_readme_estructura`
Valida las 12 secciones obligatorias del README.md.
```
Valida la estructura de mi README.md de Terraform
```

#### `validar_changelog`
Valida el formato Keep a Changelog.
```
Valida mi archivo CHANGELOG.md
```

### 🛠️ Herramientas de Generación

#### `generar_plantilla_readme`
Genera README.md completo según todas las reglas.
```
Genera una plantilla README para mi módulo S3 llamado "terraform-s3-bucket"
```

#### `generar_plantilla_changelog`
Genera CHANGELOG.md con formato estándar.
```
Genera una plantilla CHANGELOG para mi módulo
```

#### `generar_config_terraform_docs`
Genera configuración .terraform-docs.yml.
```
Genera la configuración de terraform-docs para mi módulo
```

### 📊 Reporte Completo

#### `generar_reporte_completo`
Ejecuta todas las validaciones y genera reporte detallado.
```
Genera un reporte completo de validación IaC para mi módulo en /ruta/modulo
```

## 🧪 Pruebas

### Ejecutar pruebas de funcionalidad
```bash
python3 test_iac_mcp.py
```

### Probar herramientas específicas con Amazon Q CLI
```
# Ejemplos de comandos para Amazon Q CLI:

# Validación básica
"Valida la estructura de mi módulo Terraform en /Users/cristian/mi-modulo"

# Validación de seguridad  
"Verifica que el cifrado esté configurado en mi módulo S3"

# Generación de plantillas
"Genera una plantilla README completa para mi módulo Lambda"

# Reporte completo
"Crea un reporte de validación IaC completo para mi módulo"
```

## 📋 Casos de Uso Principales

### 1. **Validación de Módulos Existentes**
- Verificar que módulos cumplan con todas las reglas
- Identificar problemas de estructura, seguridad y documentación
- Generar reportes de cumplimiento

### 2. **Creación de Nuevos Módulos**
- Generar plantillas completas de documentación
- Aplicar configuraciones de seguridad por defecto
- Seguir convenciones de nomenclatura estándar

### 3. **Auditoría y Cumplimiento**
- Reportes detallados de validación
- Verificación de configuraciones de seguridad
- Documentación automática actualizada

### 4. **Desarrollo y Mantenimiento**
- Validación continua durante desarrollo
- Generación automática de documentación
- Aplicación consistente de mejores prácticas

## 🔍 Troubleshooting

### Problema: "Herramienta no encontrada"
- Verificar que Amazon Q CLI esté reiniciado
- Confirmar configuración en mcp.json
- Verificar que el servidor esté ejecutándose

### Problema: "Error leyendo archivo"
- Verificar rutas absolutas en argumentos
- Confirmar permisos de lectura en archivos
- Verificar que los archivos existan

### Problema: "Validación fallida"
- Revisar errores específicos en el reporte
- Aplicar correcciones según las reglas
- Re-ejecutar validación después de cambios

## 🚀 Próximas Mejoras

- [ ] Integración con Checkov para validación de seguridad
- [ ] Soporte para múltiples providers (Azure, GCP)
- [ ] Validación de políticas IAM específicas
- [ ] Generación automática de diagramas de arquitectura
- [ ] Integración con CI/CD pipelines
- [ ] Métricas de calidad de código IaC

## 📞 Soporte

Para soporte técnico o preguntas sobre las reglas IaC:
- Revisar documentación en directorio `reglas/`
- Ejecutar `generar_reporte_completo` para diagnóstico
- Usar herramientas específicas para validaciones puntuales

---

**Versión:** 2.0.0 - Reglas IaC Completas  
**Última actualización:** Agosto 2025  
**Compatibilidad:** Amazon Q CLI, Terraform >= 1.0, AWS Provider >= 5.0
