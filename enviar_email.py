import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# Configurações do servidor SMTP
SMTP_SERVER = "mail.jlaimportadora.com.br"
SMTP_PORT = 587  # Porta TLS padrão (ou 465 para SSL)
EMAIL_REMETENTE = "vendas01@jlaimportadora.com.br"
SENHA = "03021731Lch*"

# Ler emails da lista
print("Lendo lista de emails...")
with open('emails.txt', 'r', encoding='utf-8') as f:
    EMAILS_DESTINO = [email.strip() for email in f.readlines() if email.strip()]

print(f"Preparando envio individual para {len(EMAILS_DESTINO)} email(s)")
print()

# Ler o HTML do email
with open('email-catalogo.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Anexar dados cadastrais uma vez para reutilizar
cadastro_file = "Dados-cadastrais-JLA.pdf"
cadastro_data = None
if os.path.exists(cadastro_file):
    with open(cadastro_file, 'rb') as f:
        cadastro_data = f.read()
    print(f"✓ Arquivo pronto: {cadastro_file}")
else:
    print(f"⚠ Arquivo não encontrado: {cadastro_file}")

print("✓ Email preparado (catálogo disponível via link de download)")
print()

# Conectar ao servidor SMTP uma vez
print(f"Conectando ao servidor {SMTP_SERVER}:{SMTP_PORT}...")
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    print("Autenticando...")
    server.login(EMAIL_REMETENTE, SENHA)
    print("✓ Conectado com sucesso\n")
    
    # Enviar para cada destinatário individualmente
    enviados = 0
    erros = 0
    
    for email_destino in EMAILS_DESTINO:
        try:
            # Criar mensagem individual
            msg = MIMEMultipart('alternative')
            msg['From'] = EMAIL_REMETENTE
            msg['To'] = email_destino
            msg['Subject'] = "Catálogo JLA Importadora - Retentores, Vedações, Rolamentos e Correias"
            
            # Anexar HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Anexar dados cadastrais se disponível
            if cadastro_data:
                pdf_attachment = MIMEApplication(cadastro_data, _subtype='pdf')
                pdf_attachment.add_header('Content-Disposition', 'attachment', filename=cadastro_file)
                msg.attach(pdf_attachment)
            
            # Enviar
            print(f"Enviando para {email_destino}...", end=' ')
            server.send_message(msg)
            print("✓")
            enviados += 1
            
        except Exception as e:
            print(f"✗ Erro: {e}")
            erros += 1
    
    server.quit()
    
    print(f"\n{'='*60}")
    print(f"✓ Envio concluído!")
    print(f"  Enviados com sucesso: {enviados}")
    if erros > 0:
        print(f"  Erros: {erros}")
    print(f"{'='*60}")
    
except smtplib.SMTPAuthenticationError:
    print("\n✗ Erro de autenticação. Verifique o email e senha.")
except smtplib.SMTPException as e:
    print(f"\n✗ Erro SMTP: {e}")
except Exception as e:
    print(f"\n✗ Erro: {e}")
