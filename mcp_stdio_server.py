#!/usr/bin/env python3
"""
MCP Server para Amazon Q CLI usando stdio
Este servidor implementa el protocolo MCP usando entrada/salida estándar
Incluye reglas personalizadas completas para IaC (Infrastructure as Code)
Versión 2.0 - Estructura modular refactorizada
"""

import json
import sys
import logging
import os
from typing import Dict, Any, List
from pydantic import BaseModel

# Importar el manager de reglas IaC refactorizado
from iac_rules import ReglasIaCManager

# Configurar logging para escribir a stderr (no interfiere con stdio)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

class MCPRequest(BaseModel):
    """Modelo para las peticiones MCP"""
    jsonrpc: str = "2.0"
    id: int
    method: str
    params: Dict[str, Any] = {}

class MCPResponse(BaseModel):
    """Modelo para las respuestas MCP"""
    jsonrpc: str = "2.0"
    id: int
    result: Dict[str, Any] = {}
    error: Dict[str, Any] = None

class MCPStdioServer:
    """Clase principal del servidor MCP para stdio con reglas IaC modulares"""
    
    def __init__(self):
        self.tools = {}
        self.resources = {}
        self.reglas_manager = ReglasIaCManager()  # Usar el manager refactorizado
        self._register_tools()
        logger.info(f"MCP CloudOps v{self.reglas_manager.version} con estructura modular inicializado")
    
    def _register_tools(self):
        """Registra todas las herramientas disponibles usando el manager refactorizado"""
        
        # Herramienta de saludo (para pruebas)
        self.tools["saludo"] = {
            "name": "saludo",
            "description": "Responde con un saludo amigable desde tu MCP server personalizado",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "nombre": {
                        "type": "string",
                        "description": "Nombre de la persona a saludar"
                    }
                }
            }
        }
        
        # ========== REGLAS BÁSICAS ==========
        
        self.tools["validar_estructura_modulo"] = {
            "name": "validar_estructura_modulo",
            "description": "🏗️ [BÁSICAS] Valida que el módulo tenga exactamente 16 elementos obligatorios",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ruta_modulo": {
                        "type": "string",
                        "description": "Ruta al directorio del módulo Terraform a validar"
                    }
                },
                "required": ["ruta_modulo"]
            }
        }
        
        self.tools["validar_variables_obligatorias"] = {
            "name": "validar_variables_obligatorias",
            "description": "🏗️ [BÁSICAS] Verifica que estén presentes client, project, environment con descriptions",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ruta_variables": {
                        "type": "string",
                        "description": "Ruta al archivo variables.tf"
                    }
                },
                "required": ["ruta_variables"]
            }
        }
        
        # ========== REGLAS AVANZADAS ==========
        
        self.tools["validar_tipos_datos"] = {
            "name": "validar_tipos_datos",
            "description": "⚙️ [AVANZADAS] Valida el uso correcto de tipos de datos inteligentes (map(object()), list(object()), etc.)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ruta_variables": {
                        "type": "string",
                        "description": "Ruta al archivo variables.tf"
                    }
                },
                "required": ["ruta_variables"]
            }
        }
        
        self.tools["validar_for_each"] = {
            "name": "validar_for_each",
            "description": "⚙️ [AVANZADAS] Valida que se use for_each en lugar de count para recursos múltiples",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ruta_main": {
                        "type": "string",
                        "description": "Ruta al archivo main.tf"
                    }
                },
                "required": ["ruta_main"]
            }
        }
        
        # ========== REGLAS DE SEGURIDAD ==========
        
        self.tools["validar_cifrado_obligatorio"] = {
            "name": "validar_cifrado_obligatorio",
            "description": "🔒 [SEGURIDAD] Valida que el cifrado esté habilitado por defecto en todos los recursos",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ruta_variables": {
                        "type": "string",
                        "description": "Ruta al archivo variables.tf"
                    },
                    "ruta_main": {
                        "type": "string",
                        "description": "Ruta al archivo main.tf"
                    }
                },
                "required": ["ruta_variables", "ruta_main"]
            }
        }
        
        self.tools["validar_acceso_publico"] = {
            "name": "validar_acceso_publico",
            "description": "🔒 [SEGURIDAD] Valida que el acceso público esté bloqueado por defecto",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ruta_variables": {
                        "type": "string",
                        "description": "Ruta al archivo variables.tf"
                    },
                    "ruta_main": {
                        "type": "string",
                        "description": "Ruta al archivo main.tf"
                    }
                },
                "required": ["ruta_variables", "ruta_main"]
            }
        }
        
        # ========== REGLAS DE DOCUMENTACIÓN ==========
        
        self.tools["validar_readme_estructura"] = {
            "name": "validar_readme_estructura",
            "description": "📄 [DOCUMENTACIÓN] Valida que el README.md tenga las 12 secciones obligatorias en el orden correcto",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ruta_readme": {
                        "type": "string",
                        "description": "Ruta al archivo README.md"
                    }
                },
                "required": ["ruta_readme"]
            }
        }
        
        self.tools["validar_changelog"] = {
            "name": "validar_changelog",
            "description": "📄 [DOCUMENTACIÓN] Valida que el CHANGELOG.md siga el formato Keep a Changelog",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ruta_changelog": {
                        "type": "string",
                        "description": "Ruta al archivo CHANGELOG.md"
                    }
                },
                "required": ["ruta_changelog"]
            }
        }
        
        # ========== HERRAMIENTAS DE GENERACIÓN ==========
        
        self.tools["generar_plantilla_readme"] = {
            "name": "generar_plantilla_readme",
            "description": "🛠️ [GENERACIÓN] Genera una plantilla completa de README.md según todas las reglas de documentación",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "nombre_modulo": {
                        "type": "string",
                        "description": "Nombre del módulo Terraform"
                    },
                    "tipo_recurso": {
                        "type": "string",
                        "description": "Tipo de recurso principal (ej: s3, lambda, rds)",
                        "default": "recurso"
                    }
                },
                "required": ["nombre_modulo"]
            }
        }
        
        self.tools["generar_plantilla_changelog"] = {
            "name": "generar_plantilla_changelog",
            "description": "🛠️ [GENERACIÓN] Genera una plantilla completa de CHANGELOG.md con formato Keep a Changelog",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        }
        
        self.tools["generar_config_terraform_docs"] = {
            "name": "generar_config_terraform_docs",
            "description": "🛠️ [GENERACIÓN] Genera la configuración completa de .terraform-docs.yml",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        }
        
        # ========== HERRAMIENTAS DE INFORMACIÓN ==========
        
        self.tools["obtener_estadisticas_reglas"] = {
            "name": "obtener_estadisticas_reglas",
            "description": "📊 [INFO] Obtiene estadísticas completas sobre las reglas IaC disponibles por categoría",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        }
        
        self.tools["generar_reporte_completo"] = {
            "name": "generar_reporte_completo",
            "description": "📊 [REPORTE] Genera un reporte completo de validación aplicando todas las reglas IaC organizadas por categorías",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ruta_modulo": {
                        "type": "string",
                        "description": "Ruta al directorio del módulo Terraform"
                    }
                },
                "required": ["ruta_modulo"]
            }
        }
    
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja la inicialización del servidor MCP"""
        logger.info("Inicializando servidor MCP stdio")
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {"listChanged": False},
                "resources": {"subscribe": False, "listChanged": False}
            },
            "serverInfo": {
                "name": "mcp-flask-server-stdio",
                "version": "1.0.0"
            }
        }
    
    def handle_tools_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Lista todas las herramientas disponibles"""
        logger.info("Listando herramientas disponibles")
        tools_list = []
        for tool_name, tool_info in self.tools.items():
            tools_list.append({
                "name": tool_info["name"],
                "description": tool_info["description"],
                "inputSchema": tool_info["inputSchema"]
            })
        return {"tools": tools_list}
    
    def handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta una herramienta específica usando el manager refactorizado"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        logger.info(f"Ejecutando herramienta: {tool_name} con argumentos: {arguments}")
        
        if tool_name not in self.tools:
            raise Exception(f"Herramienta desconocida: {tool_name}")
        
        # Herramienta de saludo (para pruebas)
        if tool_name == "saludo":
            nombre = arguments.get("nombre", "Usuario")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"¡Hola {nombre}! 👋 Soy tu servidor MCP CloudOps v{self.reglas_manager.version} especializado en reglas IaC para Terraform. ¿En qué puedo ayudarte hoy?"
                    }
                ]
            }
        
        # Delegar al manager de reglas IaC refactorizado
        try:
            resultado = self.reglas_manager.ejecutar_herramienta(tool_name, arguments)
            return {
                "content": [
                    {
                        "type": "text", 
                        "text": resultado
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Error ejecutando herramienta {tool_name}: {str(e)}")
            raise Exception(f"Error ejecutando {tool_name}: {str(e)}")
    
    def run(self):
        """Ejecuta el servidor MCP usando stdio"""
        logger.info("Iniciando servidor MCP stdio...")
        
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Parsear petición JSON-RPC
                    request_data = json.loads(line)
                    request = MCPRequest(**request_data)
                    
                    logger.info(f"Procesando: {request.method}")
                    
                    # Procesar petición
                    if request.method == "initialize":
                        result = self.handle_initialize(request.params)
                    elif request.method == "tools/list":
                        result = self.handle_tools_list(request.params)
                    elif request.method == "tools/call":
                        result = self.handle_tools_call(request.params)
                    else:
                        raise Exception(f"Método desconocido: {request.method}")
                    
                    # Crear respuesta
                    response = MCPResponse(
                        id=request.id,
                        result=result
                    )
                    
                    # Enviar respuesta a stdout
                    print(json.dumps(response.model_dump()), flush=True)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Error decodificando JSON: {e}")
                    error_response = MCPResponse(
                        id=0,
                        error={"code": -32700, "message": f"Parse error: {str(e)}"}
                    )
                    print(json.dumps(error_response.model_dump()), flush=True)
                    
                except Exception as e:
                    logger.error(f"Error procesando petición: {e}")
                    error_response = MCPResponse(
                        id=request.id if 'request' in locals() else 0,
                        error={"code": -32603, "message": f"Internal error: {str(e)}"}
                    )
                    print(json.dumps(error_response.model_dump()), flush=True)
                    
        except KeyboardInterrupt:
            logger.info("Servidor interrumpido por el usuario")
        except Exception as e:
            logger.error(f"Error fatal en el servidor: {e}")
        finally:
            logger.info("Servidor MCP stdio terminado")

if __name__ == "__main__":
    server = MCPStdioServer()
    server.run()
