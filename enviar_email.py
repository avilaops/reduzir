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

# Emails de destino
EMAILS_DESTINO = [
    "nicolasrosaab@gmail.com",
    "vendas@jlaimportadora.com.br"
]

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

# Anexar PDF se existir
pdf_file = "Catalogo-JLA-completo.pdf"
if os.path.exists(pdf_file):
    with open(pdf_file, 'rb') as f:
        pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_file)
        msg.attach(pdf_attachment)
    print(f"✓ PDF anexado: {pdf_file}")
else:
    print(f"⚠ PDF não encontrado: {pdf_file}")

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
