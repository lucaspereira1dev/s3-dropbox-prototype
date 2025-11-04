Este projeto é uma aplicação web semelhante ao Dropbox, desenvolvida com Flask e integrada ao Google Cloud Storage (GCP). Permite que usuários façam upload, visualização, download e exclusão de arquivos direto na nuvem.
Recursos

    Dashboard para listar arquivos no bucket do GCP.

    Upload de arquivos via interface web.

    Download de arquivos com links assinados do GCP Storage.

    Exclusão de arquivos da nuvem.

    Feedback para o usuário utilizando flash messages.

    Templates adaptáveis via HTML/Tailwind CSS.

Tecnologias Utilizadas

    Flask: Framework web Python.

    Google Cloud Storage: Armazenamento de arquivos escalável e seguro.

    dotenv: Para gerenciamento de variáveis sensíveis (.env).

    HTML + Tailwind CSS: Para estilização dos templates.

    bucket_helpers: Módulo customizado para abstração das operações de storage no GCP.

Pré-requisitos

    Python 3.8 ou superior

    Conta e projeto configurado no Google Cloud Platform

    Bucket do Google Cloud Storage criado

    Variáveis configuradas no arquivo .env:

        GOOGLE_APPLICATION_CREDENTIALS: Caminho do arquivo de credenciais do GCP

        GCS_BUCKET_NAME: Nome do bucket
