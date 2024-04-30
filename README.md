[English Version](#data-engineering-crimes-and-accidents-in-são-francisco)

[Portuguese Version](#engenharia-de-dados-crimes-e-acidentes-em-são-francisco)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

# Data Engineering - Crimes and Accidents in São Francisco

Status: In Progress

Area: Data Engineer

![Untitled](images/Banner.png)

# Description
This project aims to complete a full cycle of a simple data engineering service. The system will consume data from a public API, store this historical data in a structured database, and make it available for the data visualization system for analysis.

# Architecture
![Arquitetura_Sistema](images/Architecture.png)
# API
[API Oficial](https://www.notion.so/Teste-da-api-do-1Password-env-via-1password-d0fa81daf8fa4b65b356d8cd9b303be6?pvs=21) | [Documentação Oficial](https://datasf.gitbook.io/datasf-dataset-explainers/sfpd-incident-report-2018-to-present)

The chosen data source for this project was a public API provided by the government of the city of São Francisco. This API provides data from the San Francisco Police Department (SFPD). The dataset compiles data from the department's Crime Data Warehouse (CDW) to provide information on accident and crime reports.

## Are incident reports the 'official' count of crimes?
No. While incident reports may serve as a basis for official crime statistics, official crime statistics are governed by the FBI's UCR (Uniform Crime Reporting) and NIBRS (National Incident-Based Reporting System) programs. The most recent version of official UCR/NIBRS statistics released by the SFPD can be found through the California Department of Justice's Open Justice portal.

## What are incident reports?
This dataset includes incident reports recorded from January 1, 2018. These reports are submitted by officers or self-reported by members of the public through the SFPD's online reporting system. The reports are categorized into the following types, based on how they were received and the type of incident:

Initial Reports: the first report filed for an incident.
Supplemental Reports: a follow-up report to an initial report, Coplogic, or vehicle report.
Coplogic Reports: incident reports submitted by members of the public using the SFPD's online reporting system.
Vehicle Reports: incident reports related to stolen and/or recovered vehicles.
All incident reports must be approved by a sergeant or lieutenant supervisor. Once a supervising officer has provided approval through electronic signature, no further changes can be made to the initial report. If changes or additional information are needed or discovered during an investigation, a supplemental report may be generated to capture updates.

For example, a supplemental report may be issued to indicate an arrest made, a missing person found, or to provide additional details of properties taken in a theft. To differentiate between initial and supplemental reports, a filter can be applied to the "Report Type Description" field. Not filtering between initial and supplemental reports may lead to duplicate counting of incidents.

The department uses a Secure File Transfer Protocol (SFTP) protocol to share incident data daily with DataSF.

## Multiple Incident Codes
Incident reports may have one or more associated incident codes. For example, an officer may have a warrant and, upon making the arrest, discovers narcotics in the individual's possession. The officer would record two incident codes: (1) for the warrant and (2) for the discovery of narcotics.

When there are multiple incident codes, the Incident ID, Incident Number, and CAD Numbers remain the same, and the Row ID field can be used as a unique identifier for each data row. An example is provided below.

Incident Datetime	Row ID	Incident ID	Incident Number	CAD Number	Incident Code	Incident Category
1/1/18 13:20	61902222223	60044	180999999	180222222	62050	Warrant
1/1/18 13:20	61903333320	60044	180999999	180222222	16710	Drug Offense

## What is not captured in this dataset?
Incident reports do not necessarily capture all data related to policing and crime. This dataset does not include citations (unless an associated incident report has been written with the citation). For example, a routine speeding ticket generally does not require an incident report; however, a speeding ticket revealing a driver with a warrant resulting in an arrest would require an incident report.

This dataset does not include any identifiable information about any person (suspect, victim, reporting party, officer, witness, etc.). This dataset may not capture other law enforcement incidents within San Francisco (e.g., BART PD, National Park Police, etc.) or reports not submitted to the SFPD.

The information cited above was taken from the official API documentation, which can be read directly on the official page.

[Source](https://datasf.gitbook.io/datasf-dataset-explainers/sfpd-incident-report-2018-to-present)

# Chosen Technologies
For this project, open-source technologies that are widely used in the data engineering market were chosen, considering scalability and the barrier to entry for new participants according to project requirements.

## Python
Python was chosen as the language to act as the Producer that will retrieve information from the source and perform data ingestion directly into the relational database that will store historical data. The language was chosen for its integrations and tools widely used by the data engineering market, facilitating integrations and tasks that need to be performed. The libraries can be seen in the requirements file.

Some libraries were also used to ensure the security and quality of the code. For this, pre-commit was used, allowing the insertion of scripts that are executed when committing to the repository. The scripts used were:

## Pylint
Pylint is a tool for Python that analyzes source code for errors, checks style according to PEP 8, and promotes good programming practices. It helps improve the quality and consistency of Python code by giving a score based on defined rules of good practices for the analyzed code. It was defined for this project that codes with a score below 8 will not be accepted in commits.

## Black
Black is an automatic formatting tool for Python code. It enforces consistent style on the code, eliminating formatting debates. Formatting is applied automatically, making it easier to standardize and improve code readability.

## Pytest
Pytest is a testing library for Python that offers a concise and easy-to-use syntax. It facilitates the writing and execution of automated tests, being widely adopted by the Python developer community.

## Detect-Secrets
Detect-Secrets is a tool used to detect sensitive information, such as passwords, in code repositories. Designed for integration with CI/CD, it helps prevent accidental exposure of secrets in commits.

## Polars
Polars is a data processing library written in Rust, with an interface for Python. It offers efficient and expressive data manipulation operations, being especially suitable for large datasets. Polars is designed to provide fast performance and easy integration with the Python data science ecosystem. In summary, the library simplifies data analysis and manipulation in Python, leveraging Rust's efficiency in the background with higher performance than its direct competitor, Pandas.
Despite the need for several improvements in the Polars environment to reach the maturity level of Pandas, it is still a good choice for projects with a larger data load. In this specific project, there were no significant gains with the choice of Polars over Pandas due to the low volume of data processed and the application's machine configurations.

## Apache Airflow
Apache Airflow is an open-source workflow orchestration platform designed to automate, schedule, and monitor complex tasks in data pipelines. Developed in Python, Airflow allows users to define, schedule, and execute workflows as interactive, code-directed tasks. Its flexible and extensible architecture supports integrations with various data sources and tools, enabling automation of data processes, ETL (Extraction, Transformation, and Loading), report generation, and other operations related to data processing.

## PostgreSQL
PostgreSQL is an open-source relational database management system. It is known for its robustness, extensibility, and compliance with SQL standards. PostgreSQL offers advanced features such as support for custom data types, extensions, triggers, and stored procedures. Additionally, it has a solid concurrency control system and is highly scalable, making it suitable for a variety of applications, from small projects to large enterprise systems.

Although not ideal for a DataWarehouse project, it was chosen for its ease of use, integrations, and ability to handle the low volume of data processed by the application. Considering that the database will not grow exponentially, PostgreSQL will meet the requirements well, with low cost and low barrier to entry.

## Streamlit
Streamlit is an open-source Python library that simplifies the creation of interactive web applications for data analysis and visualization. Designed to be easy to use, Streamlit allows developers to quickly turn simple scripts into interactive web applications without extensive web development knowledge.

With a declarative and minimalist approach, Streamlit makes it easy to create applications with interactive widgets, charts, and tables, all from a single Python script. It supports real-time updates and seamlessly integrates with popular data visualization libraries such as Matplotlib, Plotly, and Altair.

## Docker
Docker is an open-source platform that facilitates the creation, distribution, and execution of applications in containers. Containers are lightweight and independent units that encapsulate an application and all its dependencies, ensuring consistency across different environments.

Docker simplifies the process of development, deployment, and scalability of applications by eliminating inconsistencies between development, testing, and production environments. It allows developers to package an application with its dependencies into a container, ensuring that the application runs the same way in any environment where Docker is installed.

# Engenharia de Dados - Crimes e Acidentes em São Francisco

Status: Em Andamento

Área: Data Engineer

![Untitled](images/Banner.png)

# Descrição

Este projeto tem como objetivo fazer um ciclo completo de um serviço de engenharia de dados simples. O sistema irá consumir dados de uma API pública, armazenar esses dados históricos em um banco de dados estruturado e disponibilizar para o sistema de visualização de dados para análise.

# Arquitetura

![Arquitetura_Sistema](images/Architecture.png)

# API

[API Oficial](https://www.notion.so/Teste-da-api-do-1Password-env-via-1password-d0fa81daf8fa4b65b356d8cd9b303be6?pvs=21) | [Documentação Oficial](https://datasf.gitbook.io/datasf-dataset-explainers/sfpd-incident-report-2018-to-present)

A fonte de dados escolhida para esse projeto foi uma API pública disponibilizada pelo governo da cidade de São Francisco. Essa API disponibiliza dados do Departamento de Polícia de São Francisco (SFPD). O dataset compila dados do Data Warehouse do departamento de Crimes (CDW) para prover informações nos reports de  acidentes e crimes. 

## Os relatórios de incidentes são a contagem 'oficial' de crimes?

Não. Embora os relatórios de incidentes possam servir como base para estatísticas oficiais de criminalidade, as estatísticas oficiais de criminalidade são regidas pelos programas UCR (Uniform Crime Reporting) e NIBRS (National Incident-Based Reporting System) do FBI. A versão mais recente das estatísticas oficiais UCR/NIBRS divulgadas pela SFPD pode ser encontrada por meio do portal Open Justice do Departamento de Justiça da Califórnia.

## O que são relatórios de incidentes?

Este conjunto de dados inclui relatórios de incidentes registrados a partir de 1º de janeiro de 2018. Esses relatórios são apresentados por policiais ou auto informados por membros do público por meio do sistema de relatórios online da SFPD. Os relatórios são categorizados nos seguintes tipos, com base em como foram recebidos e no tipo de incidente:

- **Relatórios Iniciais**: o primeiro relatório registrado para um incidente.
- **Relatórios Suplementares**: um relatório de acompanhamento a um relatório inicial, Coplogic ou relatório de veículo.
- **Relatórios Coplogic**: relatórios de incidentes apresentados por membros do público usando o sistema de relatórios online da SFPD.
- **Relatórios de Veículos**: relatórios de incidentes relacionados a veículos roubados e/ou recuperados.

Todos os relatórios de incidentes devem ser aprovados por um sargento ou tenente supervisor. Uma vez que um oficial supervisor tenha fornecido aprovação por meio de assinatura eletrônica, nenhuma alteração adicional pode ser feita ao relatório inicial. Se mudanças ou informações adicionais forem necessárias ou descobertas durante uma investigação, um relatório suplementar pode ser gerado para capturar atualizações.

Por exemplo, um relatório suplementar pode ser emitido para indicar uma prisão realizada, uma pessoa desaparecida encontrada ou para fornecer detalhes adicionais de propriedades levadas em um furto. Para diferenciar entre os relatórios iniciais e suplementares, um filtro pode ser aplicado ao campo "Descrição do Tipo de Relatório" ("Report Type Description"). Não filtrar entre os relatórios iniciais e suplementares pode levar à contagem duplicada de incidentes.

O departamento utiliza um protocolo de Transferência Segura de Arquivos (SFTP) para compartilhar dados de incidentes diariamente com o DataSF.

## Múltiplos Códigos de Incidente

Relatórios de incidentes podem ter um ou mais códigos de incidente associados. Por exemplo, um policial pode ter um mandado de prisão e, ao realizar a prisão, descobre narcóticos em posse do indivíduo. O policial registraria dois códigos de incidente: (1) para o mandado e (2) para a descoberta de narcóticos.

Quando existem múltiplos códigos de incidente, o ID do Incidente, o Número do Incidente e os Números CAD permanecem os mesmos, e o campo de ID da Linha pode ser usado como um identificador único para cada linha de dados. Um exemplo é fornecido abaixo.

| Incident Datetime | Row ID | Incident ID | Incident Number | CAD Number | Incident Code | Incident Category |
| --- | --- | --- | --- | --- | --- | --- |
| 1/1/18 13:20 | 61902222223 | 60044 | 180999999 | 180222222 | 62050 | Warrant |
| 1/1/18 13:20 | 61903333320 | 60044 | 180999999 | 180222222 | 16710 | Drug Offense |

## O que não é capturado neste conjunto de dados?

Os relatórios de incidentes não capturam necessariamente todos os dados relacionados à polícia e à criminalidade. Este conjunto de dados não inclui citações (a menos que um relatório de incidente associado tenha sido escrito com a citação). Por exemplo, uma multa por excesso de velocidade rotineira geralmente não requer um relatório de incidente; no entanto, uma multa por excesso de velocidade que revele um motorista com um mandado de prisão resultando em uma prisão exigiria um relatório de incidente.

Este conjunto de dados não inclui nenhuma informação identificável de qualquer pessoa (suspeito, vítima, parte que relata, policial, testemunha, etc.). Este conjunto de dados pode não capturar outros incidentes de agências de aplicação da lei dentro de São Francisco (por exemplo, BART PD, Polícia do Parque Nacional, etc.) ou relatórios não apresentados à SFPD.

As informações citadas acima foram retiradas da documentação oficial da API que podem ser lidas diretamente na página oficial.

[Fonte](https://datasf.gitbook.io/datasf-dataset-explainers/sfpd-incident-report-2018-to-present)

# Tecnologias Escolhidas

Para este projeto foram escolhidas tecnologias open source que tem grande uso no mercado de engenharia de dados, pensando em escalabilidade e barreira de entrada de novos participantes de acordo com os requisitos do projeto.

## Python

A linguagem Python foi escolhida para se fazer o papel de Producer que pegará as informações da fonte e fará a ingestão de dados diretamente no banco de dados relacional que armazenará os dados históricos. A linguagem foi escolhida por ter integrações e ferramentas já amplamente utilizadas pelo mercado de engenharia de dados facilitando as integrações e tarefas que devem ser feitas. As bibliotecas podem ser vistas no arquivo de requirements

Algumas bibliotecas também foram utilizadas para garantir a segurança e qualidade do código feito. Para isso foi utilizado o pre-commit que permite inserir scripts que são executados ao dar um commit no repositório. Os scripts utilzados foram:

### Pylint

O Pylint é uma ferramenta para Python que analisa o código-fonte em busca de erros, verifica o estilo conforme o PEP 8 e promove boas práticas de programação. Ele ajuda  a melhorar a qualidade e a consistência do código Python dando uma nota baseado nas regras definidas de boas práticas para o código que está sendo analisado. Foi definido para esse projeto que códigos com nota abaixo de 8 não serão aceitos nos commits.

### Black

Black é uma ferramenta de formatação automática para código Python. Ela impõe um estilo consistente ao código, eliminando debates sobre formatação. A formatação é aplicada automaticamente, facilitando a padronização e a legibilidade do código.

### Pytest

Pytest é uma biblioteca de testes para Python que oferece uma sintaxe concisa e fácil de usar. Facilita a escrita e execução de testes automatizados, sendo amplamente adotada pela comunidade de desenvolvedores Python.

### Detect-Secrets

Detect-Secrets é uma ferramenta utilizada para detectar informações sensíveis, como senhas, em repositórios de código. Projetada para integração com CI/CD, ajuda a evitar a exposição acidental de segredos nos commits.

## Polars

Polars é uma biblioteca de processamento de dados escrita em Rust, com uma interface para Python. Ela oferece operações de manipulação de dados eficientes e expressivas, sendo especialmente adequada para grandes conjuntos de dados. Polars é projetada para proporcionar desempenho rápido e fácil integração com o ecossistema de ferramentas de ciência de dados em Python. Em resumo, a biblioteca simplifica a análise e manipulação de dados em Python, aproveitando a eficiência do Rust nos bastidores com um desempenho e performance maior que a sua concorrente direta o Pandas. 

Apesar de ainda ser necessário várias melhorias no ambiente do Polars para atingir a maturidade do Pandas, ainda é uma boa escolha para projetos com uma carga de dados maior. Nesse projeto, em específico, não houve ganhos significativos com a escolha do Polars frente ao pandas pelo baixo volume de dados trabalhados e as configurações da máquina da aplicação.

## Apache Airflow

O Apache Airflow é uma plataforma de orquestração de fluxo de trabalho open-source, projetada para automatizar, agendar e monitorar tarefas complexas em pipelines de dados. Desenvolvido em Python, o Airflow permite que os usuários definam, programem e executem fluxos de trabalho como tarefas interativas e direcionadas por código. Sua arquitetura flexível e extensível suporta integrações com várias fontes de dados e ferramentas, permitindo a automação de processos de dados, ETL (Extração, Transformação e Carga), geração de relatórios e outras operações relacionadas ao processamento de dados.

## PostgreSql

O PostgreSQL, é um sistema de gerenciamento de banco de dados relacional open-source. Ele é conhecido por sua robustez, extensibilidade e conformidade com os padrões SQL. O PostgreSQL oferece recursos avançados, como suporte a tipos de dados personalizados, extensões, gatilhos e procedimentos armazenados. Além disso, possui um sólido sistema de controle de concorrência e é altamente escalável, tornando-o adequado para uma variedade de aplicações, desde pequenos projetos até grandes sistemas corporativos. 

Apesar de não ser o tipo ideal para um projeto de DataWarehouse, foi escolhido pela facilidade de uso e integrações e por atender bem o baixo volume de dados trabalhados pela aplicação, considerando que a base de dados não irá crescer exponencialmente, o PostgreSQL atenderá bem os requisitos, com baixo custo e baixa barreira de entrada.

## Streamlit

O Streamlit é uma biblioteca de código aberto em Python que simplifica a criação de aplicativos web interativos para análise de dados e visualização. Projetado para ser fácil de usar, o Streamlit permite que os desenvolvedores transformem rapidamente scripts simples em aplicativos web interativos, sem a necessidade de conhecimentos extensivos em desenvolvimento web.

Com uma abordagem declarativa e minimalista, o Streamlit facilita a criação de aplicativos com widgets interativos, gráficos e tabelas, tudo a partir de um único script Python. Ele oferece suporte a atualizações em tempo real e é integrado perfeitamente com bibliotecas populares de visualização de dados, como Matplotlib, Plotly e Altair.

## Docker

O Docker é uma plataforma de código aberto que facilita a criação, distribuição e execução de aplicativos em contêineres. Os contêineres são unidades leves e independentes que encapsulam um aplicativo e todas as suas dependências, garantindo consistência em diferentes ambientes.

O Docker simplifica o processo de desenvolvimento, implantação e escalabilidade de aplicativos, pois elimina inconsistências entre ambientes de desenvolvimento, teste e produção. Ele permite que os desenvolvedores empacotem um aplicativo com suas dependências em um contêiner, garantindo que o aplicativo execute da mesma maneira em qualquer ambiente onde o Docker esteja instalado.
