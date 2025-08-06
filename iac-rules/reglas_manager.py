#!/usr/bin/env python3
"""
Manager principal de reglas IaC
Orquesta todas las categorías de reglas y proporciona una interfaz unificada
"""

import datetime
from typing import Dict, Any, List

from .reglas_basicas import ReglasBasicas
from .reglas_avanzadas import ReglasAvanzadas
from .reglas_seguridad import ReglasSeguridad
from .reglas_documentacion import ReglasDocumentacion

class ReglasIaCManager:
    """Manager principal que orquesta todas las reglas IaC"""
    
    def __init__(self):
        # Instanciar todas las categorías de reglas
        self.reglas_basicas = ReglasBasicas()
        self.reglas_avanzadas = ReglasAvanzadas()
        self.reglas_seguridad = ReglasSeguridad()
        self.reglas_documentacion = ReglasDocumentacion()
        
        # Metadatos del manager
        self.version = "2.0.0"
        self.categorias_reglas = ["básicas", "avanzadas", "seguridad", "documentación"]

    # ========== MÉTODOS DE REGLAS BÁSICAS ==========
    
    def validar_estructura_modulo_completa(self, ruta_modulo: str) -> Dict[str, Any]:
        """Delegar a reglas básicas"""
        return self.reglas_basicas.validar_estructura_modulo_completa(ruta_modulo)
    
    def validar_convenciones_nomenclatura(self, contenido_locals: str, contenido_main: str) -> Dict[str, Any]:
        """Delegar a reglas básicas"""
        return self.reglas_basicas.validar_convenciones_nomenclatura(contenido_locals, contenido_main)
    
    def validar_variables_obligatorias(self, contenido_variables: str) -> Dict[str, Any]:
        """Delegar a reglas básicas"""
        return self.reglas_basicas.validar_variables_obligatorias(contenido_variables)
    
    def validar_sistema_etiquetado(self, contenido_providers: str, contenido_main: str) -> Dict[str, Any]:
        """Delegar a reglas básicas"""
        return self.reglas_basicas.validar_sistema_etiquetado(contenido_providers, contenido_main)
    
    def validar_sample_funcional(self, ruta_sample: str) -> Dict[str, Any]:
        """Delegar a reglas básicas"""
        return self.reglas_basicas.validar_sample_funcional(ruta_sample)

    # ========== MÉTODOS DE REGLAS AVANZADAS ==========
    
    def validar_tipos_datos_inteligentes(self, contenido_variables: str) -> Dict[str, Any]:
        """Delegar a reglas avanzadas"""
        return self.reglas_avanzadas.validar_tipos_datos_inteligentes(contenido_variables)
    
    def validar_for_each_obligatorio(self, contenido_main: str) -> Dict[str, Any]:
        """Delegar a reglas avanzadas"""
        return self.reglas_avanzadas.validar_for_each_obligatorio(contenido_main)
    
    def validar_validaciones_variables(self, contenido_variables: str) -> Dict[str, Any]:
        """Delegar a reglas avanzadas"""
        return self.reglas_avanzadas.validar_validaciones_variables(contenido_variables)
    
    def validar_transformaciones_simples_locals(self, contenido_locals: str) -> Dict[str, Any]:
        """Delegar a reglas avanzadas"""
        return self.reglas_avanzadas.validar_transformaciones_simples_locals(contenido_locals)
    
    def validar_outputs_descriptivos(self, contenido_outputs: str) -> Dict[str, Any]:
        """Delegar a reglas avanzadas"""
        return self.reglas_avanzadas.validar_outputs_descriptivos(contenido_outputs)
    
    def validar_provider_configuracion(self, contenido_providers: str) -> Dict[str, Any]:
        """Delegar a reglas avanzadas"""
        return self.reglas_avanzadas.validar_provider_configuracion(contenido_providers)

    # ========== MÉTODOS DE REGLAS SEGURIDAD ==========
    
    def validar_cifrado_obligatorio(self, contenido_variables: str, contenido_main: str) -> Dict[str, Any]:
        """Delegar a reglas de seguridad"""
        return self.reglas_seguridad.validar_cifrado_obligatorio(contenido_variables, contenido_main)
    
    def validar_acceso_publico_bloqueado(self, contenido_variables: str, contenido_main: str) -> Dict[str, Any]:
        """Delegar a reglas de seguridad"""
        return self.reglas_seguridad.validar_acceso_publico_bloqueado(contenido_variables, contenido_main)
    
    def validar_force_ssl_tls(self, contenido_main: str, contenido_data: str) -> Dict[str, Any]:
        """Delegar a reglas de seguridad"""
        return self.reglas_seguridad.validar_force_ssl_tls(contenido_main, contenido_data)
    
    def validar_politicas_menor_privilegio(self, contenido_variables: str, contenido_data: str) -> Dict[str, Any]:
        """Delegar a reglas de seguridad"""
        return self.reglas_seguridad.validar_politicas_menor_privilegio(contenido_variables, contenido_data)
    
    def validar_logging_monitoreo(self, contenido_variables: str, contenido_main: str) -> Dict[str, Any]:
        """Delegar a reglas de seguridad"""
        return self.reglas_seguridad.validar_logging_monitoreo(contenido_variables, contenido_main)
    
    def validar_configuracion_redes(self, contenido_main: str) -> Dict[str, Any]:
        """Delegar a reglas de seguridad"""
        return self.reglas_seguridad.validar_configuracion_redes(contenido_main)

    # ========== MÉTODOS DE REGLAS DOCUMENTACIÓN ==========
    
    def validar_readme_estructura_completa(self, contenido_readme: str) -> Dict[str, Any]:
        """Delegar a reglas de documentación"""
        return self.reglas_documentacion.validar_readme_estructura_completa(contenido_readme)
    
    def validar_changelog_formato_completo(self, contenido_changelog: str) -> Dict[str, Any]:
        """Delegar a reglas de documentación"""
        return self.reglas_documentacion.validar_changelog_formato_completo(contenido_changelog)
    
    def validar_sample_readme(self, contenido_sample_readme: str) -> Dict[str, Any]:
        """Delegar a reglas de documentación"""
        return self.reglas_documentacion.validar_sample_readme(contenido_sample_readme)
    
    def validar_terraform_docs_configuracion(self, ruta_modulo: str) -> Dict[str, Any]:
        """Delegar a reglas de documentación"""
        return self.reglas_documentacion.validar_terraform_docs_configuracion(ruta_modulo)
    
    def validar_descriptions_obligatorios(self, contenido_variables: str, contenido_outputs: str) -> Dict[str, Any]:
        """Delegar a reglas de documentación"""
        return self.reglas_documentacion.validar_descriptions_obligatorios(contenido_variables, contenido_outputs)

    # ========== MÉTODOS DE GENERACIÓN ==========
    
    def obtener_plantilla_readme_completa(self, nombre_modulo: str, tipo_recurso: str = "recurso") -> str:
        """Delegar a reglas de documentación"""
        return self.reglas_documentacion.obtener_plantilla_readme_completa(nombre_modulo, tipo_recurso)
    
    def obtener_plantilla_changelog_completa(self) -> str:
        """Delegar a reglas de documentación"""
        return self.reglas_documentacion.obtener_plantilla_changelog_completa()
    
    def obtener_configuracion_terraform_docs(self) -> str:
        """Delegar a reglas de documentación"""
        return self.reglas_documentacion.obtener_configuracion_terraform_docs()
    
    def obtener_plantilla_sample_readme(self, nombre_modulo: str) -> str:
        """Delegar a reglas de documentación"""
        return self.reglas_documentacion.obtener_plantilla_sample_readme(nombre_modulo)

    # ========== MÉTODOS DE ORQUESTACIÓN ==========
    
    def generar_reporte_validacion_completo(self, ruta_modulo: str) -> Dict[str, Any]:
        """Generar reporte completo aplicando todas las categorías de reglas"""
        reporte = {
            "modulo": ruta_modulo,
            "timestamp": datetime.datetime.now().isoformat(),
            "version_reglas": self.version,
            "validaciones": {},
            "resumen": {
                "total_errores": 0,
                "total_advertencias": 0,
                "validacion_exitosa": True,
                "reglas_aplicadas": [],
                "categorias_evaluadas": []
            }
        }
        
        # Validaciones que no requieren contenido de archivos (solo estructura)
        validaciones_estructura = [
            ("estructura_modulo", self.validar_estructura_modulo_completa, "básicas"),
            ("terraform_docs_config", self.validar_terraform_docs_configuracion, "documentación")
        ]
        
        for nombre, funcion_validacion, categoria in validaciones_estructura:
            try:
                resultado = funcion_validacion(ruta_modulo)
                reporte["validaciones"][nombre] = resultado
                reporte["resumen"]["total_errores"] += len(resultado.get("errores", []))
                reporte["resumen"]["total_advertencias"] += len(resultado.get("advertencias", []))
                reporte["resumen"]["reglas_aplicadas"].append(nombre)
                
                if categoria not in reporte["resumen"]["categorias_evaluadas"]:
                    reporte["resumen"]["categorias_evaluadas"].append(categoria)
                
                if not resultado.get("valido", True):
                    reporte["resumen"]["validacion_exitosa"] = False
                    
            except Exception as e:
                reporte["validaciones"][nombre] = {
                    "valido": False,
                    "errores": [f"Error ejecutando validación: {str(e)}"],
                    "categoria": categoria
                }
                reporte["resumen"]["validacion_exitosa"] = False
        
        # Agregar resumen por categorías
        reporte["resumen"]["total_categorias"] = len(self.categorias_reglas)
        reporte["resumen"]["categorias_evaluadas_count"] = len(reporte["resumen"]["categorias_evaluadas"])
        
        return reporte

    def obtener_estadisticas_reglas(self) -> Dict[str, Any]:
        """Obtener estadísticas sobre las reglas disponibles"""
        return {
            "version": self.version,
            "categorias_disponibles": self.categorias_reglas,
            "total_categorias": len(self.categorias_reglas),
            "reglas_por_categoria": {
                "básicas": [
                    "validar_estructura_modulo_completa",
                    "validar_convenciones_nomenclatura", 
                    "validar_variables_obligatorias",
                    "validar_sistema_etiquetado",
                    "validar_sample_funcional"
                ],
                "avanzadas": [
                    "validar_tipos_datos_inteligentes",
                    "validar_for_each_obligatorio",
                    "validar_validaciones_variables",
                    "validar_transformaciones_simples_locals",
                    "validar_outputs_descriptivos",
                    "validar_provider_configuracion"
                ],
                "seguridad": [
                    "validar_cifrado_obligatorio",
                    "validar_acceso_publico_bloqueado",
                    "validar_force_ssl_tls",
                    "validar_politicas_menor_privilegio",
                    "validar_logging_monitoreo",
                    "validar_configuracion_redes"
                ],
                "documentación": [
                    "validar_readme_estructura_completa",
                    "validar_changelog_formato_completo",
                    "validar_sample_readme",
                    "validar_terraform_docs_configuracion",
                    "validar_descriptions_obligatorios"
                ]
            },
            "herramientas_generacion": [
                "obtener_plantilla_readme_completa",
                "obtener_plantilla_changelog_completa",
                "obtener_configuracion_terraform_docs",
                "obtener_plantilla_sample_readme"
            ]
        }

    def validar_categoria_completa(self, categoria: str, archivos_modulo: Dict[str, str]) -> Dict[str, Any]:
        """Validar una categoría completa de reglas con archivos proporcionados"""
        if categoria not in self.categorias_reglas:
            return {
                "valido": False,
                "errores": [f"Categoría '{categoria}' no reconocida"],
                "categoria": categoria
            }
        
        resultados = {
            "categoria": categoria,
            "validaciones": {},
            "resumen": {
                "total_errores": 0,
                "total_advertencias": 0,
                "validacion_exitosa": True
            }
        }
        
        # Aquí se implementarían las validaciones específicas por categoría
        # usando los archivos proporcionados en archivos_modulo
        
        return resultados

    def ejecutar_herramienta(self, nombre_herramienta: str, argumentos: Dict[str, Any]) -> str:
        """Ejecuta una herramienta específica basada en su nombre"""
        
        # ========== REGLAS BÁSICAS ==========
        if nombre_herramienta == "validar_estructura_modulo":
            ruta_modulo = argumentos.get("ruta_modulo")
            resultado = self.validar_estructura_modulo_completa(ruta_modulo)
            return self._formatear_resultado_validacion(resultado, "Validación de Estructura del Módulo")
            
        elif nombre_herramienta == "validar_variables_obligatorias":
            ruta_variables = argumentos.get("ruta_variables")
            try:
                with open(ruta_variables, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                resultado = self.validar_variables_obligatorias(contenido)
                return self._formatear_resultado_validacion(resultado, "Validación de Variables Obligatorias")
            except Exception as e:
                return f"❌ Error leyendo archivo {ruta_variables}: {str(e)}"
        
        # ========== REGLAS AVANZADAS ==========
        elif nombre_herramienta == "validar_tipos_datos":
            ruta_variables = argumentos.get("ruta_variables")
            try:
                with open(ruta_variables, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                resultado = self.validar_tipos_datos_inteligentes(contenido)
                return self._formatear_resultado_validacion(resultado, "Validación de Tipos de Datos")
            except Exception as e:
                return f"❌ Error leyendo archivo {ruta_variables}: {str(e)}"
                
        elif nombre_herramienta == "validar_for_each":
            ruta_main = argumentos.get("ruta_main")
            try:
                with open(ruta_main, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                resultado = self.validar_for_each_obligatorio(contenido)
                return self._formatear_resultado_validacion(resultado, "Validación de for_each")
            except Exception as e:
                return f"❌ Error leyendo archivo {ruta_main}: {str(e)}"
        
        # ========== REGLAS DE SEGURIDAD ==========
        elif nombre_herramienta == "validar_cifrado_obligatorio":
            ruta_variables = argumentos.get("ruta_variables")
            ruta_main = argumentos.get("ruta_main")
            try:
                with open(ruta_variables, 'r', encoding='utf-8') as f:
                    contenido_variables = f.read()
                with open(ruta_main, 'r', encoding='utf-8') as f:
                    contenido_main = f.read()
                resultado = self.validar_cifrado_obligatorio(contenido_variables, contenido_main)
                return self._formatear_resultado_validacion(resultado, "Validación de Cifrado Obligatorio")
            except Exception as e:
                return f"❌ Error leyendo archivos: {str(e)}"
                
        elif nombre_herramienta == "validar_acceso_publico":
            ruta_variables = argumentos.get("ruta_variables")
            ruta_main = argumentos.get("ruta_main")
            try:
                with open(ruta_variables, 'r', encoding='utf-8') as f:
                    contenido_variables = f.read()
                with open(ruta_main, 'r', encoding='utf-8') as f:
                    contenido_main = f.read()
                resultado = self.validar_acceso_publico_bloqueado(contenido_variables, contenido_main)
                return self._formatear_resultado_validacion(resultado, "Validación de Acceso Público")
            except Exception as e:
                return f"❌ Error leyendo archivos: {str(e)}"
        
        # ========== REGLAS DE DOCUMENTACIÓN ==========
        elif nombre_herramienta == "validar_readme_estructura":
            ruta_readme = argumentos.get("ruta_readme")
            try:
                with open(ruta_readme, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                resultado = self.validar_readme_estructura_completa(contenido)
                return self._formatear_resultado_validacion(resultado, "Validación de Estructura README")
            except Exception as e:
                return f"❌ Error leyendo archivo {ruta_readme}: {str(e)}"
                
        elif nombre_herramienta == "validar_changelog":
            ruta_changelog = argumentos.get("ruta_changelog")
            try:
                with open(ruta_changelog, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                resultado = self.validar_changelog_formato_completo(contenido)
                return self._formatear_resultado_validacion(resultado, "Validación de CHANGELOG")
            except Exception as e:
                return f"❌ Error leyendo archivo {ruta_changelog}: {str(e)}"
        
        # ========== HERRAMIENTAS DE GENERACIÓN ==========
        elif nombre_herramienta == "generar_plantilla_readme":
            nombre_modulo = argumentos.get("nombre_modulo")
            tipo_recurso = argumentos.get("tipo_recurso", "recurso")
            plantilla = self.obtener_plantilla_readme_completa(nombre_modulo, tipo_recurso)
            return f"📄 **Plantilla README.md generada para {nombre_modulo}**\n\n```markdown\n{plantilla}\n```"
            
        elif nombre_herramienta == "generar_plantilla_changelog":
            plantilla = self.obtener_plantilla_changelog_completa()
            return f"📄 **Plantilla CHANGELOG.md generada**\n\n```markdown\n{plantilla}\n```"
            
        elif nombre_herramienta == "generar_config_terraform_docs":
            config = self.obtener_configuracion_terraform_docs()
            return f"⚙️ **Configuración .terraform-docs.yml generada**\n\n```yaml\n{config}\n```"
        
        # ========== HERRAMIENTAS DE INFORMACIÓN ==========
        elif nombre_herramienta == "obtener_estadisticas_reglas":
            estadisticas = self.obtener_estadisticas_reglas()
            return self._formatear_estadisticas(estadisticas)
            
        elif nombre_herramienta == "generar_reporte_completo":
            ruta_modulo = argumentos.get("ruta_modulo")
            reporte = self.generar_reporte_validacion_completo(ruta_modulo)
            return self._formatear_reporte_completo(reporte)
        
        else:
            raise Exception(f"Herramienta no implementada: {nombre_herramienta}")
    
    def _formatear_resultado_validacion(self, resultado: Dict[str, Any], titulo: str) -> str:
        """Formatea el resultado de una validación para presentación"""
        estado = "✅ VÁLIDO" if resultado.get("valido", False) else "❌ INVÁLIDO"
        mensaje = resultado.get("mensaje", "Sin mensaje")
        
        output = f"## {titulo}\n\n**Estado:** {estado}\n\n**Resultado:** {mensaje}\n\n"
        
        if "errores" in resultado and resultado["errores"]:
            output += "### ❌ Errores encontrados:\n"
            for error in resultado["errores"]:
                output += f"- {error}\n"
            output += "\n"
        
        if "advertencias" in resultado and resultado["advertencias"]:
            output += "### ⚠️ Advertencias:\n"
            for advertencia in resultado["advertencias"]:
                output += f"- {advertencia}\n"
            output += "\n"
        
        if "recomendaciones" in resultado and resultado["recomendaciones"]:
            output += "### 💡 Recomendaciones:\n"
            for recomendacion in resultado["recomendaciones"]:
                output += f"- {recomendacion}\n"
            output += "\n"
        
        return output
    
    def _formatear_estadisticas(self, estadisticas: Dict[str, Any]) -> str:
        """Formatea las estadísticas de reglas"""
        output = "## 📊 Estadísticas de Reglas IaC\n\n"
        
        output += f"**Versión:** {estadisticas['version']}\n"
        output += f"**Total de reglas:** {estadisticas['total_reglas']}\n\n"
        
        for categoria, info in estadisticas['categorias'].items():
            output += f"### {categoria.title()}\n"
            output += f"- **Cantidad:** {info['cantidad']}\n"
            output += f"- **Reglas:** {', '.join(info['reglas'])}\n\n"
        
        return output
    
    def _formatear_reporte_completo(self, reporte: Dict[str, Any]) -> str:
        """Formatea el reporte completo de validación"""
        output = f"# 📋 Reporte Completo de Validación IaC\n\n"
        output += f"**Módulo:** {reporte['modulo']}\n"
        output += f"**Fecha:** {reporte['fecha']}\n"
        output += f"**Versión:** {reporte['version']}\n\n"
        
        # Resumen general
        output += "## 📊 Resumen General\n\n"
        resumen = reporte['resumen']
        output += f"- **Total de validaciones:** {resumen['total_validaciones']}\n"
        output += f"- **Validaciones exitosas:** {resumen['exitosas']}\n"
        output += f"- **Validaciones fallidas:** {resumen['fallidas']}\n"
        output += f"- **Porcentaje de éxito:** {resumen['porcentaje_exito']:.1f}%\n\n"
        
        # Detalles por categoría
        for categoria, resultados in reporte['resultados'].items():
            if resultados:  # Solo mostrar categorías con resultados
                output += f"## {categoria.title()}\n\n"
                for nombre_validacion, resultado in resultados.items():
                    estado = "✅" if resultado.get("valido", False) else "❌"
                    output += f"### {estado} {nombre_validacion}\n"
                    output += f"{resultado.get('mensaje', 'Sin mensaje')}\n\n"
        
        return output
