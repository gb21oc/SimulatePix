from datetime import datetime
from pybase64 import b64encode
from utilConfig import msgExcept
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor


def generatePDF(amount_paid, name_receiver, account_receiver, cpf_receiver, paying_name, paying_account, paying_cpf):
    try:
        pdf = canvas.Canvas(f"{paying_account}.pdf")

        # ---------------- CABEÇALHO -----------------
        # Titulo
        pdf.setFillColor(HexColor("#FFA500"))
        pdf.setFont("Helvetica-Oblique", 20)
        pdf.drawString(202, 715, "Comprovante PIX")

        # Data
        dataAtual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pdf.setFillColor(HexColor("#FF8C00"))
        pdf.setFont("Helvetica-Oblique", 10)
        pdf.drawString(230, 690, f"{dataAtual}")

        # ---------------- VALOR PAGO-----------------
        # Valor pago
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.setFillColor(HexColor("#000000"))
        pdf.drawString(100, 655,
                       f"--------------------------------------------------------------------------------------------------")
        pdf.setFillColor(HexColor("#808080"))
        pdf.drawString(100, 635, f"Valor Pago")
        pdf.setFillColor(HexColor("#000000"))
        pdf.drawString(100, 615, "R${:,.2f}".format(amount_paid))
        pdf.drawString(100, 595,
                       f"--------------------------------------------------------------------------------------------------")

        # Forma de pagamento
        pdf.setFillColor(HexColor("#808080"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 575, f"Conta Pagador")
        pdf.setFillColor(HexColor("#000000"))
        pdf.drawString(100, 555, f"{paying_account}")

        # ---------------- RECEBEDOR -----------------
        # Dados do recebedor
        pdf.setFillColor(HexColor("#808080"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 525, f"Dados do recebedor")

        # Para
        pdf.setFillColor(HexColor("#808080"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 495, f"Para")

        # Para Nome
        pdf.setFillColor(HexColor("#000000"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 475, f"{name_receiver}")

        # Conta
        pdf.setFillColor(HexColor("#808080"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 455, f"Conta")

        # Numero conta
        pdf.setFillColor(HexColor("#000000"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 435, f"{account_receiver}")

        # CPF
        pdf.setFillColor(HexColor("#808080"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 415, f"CPF")

        # Numero CPF
        pdf.setFillColor(HexColor("#000000"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 395, f"{cpf_receiver.replace(cpf_receiver[0:3], 'X'*3).replace(cpf_receiver[-2::], 'X'*2)}")

        # ---------------- PAGADOR-----------------
        # Dados do recebedor
        pdf.setFillColor(HexColor("#808080"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 365, f"Dados do pagador")

        # Para
        pdf.setFillColor(HexColor("#808080"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 335, f"Para")

        # Para Nome
        pdf.setFillColor(HexColor("#000000"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 315, f"{paying_name}")

        # Conta
        pdf.setFillColor(HexColor("#808080"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 295, f"Conta")

        # Numero conta
        pdf.setFillColor(HexColor("#000000"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 275, f"{paying_account}")

        # CPF
        pdf.setFillColor(HexColor("#808080"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 255, f"CPF")

        # Numero CPF
        pdf.setFillColor(HexColor("#000000"))
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.drawString(100, 235, f"{paying_cpf.replace(paying_cpf[0:3], 'X'*3).replace(paying_cpf[-2::], 'X'*2)}")

        pdf.save()

        file = open(f"{paying_account}.pdf", "rb").read()
        pdfBase64 = b64encode(file).decode("utf-8")
        return pdfBase64
    except (Exception, ValueError, IndexError):
        return {'message': msgExcept}, 500
