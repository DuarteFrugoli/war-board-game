#!/usr/bin/env python3
"""
Script para enviar notificação por email sobre o status do pipeline
"""

import smtplib
import ssl
import argparse
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_notification_email(to_email, pipeline_status, run_number, commit_sha, branch):
   
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    from_email = os.getenv('FROM_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    
    if not all([from_email, password, to_email]):
        print("Erro: Variáveis de ambiente de email não configuradas")
        print(f"FROM_EMAIL: {'OK' if from_email else 'FALTA'}")
        print(f"EMAIL_PASSWORD: {'OK' if password else 'FALTA'}")
        print(f"NOTIFICATION_EMAIL: {'OK' if to_email else 'FALTA'}")
        return False
    

    test_status, lint_status, build_status = pipeline_status.split('-')
    
    # Determinar status geral
    if all(status == 'success' for status in [test_status, lint_status, build_status]):
        overall_status = "SUCESSO"
        status_color = "#28a745"
    elif any(status == 'failure' for status in [test_status, lint_status, build_status]):
        overall_status = "FALHA"
        status_color = "#dc3545"
    else:
        overall_status = "PARCIAL"
        status_color = "#ffc107"
    
    # Criar mensagem
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Pipeline War Board Game - {overall_status} - Run #{run_number}"
    message["From"] = from_email
    message["To"] = to_email
    
    
    text_content = f"""
Pipeline Executado - War Board Game

Status: {overall_status}
Run Number: #{run_number}
Branch: {branch}
Commit: {commit_sha[:8]}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

Detalhes dos Jobs:
- Testes: {test_status.upper()}
- Análise de Código: {lint_status.upper()}
- Build/Empacotamento: {build_status.upper()}

Este é um email automático do GitHub Actions.
Repositório: war-board-game
    """
    
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: {status_color};">War Board Game - Pipeline Executado</h2>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3>Status: <span style="color: {status_color};">{overall_status}</span></h3>
                <p><strong>Run Number:</strong> #{run_number}</p>
                <p><strong>Branch:</strong> {branch}</p>
                <p><strong>Commit:</strong> {commit_sha[:8]}</p>
                <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            </div>
            
            <h3>Detalhes dos Jobs:</h3>
            <ul style="list-style-type: none; padding: 0;">
                <li style="margin: 10px 0;">
                    {"[OK]" if test_status == "success" else "[FAIL]" if test_status == "failure" else "[WARN]"} 
                    <strong>Testes:</strong> {test_status.upper()}
                </li>
                <li style="margin: 10px 0;">
                    {"[OK]" if lint_status == "success" else "[FAIL]" if lint_status == "failure" else "[WARN]"} 
                    <strong>Análise de Código:</strong> {lint_status.upper()}
                </li>
                <li style="margin: 10px 0;">
                    {"[OK]" if build_status == "success" else "[FAIL]" if build_status == "failure" else "[WARN]"} 
                    <strong>Build/Empacotamento:</strong> {build_status.upper()}
                </li>
            </ul>
            
            <hr style="margin: 30px 0;">
            <p style="color: #6c757d; font-size: 12px;">
                Este é um email automático do GitHub Actions.<br>
                Repositório: <strong>war-board-game</strong>
            </p>
        </div>
    </body>
    </html>
    """
    
    # Anexar conteúdos
    message.attach(MIMEText(text_content, "plain"))
    message.attach(MIMEText(html_content, "html"))
    
    try:
      
        context = ssl.create_default_context()
        

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(from_email, password)
            server.send_message(message)
        
        print(f"Email enviado com sucesso para {to_email}")
        return True
        
    except Exception as e:
        print(f"Erro ao enviar email: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Enviar notificação de pipeline por email')
    parser.add_argument('--to-email', required=True, help='Email de destino')
    parser.add_argument('--pipeline-status', required=True, help='Status do pipeline (test-lint-build)')
    parser.add_argument('--run-number', required=True, help='Número da execução')
    parser.add_argument('--commit-sha', required=True, help='SHA do commit')
    parser.add_argument('--branch', required=True, help='Nome da branch')
    
    args = parser.parse_args()
    
    print("Enviando notificação por email...")
    print(f"Destinatário: {args.to_email}")
    print(f"Status: {args.pipeline_status}")
    
    success = send_notification_email(
        args.to_email,
        args.pipeline_status,
        args.run_number,
        args.commit_sha,
        args.branch
    )
    
    sys.exit(0 if success else 1)

if _name_ == "_main_":
    main()