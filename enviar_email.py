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

print(f"Preparando envio para {len(EMAILS_DESTINO)} email(s):")
for email in EMAILS_DESTINO:
    print(f"  - {email}")
print()

# Criar mensagem
msg = MIMEMultipart('alternative')
msg['From'] = EMAIL_REMETENTE
msg['To'] = ", ".join(EMAILS_DESTINO)
msg['Subject'] = "Catálogo JLA Importadora - Retentores, Vedações, Rolamentos e Correias"

# Ler o HTML do email
with open('email-catalogo.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Anexar HTML
html_part = MIMEText(html_content, 'html', 'utf-8')
msg.attach(html_part)

# Anexar dados cadastrais
cadastro_file = "Dados-cadastrais-JLA.pdf"
if os.path.exists(cadastro_file):
    with open(cadastro_file, 'rb') as f:
        pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename=cadastro_file)
        msg.attach(pdf_attachment)
    print(f"✓ Anexado: {cadastro_file}")
else:
    print(f"⚠ Arquivo não encontrado: {cadastro_file}")

print("✓ Email preparado (catálogo disponível via link de download)")

# Enviar email
print(f"\nEnviando email para {', '.join(EMAILS_DESTINO)}...")
print(f"Servidor: {SMTP_SERVER}:{SMTP_PORT}")

try:
    # Conectar ao servidor SMTP
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  # Iniciar criptografia TLS
    
    # Fazer login
    print("Autenticando...")
    server.login(EMAIL_REMETENTE, SENHA)
    
    # Enviar email
    print("Enviando...")
    server.send_message(msg)
    server.quit()
    
    print(f"\n✓ Email enviado com sucesso para {', '.join(EMAILS_DESTINO)}!")
    print(f"✓ Assunto: {msg['Subject']}")
    
except smtplib.SMTPAuthenticationError:
    print("\n✗ Erro de autenticação. Verifique o email e senha.")
except smtplib.SMTPException as e:
    print(f"\n✗ Erro SMTP: {e}")
except Exception as e:
    print(f"\n✗ Erro: {e}")
