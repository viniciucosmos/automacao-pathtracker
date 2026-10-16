
from tkinter import Tk, filedialog
from openpyxl import load_workbook
from datetime import datetime


def selecionar_planilha():
    """Abre uma janela para selecionar o arquivo Excel."""

    janela = Tk()
    janela.withdraw()
    janela.attributes("-topmost", True)

    caminho = filedialog.askopenfilename(
        title="Selecione a planilha de Exclusões",
        filetypes=[
            ("Planilhas Excel", "*.xlsx")
        ]
    )

    janela.destroy()

    if not caminho:
        raise Exception("Nenhuma planilha foi selecionada.")

    return caminho


def salvar_clientes(caminho, data_rota, resultado):
    """Adiciona clientes não visitados à aba Exclusões."""

    workbook = load_workbook(caminho)

    if "Exclusões" not in workbook.sheetnames:
        workbook.close()
        raise Exception(
            "A planilha selecionada não possui a aba 'Exclusões'."
        )

    aba = workbook["Exclusões"]

    # Localiza os cabeçalhos na linha 5.
    cabecalhos = {
        str(aba.cell(row=5, column=col).value).strip(): col
        for col in range(1, aba.max_column + 1)
        if aba.cell(row=5, column=col).value is not None
    }

    colunas_necessarias = [
        "Data da Rota Planejada",
        "Vendedor",
        "Código do Cliente",
        "Nome do Cliente"
    ]

    faltantes = [
        coluna for coluna in colunas_necessarias
        if coluna not in cabecalhos
    ]

    if faltantes:
        workbook.close()
        raise Exception(
            f"Colunas não encontradas na linha 5: {faltantes}"
        )

    col_data = cabecalhos["Data da Rota Planejada"]
    col_vendedor = cabecalhos["Vendedor"]
    col_cliente = cabecalhos["Código do Cliente"]
    col_nome = cabecalhos["Nome do Cliente"]

    data = datetime.strptime(data_rota, "%d/%m/%Y").date()

    # Cria as chaves dos registros que já existem.
    existentes = set()

    for linha in range(6, aba.max_row + 1):
        valor_data = aba.cell(linha, col_data).value
        valor_vendedor = aba.cell(linha, col_vendedor).value
        valor_cliente = aba.cell(linha, col_cliente).value

        if valor_data is None or valor_vendedor is None or valor_cliente is None:
            continue

        if isinstance(valor_data, datetime):
            data_existente = valor_data.date()
        elif hasattr(valor_data, "year") and hasattr(valor_data, "month"):
            data_existente = valor_data
        else:
            try:
                data_existente = datetime.strptime(
                    str(valor_data).strip(), "%d/%m/%Y"
                ).date()
            except ValueError:
                continue

        chave = (
            data_existente,
            str(valor_vendedor).strip().lstrip("0") or "0",
            str(valor_cliente).strip().lstrip("0") or "0"
        )

        existentes.add(chave)

    adicionados = 0
    duplicados = 0

    for item in resultado:
        chave = (
            data,
            str(item["vendedor"]).strip().lstrip("0") or "0",
            str(item["codigo_cliente"]).strip().lstrip("0") or "0"
        )

        if chave in existentes:
            duplicados += 1
            continue

            nova_linha = 6

    while any(
        aba.cell(nova_linha, coluna).value is not None
        for coluna in (col_data, col_vendedor, col_cliente, col_nome)
    ):
        nova_linha += 1

        aba.cell(nova_linha, col_data).value = data
        aba.cell(nova_linha, col_data).number_format = "d/m/yyyy"

        aba.cell(nova_linha, col_vendedor).value = int(
            item["vendedor"]
        )
        aba.cell(nova_linha, col_vendedor).number_format = "000"

        aba.cell(nova_linha, col_cliente).value = int(
            item["codigo_cliente"]
        )
        aba.cell(nova_linha, col_cliente).number_format = "00000000"

        aba.cell(nova_linha, col_nome).value = item["nome_comercial"]

        existentes.add(chave)
        adicionados += 1

    workbook.save(caminho)
    workbook.close()

    return adicionados, duplicados
