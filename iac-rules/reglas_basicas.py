#!/usr/bin/env python3
"""
Reglas Básicas de IaC (B1-B5)
Implementa las reglas fundamentales para módulos Terraform según Pragma CloudOps
"""

import re
import os
from typing import Dict, Any, List

class ReglasBasicas:
    """Implementa las reglas básicas B1-B5 para módulos Terraform"""
    
    def __init__(self):
        # REGLA B1: Estructura obligatoria
        self.archivos_obligatorios_raiz = [
            ".gitignore", "CHANGELOG.md", "README.md", "data.tf", 
            "locals.tf", "main.tf", "outputs.tf", "providers.tf", "variables.tf"
        ]
        
        self.archivos_obligatorios_sample = [
            "sample/README.md", "sample/data.tf", "sample/main.tf", 
            "sample/outputs.tf", "sample/providers.tf", "sample/terraform.tfvars.sample"
        ]
        
        self.total_elementos_obligatorios = 16  # 9 archivos raíz + 1 directorio + 6 archivos sample
        
        # REGLA B3: Variables obligatorias
        self.variables_obligatorias = ["client", "project", "environment"]
        
        # REGLA B4: Etiquetas obligatorias
        self.etiquetas_transversales = [
            "environment", "project", "owner", "client", 
            "area", "provisioned", "datatype"
        ]

    def validar_estructura_modulo_completa(self, ruta_modulo: str) -> Dict[str, Any]:
        """REGLA B1: Validar estructura completa de 16 elementos obligatorios"""
        errores = []
        advertencias = []
        elementos_encontrados = 0
        
        # Verificar archivos en raíz
        for archivo in self.archivos_obligatorios_raiz:
            ruta_archivo = os.path.join(ruta_modulo, archivo)
            if os.path.exists(ruta_archivo):
                elementos_encontrados += 1
            else:
                errores.append(f"❌ Archivo obligatorio faltante: {archivo}")
        
        # Verificar directorio sample/
        sample_dir = os.path.join(ruta_modulo, "sample")
        if os.path.exists(sample_dir):
            elementos_encontrados += 1  # Contar el directorio
            
            # Verificar archivos dentro de sample/
            for archivo in self.archivos_obligatorios_sample:
                ruta_archivo = os.path.join(ruta_modulo, archivo)
                if os.path.exists(ruta_archivo):
                    elementos_encontrados += 1
                else:
                    errores.append(f"❌ Archivo sample obligatorio faltante: {archivo}")
        else:
            errores.append("❌ Directorio sample/ obligatorio faltante")
        
        # Validación numérica exacta
        if elementos_encontrados != self.total_elementos_obligatorios:
            errores.append(f"❌ Estructura incorrecta: encontrados {elementos_encontrados} elementos, requeridos {self.total_elementos_obligatorios}")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias,
            "elementos_encontrados": elementos_encontrados,
            "elementos_requeridos": self.total_elementos_obligatorios
        }

    def validar_convenciones_nomenclatura(self, contenido_locals: str, contenido_main: str) -> Dict[str, Any]:
        """REGLA B2: Validar convenciones de nomenclatura obligatorias"""
        errores = []
        advertencias = []
        
        # Verificar que locals.tf contenga resource_names
        if "resource_names" not in contenido_locals:
            errores.append("❌ locals.tf debe contener 'resource_names' con convención de nomenclatura")
        
        # Verificar patrón de nomenclatura en locals
        patron_esperado = r'\$\{var\.client\}-\$\{var\.project\}-\$\{var\.environment\}'
        if not re.search(patron_esperado, contenido_locals):
            errores.append("❌ Convención de nomenclatura no implementada: {client}-{project}-{environment}-{type}-{key}")
        
        # Verificar uso de resource_names en main.tf
        if "local.resource_names" not in contenido_main:
            advertencias.append("⚠️ main.tf no usa local.resource_names para nombres de recursos")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }

    def validar_variables_obligatorias(self, contenido_variables: str) -> Dict[str, Any]:
        """REGLA B3: Validar variables obligatorias (client, project, environment)"""
        errores = []
        advertencias = []
        variables_encontradas = []
        
        # Verificar cada variable obligatoria
        for variable in self.variables_obligatorias:
            patron = rf'variable\s+"{variable}"\s*\{{'
            if re.search(patron, contenido_variables):
                variables_encontradas.append(variable)
                
                # Verificar que tenga description
                patron_description = rf'variable\s+"{variable}"[^}}]*description\s*='
                if not re.search(patron_description, contenido_variables, re.DOTALL):
                    errores.append(f"❌ Variable '{variable}' sin description obligatorio")
                
                # Verificar validación para environment
                if variable == "environment":
                    patron_validation = rf'variable\s+"{variable}"[^}}]*validation\s*\{{'
                    if not re.search(patron_validation, contenido_variables, re.DOTALL):
                        errores.append("❌ Variable 'environment' debe tener validación con valores permitidos")
            else:
                errores.append(f"❌ Variable obligatoria faltante: {variable}")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias,
            "variables_encontradas": variables_encontradas
        }

    def validar_sistema_etiquetado(self, contenido_providers: str, contenido_main: str) -> Dict[str, Any]:
        """REGLA B4: Validar sistema de etiquetado de 2 niveles"""
        errores = []
        advertencias = []
        
        # Verificar default_tags en provider (debe estar en el consumidor, no en el módulo)
        if "default_tags" in contenido_providers:
            advertencias.append("⚠️ default_tags debe estar en el provider del consumidor, no en el módulo")
        
        # Verificar estructura de tags en recursos
        if "tags = merge(" not in contenido_main:
            errores.append("❌ Recursos deben usar merge() para combinar tags")
        
        # Verificar que se use Name tag
        if '"Name"' not in contenido_main:
            errores.append("❌ Recursos deben incluir tag 'Name' con convención de nomenclatura")
        
        # Verificar additional_tags en variables
        if "additional_tags" not in contenido_main:
            advertencias.append("⚠️ Considerar agregar soporte para additional_tags específicos por recurso")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }

    def validar_sample_funcional(self, ruta_sample: str) -> Dict[str, Any]:
        """REGLA B5: Validar que sample/ sea completamente funcional"""
        errores = []
        advertencias = []
        
        # Verificar terraform.tfvars.sample
        tfvars_path = os.path.join(ruta_sample, "terraform.tfvars.sample")
        if os.path.exists(tfvars_path):
            try:
                with open(tfvars_path, 'r') as f:
                    contenido = f.read()
                    
                # Verificar variables obligatorias en el ejemplo
                for variable in self.variables_obligatorias:
                    if variable not in contenido:
                        errores.append(f"❌ terraform.tfvars.sample falta variable: {variable}")
                
                # Verificar que no use placeholders
                if "[" in contenido and "]" in contenido:
                    advertencias.append("⚠️ terraform.tfvars.sample contiene placeholders, debe tener valores reales")
                    
            except Exception as e:
                errores.append(f"❌ Error leyendo terraform.tfvars.sample: {str(e)}")
        else:
            errores.append("❌ terraform.tfvars.sample faltante")
        
        # Verificar README.md del sample
        readme_sample = os.path.join(ruta_sample, "README.md")
        if not os.path.exists(readme_sample):
            errores.append("❌ sample/README.md faltante")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }
