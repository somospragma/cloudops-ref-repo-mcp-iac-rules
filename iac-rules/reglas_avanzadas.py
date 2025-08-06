#!/usr/bin/env python3
"""
Reglas Avanzadas de IaC (A1-A7)
Implementa técnicas avanzadas de Terraform según Pragma CloudOps
"""

import re
from typing import Dict, Any, List

class ReglasAvanzadas:
    """Implementa las reglas avanzadas A1-A7 para módulos Terraform"""
    
    def __init__(self):
        # REGLA A1: Tipos de datos inteligentes
        self.tipos_datos_permitidos = {
            "multiples_recursos": "map(object())",
            "configuraciones_anidadas": "list(object())",
            "pares_clave_valor": "map(string)",
            "arrays_simples": "list(string)"
        }

    def validar_tipos_datos_inteligentes(self, contenido_variables: str) -> Dict[str, Any]:
        """REGLA A1: Validar uso correcto de tipos de datos inteligentes"""
        errores = []
        advertencias = []
        
        # Buscar definiciones de variables con tipos complejos
        patron_variables = r'variable\s+"([^"]+)"\s*\{[^}]*type\s*=\s*([^}]+)\}'
        variables_tipos = re.findall(patron_variables, contenido_variables, re.DOTALL)
        
        for nombre_var, tipo in variables_tipos:
            tipo_limpio = re.sub(r'\s+', ' ', tipo.strip())
            
            # Verificar uso correcto de map(object()) para recursos múltiples
            if "_config" in nombre_var and "map(object(" not in tipo_limpio:
                errores.append(f"❌ Variable '{nombre_var}' debe usar map(object()) para recursos múltiples")
            
            # Verificar uso correcto de list(object()) para configuraciones anidadas
            if "rules" in nombre_var and "list(object(" not in tipo_limpio:
                advertencias.append(f"⚠️ Variable '{nombre_var}' podría necesitar list(object()) para configuraciones múltiples")
            
            # Verificar uso correcto de map(string) para tags
            if "tags" in nombre_var and tipo_limpio != "map(string)":
                advertencias.append(f"⚠️ Variable '{nombre_var}' debería usar map(string) para tags")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias,
            "variables_analizadas": len(variables_tipos)
        }

    def validar_for_each_obligatorio(self, contenido_main: str) -> Dict[str, Any]:
        """REGLA A2: Validar uso obligatorio de for_each (nunca count)"""
        errores = []
        advertencias = []
        
        # Buscar uso de count (prohibido)
        if re.search(r'\bcount\s*=', contenido_main):
            errores.append("❌ Uso de 'count' prohibido, debe usar 'for_each' para recursos múltiples")
        
        # Buscar recursos que deberían usar for_each
        patron_recursos = r'resource\s+"([^"]+)"\s+"([^"]+)"\s*\{'
        recursos = re.findall(patron_recursos, contenido_main)
        
        recursos_sin_for_each = []
        for tipo_recurso, nombre_recurso in recursos:
            # Buscar el bloque completo del recurso
            patron_bloque = rf'resource\s+"{tipo_recurso}"\s+"{nombre_recurso}"\s*\{{[^}}]*\}}'
            bloque = re.search(patron_bloque, contenido_main, re.DOTALL)
            
            if bloque and "for_each" not in bloque.group():
                # Si el recurso no tiene for_each, podría necesitarlo
                if "var." in bloque.group() and "_config" in bloque.group():
                    recursos_sin_for_each.append(f"{tipo_recurso}.{nombre_recurso}")
        
        if recursos_sin_for_each:
            advertencias.extend([f"⚠️ Recurso podría necesitar for_each: {recurso}" for recurso in recursos_sin_for_each])
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias,
            "recursos_analizados": len(recursos)
        }

    def validar_validaciones_variables(self, contenido_variables: str) -> Dict[str, Any]:
        """REGLA A3: Validar que variables críticas tengan validaciones"""
        errores = []
        advertencias = []
        
        # Variables que DEBEN tener validación
        variables_criticas = ["environment", "client", "project"]
        
        for variable in variables_criticas:
            patron_variable = rf'variable\s+"{variable}"\s*\{{([^}}]*)\}}'
            match = re.search(patron_variable, contenido_variables, re.DOTALL)
            
            if match:
                contenido_variable = match.group(1)
                if "validation" not in contenido_variable:
                    errores.append(f"❌ Variable crítica '{variable}' debe tener validación")
                else:
                    # Verificar tipos específicos de validación
                    if variable == "environment" and "contains(" not in contenido_variable:
                        errores.append("❌ Variable 'environment' debe validar valores permitidos con contains()")
                    
                    if variable in ["client", "project"] and "regex(" not in contenido_variable:
                        advertencias.append(f"⚠️ Variable '{variable}' debería validar formato con regex()")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }

    def validar_transformaciones_simples_locals(self, contenido_locals: str) -> Dict[str, Any]:
        """REGLA A7: Validar que transformaciones en locals sean simples (máximo 2 niveles)"""
        errores = []
        advertencias = []
        
        # Buscar uso de flatten() con for complejos (prohibido)
        if "flatten(" in contenido_locals and "for" in contenido_locals:
            # Verificar si es un flatten complejo
            patron_flatten_complejo = r'flatten\(\s*\[\s*for[^]]*for[^]]*\]\s*\)'
            if re.search(patron_flatten_complejo, contenido_locals, re.DOTALL):
                errores.append("❌ Transformación compleja con flatten() y for anidados prohibida")
        
        # Contar niveles de anidamiento en for expressions
        patron_for = r'for\s+[^}]*\{'
        for_expressions = re.findall(patron_for, contenido_locals)
        
        for expr in for_expressions:
            # Contar llaves anidadas como indicador de complejidad
            nivel_anidamiento = expr.count('{') + expr.count('[')
            if nivel_anidamiento > 2:
                advertencias.append("⚠️ Transformación en locals podría ser demasiado compleja (>2 niveles)")
        
        # Verificar que exista resource_names (obligatorio)
        if "resource_names" not in contenido_locals:
            errores.append("❌ locals.tf debe contener 'resource_names' con transformación simple")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }

    def validar_outputs_descriptivos(self, contenido_outputs: str) -> Dict[str, Any]:
        """REGLA A5: Validar que outputs tengan descriptions y estructura correcta"""
        errores = []
        advertencias = []
        
        # Buscar todos los outputs
        patron_outputs = r'output\s+"([^"]+)"\s*\{([^}]*)\}'
        outputs = re.findall(patron_outputs, contenido_outputs, re.DOTALL)
        
        outputs_sin_description = []
        outputs_sin_for_each = []
        
        for nombre_output, contenido_output in outputs:
            # Verificar description obligatorio
            if "description" not in contenido_output:
                outputs_sin_description.append(nombre_output)
            
            # Verificar uso de for_each en outputs para recursos múltiples
            if "value" in contenido_output and "aws_" in contenido_output:
                if "for k, v in" not in contenido_output and "[" not in contenido_output:
                    outputs_sin_for_each.append(nombre_output)
        
        if outputs_sin_description:
            errores.extend([f"❌ Output sin description: {output}" for output in outputs_sin_description])
        
        if outputs_sin_for_each:
            advertencias.extend([f"⚠️ Output podría necesitar for_each para recursos múltiples: {output}" for output in outputs_sin_for_each])
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias,
            "outputs_analizados": len(outputs)
        }

    def validar_provider_configuracion(self, contenido_providers: str) -> Dict[str, Any]:
        """REGLA A4: Validar configuración obligatoria del provider"""
        errores = []
        advertencias = []
        
        # Verificar provider AWS
        if 'provider "aws"' not in contenido_providers:
            errores.append("❌ Provider AWS no configurado")
        
        # Verificar versión mínima de Terraform
        if "terraform {" in contenido_providers:
            if "required_version" not in contenido_providers:
                advertencias.append("⚠️ required_version no especificada")
            elif ">= 1.0" not in contenido_providers:
                advertencias.append("⚠️ Versión mínima de Terraform debería ser >= 1.0")
        
        # Verificar required_providers
        if "required_providers" not in contenido_providers:
            advertencias.append("⚠️ required_providers no especificado")
        elif "aws" not in contenido_providers or ">= 5.0" not in contenido_providers:
            advertencias.append("⚠️ AWS provider debería ser >= 5.0")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }
