### Relatório: Descrição da Pipeline, Justificativa das Escolhas e Metodologia de Coleta e Processamento

#### 1. Descrição da Pipeline

A pipeline desenvolvida para o projeto de Identificação e Monitoramento de Saúde de Bovinos com Câmeras Termográficas é composta pelas seguintes etapas:

1. **Coleta de Imagens Termográficas:**
   - As imagens foram capturadas utilizando câmeras termográficas instaladas nas instalações da Agropecuária Vista Alegre. Essas imagens foram armazenadas em um serviço de armazenamento na nuvem (OneDrive), conforme acordado no projeto.

2. **Anotação das Imagens:**
   - As imagens capturadas foram importadas para a ferramenta **CVat** (Computer Vision Annotation Tool) para o processo de rotulagem (labeling). As regiões de interesse, especialmente os olhos dos bovinos, foram identificadas e marcadas, permitindo a criação de um dataset rotulado necessário para o treinamento dos modelos de machine learning. Foi necessário criar máscaras de segmentação para os olhos de 500 animais, ou até atingir 1000 olhos rotulados.

3. **Pré-processamento dos Dados:**
   - O código em Python desenvolvido realiza o pré-processamento das imagens rotuladas. Isso inclui a normalização dos dados, ajuste de resoluções, conversão para formatos adequados e o alinhamento das anotações feitas no CVat para que sejam compatíveis com o modelo de machine learning escolhido. Durante o processo de pré-processamento, foi utilizada a técnica de **cropping** para cortar as imagens em pedaços de 60x60 pixels, garantindo que os olhos, ou parte deles, estivessem presentes nos fragmentos, permitindo a detecção pelo modelo.

4. **Treinamento do Modelo:**
   - Utilizando bibliotecas populares de machine learning (como TensorFlow ou PyTorch), o modelo foi treinado com os dados rotulados. O modelo aprende a identificar padrões de temperatura nos olhos dos bovinos, correlacionando essas informações com potenciais enfermidades. Foram implementadas estratégias para garantir que o modelo fosse seletivo, identificando e monitorando apenas os olhos dos bovinos, mesmo em situações onde outros objetos ou animais pudessem estar presentes na imagem.

#### 2. Justificativa das Escolhas

**Ferramentas:**

- **CVat (Computer Vision Annotation Tool):**
  - CVat foi escolhida por sua robustez e suporte para grandes volumes de dados de imagem. É uma ferramenta open-source amplamente utilizada em projetos de visão computacional, oferecendo uma interface intuitiva para anotação de imagens. Sua compatibilidade com diferentes formatos de exportação e a capacidade de lidar com múltiplos anotadores tornam-na ideal para o projeto.

- **Python:**
  -Python é a linguagem escolhida devido à sua vasta biblioteca de ferramentas e frameworks para machine learning e processamento de imagens, como TensorFlow, PyTorch e OpenCV. A flexibilidade e a comunidade ativa de Python garantem um desenvolvimento rápido e eficiente de protótipos e soluções customizadas.

**Formatos:**

- **Formato XML para Exportação dos Resultados:**
  - O formato XML é amplamente aceito e compatível com diversas ferramentas de análise e visualização de dados. Sua simplicidade e eficiência no armazenamento de dados tabulares o tornam uma escolha ideal para exportar resultados de inferências realizadas pelo modelo.

#### 3. Metodologia de Coleta e Processamento

**Coleta:**

A coleta de dados foi realizada utilizando câmeras termográficas transportadas por um motorista de caminhão, que percorreu todas as instalações de confinamento dos bovinos.As imagens foram capturadas em diferentes momentos do dia para garantir a variação e a representatividade dos dados. As imagens foram então carregadas para o OneDrive, de onde foram importadas para o CVat para anotação.

**Processamento:**

O processamento das imagens seguiu uma sequência lógica:
1. **Anotação das Imagens:** Cada imagem foi cuidadosamente rotulada no CVat, com foco nos olhos dos bovinos, a área mais relevante para a medição da temperatura. Foram criadas máscaras de segmentação para os olhos de 500 animais ou até atingir 1000 olhos rotulados por grupo.
2. **Pré-processamento:** As imagens rotuladas foram preparadas para o modelo, com ajustes em resolução e formato, e as anotações foram convertidas para o formato esperado pelo modelo de machine learning. Durante esse processo, a técnica de cropping foi aplicada, onde as imagens foram cortadas em pedaços de 60x60 pixels. Isso foi feito de maneira padronizada para garantir que as partes mais significativas do olho estivessem presentes nos fragmentos de imagem, permitindo que o modelo identificasse corretamente a região de interesse.

Essa pipeline garantiu que o projeto fosse desenvolvido de forma organizada e eficiente, com cada etapa bem definida, desde a coleta de dados até a exportação dos resultados finais.

