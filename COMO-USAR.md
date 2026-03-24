# Como usar o sistema de envio de emails

## Editar lista de destinatários

Edite o arquivo `emails.txt` e adicione um email por linha:

```
marilia.ferrero@valedoverdao.com.br
fagner@valedoverdao.com.br
cliente@empresa.com.br
```

## Enviar emails

Execute o script:

```bash
python enviar_email.py
```

O script irá:
1. Ler todos os emails do arquivo `emails.txt`
2. Mostrar a lista de destinatários
3. Pedir confirmação antes de enviar
4. Enviar o email com:
   - Dados cadastrais JLA anexados
   - Link para download do catálogo
   - Design profissional com logo

## Estrutura do email

- **Anexo**: Dados-cadastrais-JLA.pdf (1.03 MB)
- **Download**: Catálogo completo via link (7.2 MB)
- **Buttons**: Baixar Catálogo + Solicitar Orçamento
- **Assinatura**: Nícolas Ávila - JLA Importadora
