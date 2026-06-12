import customtkinter as ctk
import os
import threading
from yt_dlp import YoutubeDL

#Aparencia do App
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DownloaderTGD(ctk.CTk):
    def __init__(self):
        super().__init__()

        #botao de atualização
        self.botao_atualizar = ctk.CTkButton(self, text="Atualizar Aplicação", command=lambda: self.verificar_atualizacao(manual=True), fg_color="#1f538d", hover_color="#14375e")
        self.botao_atualizar.pack(padx=10, pady=10, side="top", anchor="w")

        #janela
        self.title("TGDdownloader")
        self.geometry("500x350")
        self.resizable(False, False) #para o usuario não alterar o tamanho da janela.

        #titulo
        self.titulo = ctk.CTkLabel(self, text="TGDdownloader" , font=ctk.CTkFont(size=22, weight="bold"))
        self.titulo.pack(padx=10, pady=20) #posicionamento
        
        #entrada da url
        self.url_var = ctk.StringVar()
        self.entrada = ctk.CTkEntry(self, width=400, placeholder_text="cole o link aqui", textvariable=self.url_var)
        self.entrada.pack(padx=10, pady=10)

        #texto informativo
        self.Formato_label = ctk.CTkLabel(self, text="escolha o formato do download:")
        self.Formato_label.pack(padx=10, pady=5)

        #Opções do formato (apenas mp3 e mp4 por enquanto)
        self.formato_var = ctk.StringVar(value="Vídeo (MP4)")
        self.menu_formato = ctk.CTkOptionMenu(self, values=["Vídeo (MP4)", "Áudio (MP3)"], variable=self.formato_var)
        self.menu_formato.pack(padx=10, pady=5)

        #barra de progresso com threads
        self.barra_progresso = ctk.CTkProgressBar(self, width=400)
        self.barra_progresso.set(0)

        #botao de download
        self.botao_download = ctk.CTkButton(self, text="Iniciar o download", command=self.baixar_conteudo)
        self.botao_download.pack(padx=10, pady=20)

        #texto do status
        self.status_var = ctk.StringVar(value="Status: Pronto")
        self.label_status = ctk.CTkLabel(self, textvariable=self.status_var)    
        self.label_status.pack(padx=10, pady=10)

    def iniciar_thread(self):
        self.botao_download.configure(state="disabled")
        self.barra_progresso.pack(padx=10, pady=10)
        self.barra_progresso.set(0)
        minha_thread = threading.Thread(target=self.baixar_conteudo)
        minha_thread.start()

    def monitor_progresso(self, d):
        if d['status'] == 'downloading':
            total =d.get('total_bytes') or d.get('total_bytes_estimate')
            baixado = d.get('downloaded_bytes', 0)

            if total:
                porcentagem = baixado / total
                self.barra_progresso.set(porcentagem)

                self.status_var.set(f"Baixando... {int(porcentagem * 100)}%")
                self.update_idletasks()

         
        #Função para o Download
    def baixar_conteudo(self):
        url = self.url_var.get().strip()
        formato = self.formato_var.get()

        if not url: #verifica que não é a url
            self.status_var.set("❌ Digite um link primeiro")
            return
            
        self.status_var.set("Baixando...aguarde⏳")

        #encontrar caminho na pasta
        pasta_destino = os.path.join(os.path.expanduser("~"), "Downloads") 

        #dicionario para as configs do downloader
        if formato == "Áudio (MP3)":
            config_formato = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                    }]
                }
            
        else:
            config_formato = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            }

        ydl_opts = {
            'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
            'progress_hooks': [self.monitor_progresso],
            **config_formato
        }
                        
        #executa o download
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_var.set("✅Concluído! Verifique a pasta de downloads")
        except Exception as e:
            self.status_var.set("❌Erro ao baixar!")
            print(f"Erro: {e}")
        finally:
            self.botao_download.configure(state="normal")
            self.barra_progresso.pack_forget()
    
    def verificar_atualizacao(self, manual=False):
        import subprocess
        import sys

        if manual:
            self.status_var.set("Buscando atualizações...")
            self.update()

        try:
            comando = [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"]
            resultado = subprocess.run(comando, capture_output=True, text=True, check=True)

            if "Requirement already satisfied" in resultado.stdout:
                if manual:
                    self.status_var.set("a aplicação já está na versão mais recente!")
            else:
                if manual:
                    self.status_var.set("aplicação atualizada com sucesso!")
                else:
                    self.status_var.set("a aplicação foi atualizada automaticamente!")

        except Exception as e:
            print(f"Erro ao atualizar: {e}")
            if manual:
                self.status_var.set("Falha ao verificar atualizações.")
            else:
                self.status_var.set("não foi possível checar atualizações.")
        self.update()



        self.verificar_atualizacao(manual=False)
if __name__ == "__main__":
    app = DownloaderTGD()
    app.mainloop()
 