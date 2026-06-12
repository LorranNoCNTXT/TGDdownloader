# TGD Downloader 🚀

Um baixador de vídeos e áudios do YouTube moderno, rápido e com interface gráfica embutida, desenvolvido em Python com `CustomTkinter` e `yt-dlp` rodando em sistemas Linux (Ubuntu).

## ✨ Funcionalidades
* Baixa vídeos na melhor qualidade disponível (.mp4).
* Baixa áudios e converte automaticamente para MP3 de alta qualidade (192kbps).
* **Atualização automática:** O programa verifica se a aplicação está atualizado toda vez que abre! Essa função deve existir, visto que, a biblioteca do Youtube está sempre em atualização por conta de bots.

## 📦 Pré-requisitos
Para rodar este programa, você precisará ter instalado no seu sistema:
* Python 3.10 ou superior
* **FFmpeg** (essencial para a conversão de áudio para MP3)

No Ubuntu/Debian, instale o FFmpeg rodando:
```bash
sudo apt update && sudo apt install ffmpeg -y