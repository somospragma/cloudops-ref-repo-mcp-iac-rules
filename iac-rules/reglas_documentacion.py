#!/usr/bin/env python3
"""
Reglas de Documentación de IaC (D1-D7)
Implementa estándares de documentación obligatorios según Pragma CloudOps
"""

import re
import os
import datetime
from typing import Dict, Any, List

class ReglasDocumentacion:
    """Implementa las reglas de documentación D1-D7 para módulos Terraform"""
    
    def __init__(self):
        # REGLA D1: Secciones README obligatorias
        self.secciones_readme_obligatorias = [
            "# Módulo Terraform:",
            "## Descripción",
            "## Diagrama de Arquitectura", 
            "## Características",
            "## Estructura del Módulo",
            "## Implementación y Configuración",
            "## Parámetros de Entrada",
            "## Estructura de Configuración",
            "## Valores de Salida",
            "## Ejemplos de Uso",
            "## Consideraciones de Seguridad",
            "## Contribución"
        ]

    def validar_readme_estructura_completa(self, contenido_readme: str) -> Dict[str, Any]:
        """REGLA D1: Validar estructura obligatoria completa del README.md"""
        errores = []
        advertencias = []
        secciones_encontradas = []
        
        for seccion in self.secciones_readme_obligatorias:
            if seccion in contenido_readme:
                secciones_encontradas.append(seccion)
            else:
                errores.append(f"❌ Sección obligatoria faltante en README.md: {seccion}")
        
        # Verificar orden de secciones
        posiciones = []
        for seccion in secciones_encontradas:
            pos = contenido_readme.find(seccion)
            if pos != -1:
                posiciones.append((pos, seccion))
        
        posiciones.sort()
        orden_actual = [seccion for _, seccion in posiciones]
        
        if orden_actual != [s for s in self.secciones_readme_obligatorias if s in secciones_encontradas]:
            errores.append("❌ Las secciones del README.md no están en el orden correcto")
        
        # Verificar elementos específicos obligatorios
        elementos_obligatorios = [
            "## Requisitos Técnicos",
            "| Requisito | Versión |",
            "### Configuración del Provider",
            "### Convenciones de Nomenclatura",
            "## Consideraciones de Seguridad"
        ]
        
        for elemento in elementos_obligatorios:
            if elemento not in contenido_readme:
                errores.append(f"❌ Elemento obligatorio faltante: {elemento}")
        
        # Verificar que tenga ejemplos funcionales
        if "### Ejemplo Básico" not in contenido_readme:
            errores.append("❌ README debe incluir 'Ejemplo Básico'")
        
        if "### Ejemplo Avanzado" not in contenido_readme:
            errores.append("❌ README debe incluir 'Ejemplo Avanzado'")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias,
            "secciones_encontradas": len(secciones_encontradas),
            "secciones_requeridas": len(self.secciones_readme_obligatorias)
        }

    def validar_changelog_formato_completo(self, contenido_changelog: str) -> Dict[str, Any]:
        """REGLA D2: Validar formato completo obligatorio del CHANGELOG.md"""
        errores = []
        advertencias = []
        
        elementos_obligatorios = [
            "# Changelog",
            "[Keep a Changelog]",
            "[Semantic Versioning]",
            "## [Unreleased]",
            "### Added",
            "### Changed", 
            "### Deprecated",
            "### Removed",
            "### Fixed",
            "### Security"
        ]
        
        for elemento in elementos_obligatorios:
            if elemento not in contenido_changelog:
                errores.append(f"❌ Elemento obligatorio faltante en CHANGELOG.md: {elemento}")
        
        # Verificar formato de versiones
        patron_version = r"\[(\d+\.\d+\.\d+)\] - \d{4}-\d{2}-\d{2}"
        versiones = re.findall(patron_version, contenido_changelog)
        
        if not versiones:
            errores.append("❌ No se encontraron versiones con formato correcto [X.Y.Z] - YYYY-MM-DD")
        
        # Verificar que tenga contenido en secciones
        if "- N/A" in contenido_changelog:
            advertencias.append("⚠️ Algunas secciones contienen 'N/A', considerar agregar contenido específico")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias,
            "versiones_encontradas": versiones
        }

    def validar_sample_readme(self, contenido_sample_readme: str) -> Dict[str, Any]:
        """REGLA D3: Validar documentación del directorio sample/"""
        errores = []
        advertencias = []
        
        elementos_obligatorios_sample = [
            "# Ejemplo de Uso",
            "## Descripción",
            "## Estructura",
            "## Uso Rápido",
            "### 1. Preparación",
            "### 2. Despliegue",
            "### 3. Verificación",
            "### 4. Limpieza"
        ]
        
        for elemento in elementos_obligatorios_sample:
            if elemento not in contenido_sample_readme:
                errores.append(f"❌ Elemento obligatorio faltante en sample/README.md: {elemento}")
        
        # Verificar que tenga comandos terraform
        comandos_terraform = ["terraform init", "terraform plan", "terraform apply", "terraform destroy"]
        for comando in comandos_terraform:
            if comando not in contenido_sample_readme:
                errores.append(f"❌ sample/README.md debe incluir comando: {comando}")
        
        # Verificar que mencione terraform.tfvars.sample
        if "terraform.tfvars.sample" not in contenido_sample_readme:
            errores.append("❌ sample/README.md debe mencionar terraform.tfvars.sample")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }

    def validar_terraform_docs_configuracion(self, ruta_modulo: str) -> Dict[str, Any]:
        """REGLA D4: Validar configuración de terraform-docs"""
        errores = []
        advertencias = []
        
        # Verificar archivo .terraform-docs.yml
        terraform_docs_path = os.path.join(ruta_modulo, ".terraform-docs.yml")
        if not os.path.exists(terraform_docs_path):
            errores.append("❌ Archivo .terraform-docs.yml faltante")
        else:
            try:
                with open(terraform_docs_path, 'r') as f:
                    contenido = f.read()
                    
                elementos_requeridos = [
                    'formatter: "markdown table"',
                    'output:',
                    'file: "README.md"',
                    'mode: inject',
                    'sort:',
                    'enabled: true'
                ]
                
                for elemento in elementos_requeridos:
                    if elemento not in contenido:
                        errores.append(f"❌ Configuración terraform-docs faltante: {elemento}")
                
                # Verificar template con BEGIN_TF_DOCS
                if "BEGIN_TF_DOCS" not in contenido:
                    errores.append("❌ Template debe incluir marcadores BEGIN_TF_DOCS/END_TF_DOCS")
                        
            except Exception as e:
                errores.append(f"❌ Error leyendo .terraform-docs.yml: {str(e)}")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }

    def validar_descriptions_obligatorios(self, contenido_variables: str, contenido_outputs: str) -> Dict[str, Any]:
        """REGLA D4: Validar descriptions obligatorios en variables y outputs"""
        errores = []
        advertencias = []
        
        # Validar descriptions en variables
        patron_variables = r'variable\s+"([^"]+)"\s*\{'
        variables = re.findall(patron_variables, contenido_variables)
        
        for variable in variables:
            patron_description = rf'variable\s+"{variable}"[^}}]*description\s*='
            if not re.search(patron_description, contenido_variables, re.DOTALL):
                errores.append(f"❌ Variable '{variable}' sin description obligatorio")
        
        # Validar descriptions en outputs
        patron_outputs = r'output\s+"([^"]+)"\s*\{'
        outputs = re.findall(patron_outputs, contenido_outputs)
        
        for output in outputs:
            patron_description = rf'output\s+"{output}"[^}}]*description\s*='
            if not re.search(patron_description, contenido_outputs, re.DOTALL):
                errores.append(f"❌ Output '{output}' sin description obligatorio")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias,
            "variables_analizadas": len(variables),
            "outputs_analizados": len(outputs)
        }

    # ========== FUNCIONES DE GENERACIÓN DE PLANTILLAS ==========
    
    def obtener_plantilla_readme_completa(self, nombre_modulo: str, tipo_recurso: str = "recurso") -> str:
        """Generar plantilla completa de README.md según todas las reglas"""
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        
        return f"""# Módulo Terraform: {nombre_modulo}

## Descripción
[Descripción concisa del propósito del módulo, características clave y casos de uso principales]

## Diagrama de Arquitectura
![Arquitectura](docs/architecture.png)

## Características
- ✅ [Característica principal 1]
- ✅ [Característica principal 2]
- ✅ [Característica principal 3]
- ✅ [Característica principal 4]

## Estructura del Módulo
```
{nombre_modulo}/
├── .gitignore               # Archivos a ignorar
├── CHANGELOG.md             # Historial de cambios
├── README.md                # Documentación principal
├── data.tf                  # Recursos de datos
├── locals.tf                # Variables locales y transformaciones
├── main.tf                  # Recursos principales
├── outputs.tf               # Salidas del módulo
├── providers.tf             # Configuración de providers
├── variables.tf             # Variables de entrada
└── sample/                  # Directorio ejemplo
    ├── README.md            # Documentación ejemplo
    ├── data.tf              # Datos del ejemplo
    ├── main.tf              # Configuración ejemplo
    ├── outputs.tf           # Salidas ejemplo
    ├── providers.tf         # Providers ejemplo
    └── terraform.tfvars.sample # Variables ejemplo
```

## Implementación y Configuración

### Requisitos Técnicos
| Requisito | Versión |
|-----------|---------|
| Terraform | >= 1.0 |
| AWS Provider | >= 5.0 |

### Configuración del Provider
```hcl
provider "aws" {{
  region = "us-east-1"
  
  default_tags {{
    tags = {{
      environment = var.environment
      project     = var.project
      owner       = "cloudops"
      client      = var.client
      area        = "infrastructure"
      provisioned = "terraform"
      datatype    = "operational"
    }}
  }}
}}
```

### Convenciones de Nomenclatura
```
{{client}}-{{project}}-{{environment}}-{{resource_type}}-{{identifier}}
```

**Ejemplos:**
- `pragma-webapp-dev-{tipo_recurso}-uploads`
- `pragma-api-prod-{tipo_recurso}-encryption`

## Parámetros de Entrada

### Variables Obligatorias
| Nombre | Descripción | Tipo | Requerido | Validación |
|--------|-------------|------|-----------|------------|
| client | Nombre del cliente | string | ✅ | Alfanumérico, 3-20 chars |
| project | Nombre del proyecto | string | ✅ | Alfanumérico, 3-30 chars |
| environment | Entorno (dev/staging/prod) | string | ✅ | Valores permitidos |

### Variables de Configuración
| Nombre | Descripción | Tipo | Requerido | Default |
|--------|-------------|------|-----------|---------|
| {tipo_recurso}_config | Configuración de {tipo_recurso} | map(object()) | ✅ | - |

## Estructura de Configuración

### Configuración Principal
```hcl
{tipo_recurso}_config = {{
  "nombre_instancia" = {{
    # Configuración específica del recurso
    encryption_enabled = true
    block_public_access = true
    
    # Etiquetas adicionales específicas
    additional_tags = {{
      "custom_tag" = "custom_value"
    }}
  }}
}}
```

## Valores de Salida
| Nombre | Descripción | Tipo |
|--------|-------------|------|
| {tipo_recurso}_ids | IDs de recursos creados | map(string) |
| {tipo_recurso}_arns | ARNs de recursos creados | map(string) |

## Ejemplos de Uso

### Ejemplo Básico
```hcl
module "{nombre_modulo}" {{
  source = "git::https://github.com/somospragma/[repositorio].git?ref=v1.0.0"
  
  client      = "pragma"
  project     = "webapp"
  environment = "dev"
  
  {tipo_recurso}_config = {{
    "primary" = {{
      # Configuración mínima
    }}
  }}
}}
```

### Ejemplo Avanzado
```hcl
module "{nombre_modulo}" {{
  source = "git::https://github.com/somospragma/[repositorio].git?ref=v1.0.0"
  
  client      = "pragma"
  project     = "webapp"
  environment = "prod"
  
  {tipo_recurso}_config = {{
    "primary" = {{
      # Configuración completa con todas las opciones
      encryption_enabled = true
      block_public_access = true
      force_ssl = true
    }},
    "secondary" = {{
      # Segunda instancia con configuración diferente
    }}
  }}
}}
```

## Consideraciones de Seguridad
- ✅ Cifrado habilitado por defecto
- ✅ Acceso público bloqueado por defecto
- ✅ Conexiones SSL/TLS obligatorias
- ✅ Políticas de menor privilegio
- ✅ Logging y auditoría habilitados

## Contribución
Este módulo sigue las convenciones de Pragma CloudOps. Para contribuir:
1. Fork del repositorio
2. Crear rama feature/
3. Seguir las reglas de commit conventional
4. Abrir Pull Request

## Licencia
[Especificar licencia]

## Soporte
Para soporte técnico, contactar al equipo CloudOps de Pragma.

<!-- BEGIN_TF_DOCS -->
<!-- END_TF_DOCS -->
"""

    def obtener_plantilla_changelog_completa(self) -> str:
        """Generar plantilla completa de CHANGELOG.md"""
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        
        return f"""# Changelog

Todos los cambios notables a este módulo serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - {fecha_actual}
### Added
- Implementación inicial del módulo
- Configuración de [recurso principal]
- Ejemplos de uso básico y avanzado
- Documentación completa
- Configuraciones de seguridad por defecto

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- Cifrado habilitado por defecto
- Bloqueo de acceso público implementado
- Force SSL/TLS configurado
- Políticas de menor privilegio aplicadas
"""

    def obtener_configuracion_terraform_docs(self) -> str:
        """Generar configuración completa de .terraform-docs.yml"""
        return '''formatter: "markdown table"

output:
  file: "README.md"
  mode: inject
  template: |-
    <!-- BEGIN_TF_DOCS -->
    {{ .Content }}
    <!-- END_TF_DOCS -->

sort:
  enabled: true
  by: name

settings:
  anchor: true
  color: true
  default: true
  description: true
  escape: true
  hide-empty: false
  html: true
  indent: 2
  lockfile: true
  read-comments: true
  required: true
  sensitive: true
  type: true
'''

    def obtener_plantilla_sample_readme(self, nombre_modulo: str) -> str:
        """Generar plantilla de sample/README.md"""
        return f"""# Ejemplo de Uso - {nombre_modulo}

## Descripción
Este directorio contiene un ejemplo funcional completo del módulo {nombre_modulo}.

## Estructura
```
sample/
├── README.md                # Esta documentación
├── data.tf                  # Fuentes de datos necesarias
├── main.tf                  # Configuración principal del ejemplo
├── outputs.tf               # Salidas del ejemplo
├── providers.tf             # Configuración de providers
└── terraform.tfvars.sample  # Variables de ejemplo
```

## Uso Rápido

### 1. Preparación
```bash
# Copiar variables de ejemplo
cp terraform.tfvars.sample terraform.tfvars

# Editar variables según tu entorno
vim terraform.tfvars
```

### 2. Despliegue
```bash
terraform init
terraform plan
terraform apply
```

### 3. Verificación
```bash
terraform output
```

### 4. Limpieza
```bash
terraform destroy
```

## Variables de Ejemplo

### Configuración Mínima
Para un entorno de desarrollo básico, usa:
```hcl
client      = "ejemplo-client"
project     = "ejemplo-project"
environment = "dev"

resource_config = {{
  "development" = {{
    # Configuración mínima para desarrollo
  }}
}}
```

### Configuración Completa
Para un entorno de producción, usa:
```hcl
client      = "pragma"
project     = "webapp"
environment = "prod"

resource_config = {{
  "production" = {{
    # Configuración completa con todas las características
  }}
}}
```

## Consideraciones
- Este ejemplo es **completamente funcional** y puede desplegarse sin modificaciones
- Todos los recursos creados tienen nombres únicos usando la convención establecida
- Las configuraciones de seguridad están habilitadas por defecto
"""
