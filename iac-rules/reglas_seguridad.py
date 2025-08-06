#!/usr/bin/env python3
"""
Reglas de Seguridad de IaC (S1-S6)
Implementa configuraciones de seguridad obligatorias según Pragma CloudOps
"""

import re
from typing import Dict, Any, List

class ReglasSeguridad:
    """Implementa las reglas de seguridad S1-S6 para módulos Terraform"""
    
    def __init__(self):
        # REGLA S1-S6: Configuraciones de seguridad obligatorias
        self.configuraciones_seguridad_obligatorias = {
            "encryption_enabled": True,
            "block_public_access": True,
            "force_ssl": True,
            "enable_versioning": True
        }

    def validar_cifrado_obligatorio(self, contenido_variables: str, contenido_main: str) -> Dict[str, Any]:
        """REGLA S1: Validar que cifrado esté habilitado por defecto"""
        errores = []
        advertencias = []
        
        # Verificar que variables incluyan encryption_enabled
        if "encryption_enabled" not in contenido_variables:
            errores.append("❌ Variables deben incluir 'encryption_enabled' con default true")
        else:
            # Verificar que el default sea true
            patron_encryption = r'encryption_enabled\s*=\s*optional\([^,]*,\s*true\)'
            if not re.search(patron_encryption, contenido_variables):
                errores.append("❌ 'encryption_enabled' debe tener default = true")
        
        # Verificar implementación de cifrado en recursos
        if "aws_s3_bucket" in contenido_main:
            if "aws_s3_bucket_server_side_encryption_configuration" not in contenido_main:
                errores.append("❌ Buckets S3 deben tener configuración de cifrado server-side")
        
        if "aws_rds" in contenido_main:
            if "storage_encrypted" not in contenido_main:
                errores.append("❌ Instancias RDS deben tener storage_encrypted = true")
        
        if "aws_kms_key" in contenido_main:
            if "enable_key_rotation" not in contenido_main:
                advertencias.append("⚠️ KMS keys deberían tener key rotation habilitado")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }

    def validar_acceso_publico_bloqueado(self, contenido_variables: str, contenido_main: str) -> Dict[str, Any]:
        """REGLA S2: Validar que acceso público esté bloqueado por defecto"""
        errores = []
        advertencias = []
        
        # Verificar que variables incluyan block_public_access
        if "block_public_access" not in contenido_variables:
            errores.append("❌ Variables deben incluir 'block_public_access' con default true")
        
        # Verificar implementación para S3
        if "aws_s3_bucket" in contenido_main:
            if "aws_s3_bucket_public_access_block" not in contenido_main:
                errores.append("❌ Buckets S3 deben tener aws_s3_bucket_public_access_block")
        
        # Verificar que no haya configuraciones públicas explícitas sin justificación
        if "public" in contenido_main.lower() and "true" in contenido_main.lower():
            advertencias.append("⚠️ Configuración pública detectada, verificar que sea intencional")
        
        # Verificar security groups restrictivos
        if "aws_security_group" in contenido_main:
            if "0.0.0.0/0" in contenido_main:
                advertencias.append("⚠️ Security group con acceso desde 0.0.0.0/0 detectado")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }

    def validar_force_ssl_tls(self, contenido_main: str, contenido_data: str) -> Dict[str, Any]:
        """REGLA S3: Validar que SSL/TLS esté forzado"""
        errores = []
        advertencias = []
        
        # Para S3, verificar política de force SSL
        if "aws_s3_bucket" in contenido_main:
            if "force_ssl" not in contenido_main and "SecureTransport" not in contenido_data:
                errores.append("❌ Buckets S3 deben tener política para forzar SSL/TLS")
        
        # Verificar que no haya configuraciones HTTP inseguras
        if "http://" in contenido_main:
            errores.append("❌ URLs HTTP inseguras detectadas, usar HTTPS")
        
        if "ssl = false" in contenido_main or "tls = false" in contenido_main:
            errores.append("❌ SSL/TLS deshabilitado detectado")
        
        # Verificar ALB/ELB con HTTPS
        if "aws_lb" in contenido_main or "aws_elb" in contenido_main:
            if "HTTPS" not in contenido_main and "SSL" not in contenido_main:
                advertencias.append("⚠️ Load Balancer debería usar HTTPS/SSL")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }

    def validar_politicas_menor_privilegio(self, contenido_variables: str, contenido_data: str) -> Dict[str, Any]:
        """REGLA S4: Validar políticas de menor privilegio"""
        errores = []
        advertencias = []
        
        # Verificar estructura de policy_statements en variables
        if "policy_statements" not in contenido_variables:
            advertencias.append("⚠️ Considerar agregar 'policy_statements' para políticas personalizadas")
        else:
            # Verificar estructura correcta
            if "sid" not in contenido_variables or "effect" not in contenido_variables:
                errores.append("❌ policy_statements debe incluir 'sid' y 'effect'")
        
        # Verificar políticas dinámicas en data.tf
        if "aws_iam_policy_document" in contenido_data:
            if "dynamic \"statement\"" not in contenido_data:
                advertencias.append("⚠️ Considerar usar dynamic statements para políticas flexibles")
        
        # Verificar que no haya políticas demasiado permisivas
        if "*" in contenido_data and "Action" in contenido_data:
            advertencias.append("⚠️ Política con acciones '*' detectada, verificar que sea necesaria")
        
        # Verificar principios restrictivos
        if "\"*\"" in contenido_data and "Principal" in contenido_data:
            advertencias.append("⚠️ Política con Principal '*' detectada, considerar ser más restrictivo")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }

    def validar_logging_monitoreo(self, contenido_variables: str, contenido_main: str) -> Dict[str, Any]:
        """REGLA S5: Validar configuración de logging y monitoreo"""
        errores = []
        advertencias = []
        
        # Verificar variables de logging
        if "enable_logging" not in contenido_variables:
            advertencias.append("⚠️ Considerar agregar 'enable_logging' para auditoría")
        
        if "enable_versioning" not in contenido_variables:
            advertencias.append("⚠️ Considerar agregar 'enable_versioning' para auditoría")
        
        # Verificar implementación de versioning para S3
        if "aws_s3_bucket" in contenido_main:
            if "aws_s3_bucket_versioning" not in contenido_main:
                advertencias.append("⚠️ Buckets S3 deberían tener versioning habilitado")
            
            if "aws_s3_bucket_logging" not in contenido_main:
                advertencias.append("⚠️ Buckets S3 deberían tener access logging habilitado")
        
        # Verificar CloudTrail para auditoría
        if "aws_cloudtrail" in contenido_main:
            if "enable_logging" not in contenido_main:
                errores.append("❌ CloudTrail debe tener logging habilitado")
        
        # Verificar CloudWatch logs
        if "aws_cloudwatch_log_group" in contenido_main:
            if "retention_in_days" not in contenido_main:
                advertencias.append("⚠️ CloudWatch log groups deberían tener retention configurado")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }

    def validar_configuracion_redes(self, contenido_main: str) -> Dict[str, Any]:
        """REGLA S6: Validar configuraciones de red seguras"""
        errores = []
        advertencias = []
        
        # Verificar VPC configuration
        if "aws_vpc" in contenido_main:
            if "enable_dns_hostnames" not in contenido_main:
                advertencias.append("⚠️ VPC debería tener DNS hostnames habilitado")
            
            if "enable_dns_support" not in contenido_main:
                advertencias.append("⚠️ VPC debería tener DNS support habilitado")
        
        # Verificar subnets privadas
        if "aws_subnet" in contenido_main:
            if "map_public_ip_on_launch" in contenido_main and "true" in contenido_main:
                advertencias.append("⚠️ Subnets no deberían asignar IPs públicas automáticamente")
        
        # Verificar NACLs restrictivos
        if "aws_network_acl" in contenido_main:
            if "0.0.0.0/0" in contenido_main:
                advertencias.append("⚠️ Network ACL con reglas muy permisivas detectado")
        
        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "advertencias": advertencias
        }
