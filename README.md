<table>
<tr>
<td><a href= "https://www.inteli.edu.br/"><img src="./artefatos/img/logo-inteli.png" alt="Inteli - Instituto de Tecnologia e Liderança" border="0" width="30%"></a>
</td>
</tr>
</table>


# 2024-2A-T05-CC09-G04

# Projeto: Identificação e Monitoramento de Saúde de Bovinos usando Câmeras Termográficas

# Empresa: Agropecuária Vista Alegre Ltda

>Agropecuária Vista Alegre, uma subsidiária do Frigorífico Better Beef, localizada na região de Presidente Prudente – SP, dedica-se à pecuária de corte, com ênfase na compra e engorda de bovinos em sistema de confinamento. Com um compromisso de excelência, toda a produção de bovinos é direcionada exclusivamente ao Frigorífico Better Beef, assegurando um abastecimento constante e de alta qualidade.

# Grupo: G4

# Integrantes:

* [Beny Frid](beny.frid@sou.inteli.edu.br)
* [Enya Oliveira](Enya.arruda@sou.inteli.edu.br)
* [Guilherme Moura](guilherme.moura@sou.inteli.edu.br)
* [Henrique Burle](henrique.burle@sou.inteli.edu.br)
* [Thomaz Klifson](thomaz.klifson@sou.inteli.edu.br)


# Descrição do Projeto

Este projeto tem como objetivo desenvolver e implementar modelos de machine learning para identificar bovinos com possíveis enfermidades utilizando câmeras termográficas. A medição da temperatura ocular dos animais permitirá a detecção precoce de problemas de saúde de forma não invasiva, aumentando a eficácia do monitoramento e a saúde geral do rebanho. Ao final, será disponibilizado um sistema que permitirá à Agropecuária Vista Alegre processar manualmente as gravações capturadas, analisá-las e exportar os resultados, ajudando na tomada de decisões rápidas e informadas sobre o tratamento dos animais.

# Documentação e Artigo

Os arquivos da documentação deste projeto estão na pasta [/artefatos](/artefatos), inclusive os arquivos do artigo.

# Preparando Ambiente:

## Execução via Google Colab:
Caso prefira executar o projeto no Google Colab, siga as instruções abaixo:

- Faça upload do notebook principal e dos arquivos necessários no Colab.
- Instale as dependências no Colab executando o comando abaixo no início do notebook:

```bash
!pip install -r requirements.txt
```
## Interface de Visualização (Streamlit):
O sistema final será disponibilizado via uma interface interativa desenvolvida com Streamlit, onde o cliente poderá visualizar, processar e analisar as imagens termográficas de forma simples e eficiente. Para rodar o Streamlit localmente, siga os passos:

No terminal, execute o comando:

```bash
streamlit run app.py
```

Isso abrirá a interface no navegador, permitindo a interação com os modelos de classificação e segmentação, além da visualização dos resultados de monitoramento de saúde bovina.

# Código
Os arquivos de código estão na pasta [/codigos](/codigos). Dentro esta presente  modelos de classificacao pasta [/modelo_classificacao](/codigos/modelo_classificacao/) , e a pasta de [/segmentacao](codigos/segmentacao/) , onde esta presente o modelo de segmentacao e a parte responsavel por bounding-box


# Tags
Tags são pontos de verificação criados ao final de cada sprint para documentar o progresso do projeto. Elas permitem que a evolução do trabalho seja monitorada e revisada ao longo do tempo, proporcionando uma visão clara das etapas concluídas e das entregas realizadas em cada fase do desenvolvimento.

**Sprint 1**  
- Coleta e processamento de 500 imagens de olhos bovinos, garantindo diversidade e qualidade.
- Escolha e justificativa de ferramenta de anotação de imagens (CVAT ou VIA) e descrição metodológica para artigo científico.


**Sprint 2**  
- Desenvolvimento de modelo CNN para classificação de bovinos, com foco em evitar overfitting e comparação de desempenho entre CPU e GPU.
- Documentação detalhada da metodologia, justificando cada escolha com referências científicas.

**Sprint 3**  
- Aprimoramento de classificação: VGG16, ResNet, EfficientNet.
- Bounding Box: adicionado para melhor detecção de objetos.
- Segmentação: Implementado UNet para segmentação semântica.
- Artigo: Melhoria no desempenho e resultados.

**Sprint 4**
- Novo modelo de segmentação para a cabeça
- Canal de temperatura: identificação da temperatura pela imagem
- Artigo: Análise e discussão

**Sprint 5**
- Integração dos modelos desenvolvidos: Combinar os modelos de classificação, segmentação e temperatura.
- Desenvolvimento de uma interface em Streamlit: Criar uma interface visual e interativa

## Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">

<a property="dct:title" rel="cc:attributionURL">G4</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName">Inteli, Beny Frid, Enya Oliveira, Guilherme Moura, Henrique Burle, Thomaz Klifson </a> is licensed under <a href="https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
