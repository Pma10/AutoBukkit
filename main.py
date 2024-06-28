from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo, showerror, askyesno
from Module.get_url import BukkitDownloader
from Module.get_java import get_java
from Module.edit_velocity import update_velocity_settings
import asyncio, subprocess, os
import threading
import shutil

def install_server():
    async def async_install_server():
        java_v = cv_java.get()
        if not os.path.exists("C:/Program Files/Java/" + java_v) or not java_v == "기본":
            return showerror("경고", "설정된 자바 버전이 존재하지 않습니다.")
        bukkit = cmb_bukkit.get()  # 버킷
        version = cv_bukkit.get()  # 버전
        path = cv_bukkit_path.get()  # 경로
        ram = cv_ram.get()  # 램
        desc = cv_desc.get()  # 설명
        image = cv_image.get()  # 이미지
        port = cv_port.get()  # 포트
        white = whitelist.get()  # 화이트리스트
        pb = public.get()  # 공개여부
        cb = cb_al.get()  # 커맨드 블럭
        velocity = cv_velocity.get()  # 벨로시티
        velocity_secret = cv_velocity_secret.get()

        if not version or not path or not ram:
            progress.set(0)
            return showerror("경고", "버킷 설정을 전부 채워주세요.")

        if os.path.exists(path + "/start.bat"):
            rm = askyesno("경고", "이미 서버가 설치되어 있습니다. 덮어쓰시겠습니까?")
            if rm:
                shutil.rmtree(path)
            else:
                return showerror("취소", "서버 설치가 취소되었습니다")

        os.makedirs(path, exist_ok=True)

        bukkit_downloader = BukkitDownloader()

        if bukkit == "Paper":
            url = await bukkit_downloader.get_paper_build(version)
        else:
            url = await bukkit_downloader.get_spigot_build(version)

        if url is None:
            progress.set(0)
            await bukkit_downloader.close()
            return showerror("경고", "존재하지 않는 버전입니다")

        eula = askyesno("EULA", "EULA에 동의하십니까?")
        if not eula:
            progress.set(0)
            await bukkit_downloader.close()
            return showerror("경고", "EULA에 동의해야합니다.")

        with open(f"{path}/eula.txt", "w") as f:
            f.write("eula=true")

        progress.set(20)

        await bukkit_downloader.download(url, f"{path}/server.jar")

        await bukkit_downloader.close()

        progress.set(30)
        if cv_java == "기본":
            with open(f'{path}/start.bat', 'w') as f:
                f.write(f'@echo off\njava -Xms{ram} -Xmx{ram} -jar server.jar -nogui\npause')
        else:
            with open(f'{path}/start.bat', 'w') as f:
                f.write(f'@echo off\n"C:/Program Files/Java/{java_v}/bin/java" -Xms{ram} -Xmx{ram} -jar server.jar -nogui\npause')

        progress.set(40)

        process = subprocess.run(["start.bat"], cwd=path, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input="stop")

        progress.set(90)

        if process.returncode != 0:
            progress.set(0)
            return showerror("경고", "서버를 실행하는데 실패했습니다.")

        server_properties_path = f"{path}/server.properties"
        if not os.path.exists(server_properties_path):
            progress.set(0)
            return showerror("경고", "server.properties 파일을 찾을 수 없습니다. 서버가 제대로 실행되었는지 확인하세요.")

        progress.set(80)

        with open(server_properties_path, "r") as f:
            server_properties = f.read()

        if port:
            server_properties = server_properties.replace("server-port=25565", f"server-port={port}")
        if desc:
            server_properties = server_properties.replace("motd=A Minecraft Server", f"motd={desc}")
        if white == "활성화":
            server_properties = server_properties.replace("white-list=false", "white-list=true")
        if pb == "비활성화":
            server_properties = server_properties.replace("enable-query=false", "enable-query=true")
        if cb == "활성화":
            server_properties = server_properties.replace("enable-command-block=false", "enable-command-block=true")
        if velocity == "활성화" and cv_bukkit == "Paper":
            server_properties = server_properties.replace("online-mode=true", "online-mode=false")
            update_velocity_settings(velocity_secret)

        with open(server_properties_path, "w") as f:
            f.write(server_properties)

        progress.set(100)
        showinfo("알림", "서버가 성공적으로 설치되었습니다.")

    asyncio.run(async_install_server())

def start_installation_thread():
    threading.Thread(target=install_server).start()

root = Tk()
root.title("AutoBukkit")
root.geometry("500x550")

notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10)

bukkit_sel_frame = LabelFrame(notebook, text="버킷 설정")
additional_frame = LabelFrame(notebook, text="추가 설정")
velocity_frame = LabelFrame(notebook, text="Velocity 설정")

notebook.add(bukkit_sel_frame, text="버킷")
notebook.add(additional_frame, text="추가")
notebook.add(velocity_frame, text="Velocity")

progress_frame = LabelFrame(root, text="진행 상황")
progress_frame.pack(padx=10, pady=10, fill="x")

# 버킷 설정
Label(bukkit_sel_frame, text="버킷:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
cmb_bukkit = ttk.Combobox(bukkit_sel_frame, values=["Paper", "Spigot"], state="readonly")
cmb_bukkit.current(0)
cmb_bukkit.grid(row=0, column=1, sticky=W, padx=5, pady=5)

Label(bukkit_sel_frame, text="버전:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
cv_bukkit = Entry(bukkit_sel_frame)
cv_bukkit.grid(row=1, column=1, sticky=W, padx=5, pady=5)

Label(bukkit_sel_frame, text="버킷 경로:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
cv_bukkit_path = Entry(bukkit_sel_frame)
cv_bukkit_path.grid(row=2, column=1, sticky=W, padx=5, pady=5)
btn_bukkit_path = Button(bukkit_sel_frame, text="찾아보기",
                         command=lambda: cv_bukkit_path.insert(0, filedialog.askdirectory()))
btn_bukkit_path.grid(row=2, column=2, sticky=W, padx=5, pady=5)

Label(bukkit_sel_frame, text="램 할당:").grid(row=3, column=0, sticky=W, padx=5, pady=5)
cv_ram = Entry(bukkit_sel_frame)
cv_ram.grid(row=3, column=1, sticky=W, padx=5, pady=5)

Label(bukkit_sel_frame, text="자바 버전 설정:").grid(row=4, column=0, sticky=W, padx=5, pady=5)
cv_java = ttk.Combobox(bukkit_sel_frame, values=get_java(), state="readonly")
cv_java.grid(row=4, column=1, sticky=W, padx=5, pady=5)

btn_install = Button(bukkit_sel_frame, text="서버 설치", command=start_installation_thread)
btn_install.grid(row=5, column=0, columnspan=3, pady=10)

# 추가 설정
Label(additional_frame, text="서버 설명:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
cv_desc = Entry(additional_frame)
cv_desc.grid(row=0, column=1, sticky=W, padx=5, pady=5)

Label(additional_frame, text="서버 이미지:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
cv_image = Entry(additional_frame)
cv_image.grid(row=1, column=1, sticky=W, padx=5, pady=5)
btn_image = Button(additional_frame, text="찾아보기", command=lambda: cv_image.insert(0, filedialog.askopenfilename()))
btn_image.grid(row=1, column=2, sticky=W, padx=5, pady=5)

Label(additional_frame, text="서버 포트:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
cv_port = Entry(additional_frame)
cv_port.grid(row=2, column=1, sticky=W, padx=5, pady=5)

Label(additional_frame, text="화이트리스트:").grid(row=3, column=0, sticky=W, padx=5, pady=5)
whitelist = ttk.Combobox(additional_frame, values=["활성화", "비활성화"], state="readonly")
whitelist.current(1)
whitelist.grid(row=3, column=1, sticky=W, padx=5, pady=5)

Label(additional_frame, text="서버 플레이어 공개 여부:").grid(row=4, column=0, sticky=W, padx=5, pady=5)
public = ttk.Combobox(additional_frame, values=["활성화", "비활성화"], state="readonly")
public.current(0)
public.grid(row=4, column=1, sticky=W, padx=5, pady=5)

Label(additional_frame, text="커맨드 블럭:").grid(row=5, column=0, sticky=W, padx=5, pady=5)
cb_al = ttk.Combobox(additional_frame, values=["활성화", "비활성화"], state="readonly")
cb_al.current(1)
cb_al.grid(row=5, column=1, sticky=W, padx=5, pady=5)

# 진행 상황
progress = IntVar()
progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=400, mode="determinate", variable=progress)
progress_bar.pack(pady=10, padx=5)

# 벨로시티 연결
Label(velocity_frame, text="벨로시티:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
cv_velocity = ttk.Combobox(velocity_frame, values=["활성화", "비활성화"], state="readonly")
cv_velocity.current(1)
cv_velocity.grid(row=0, column=1, sticky=W, padx=5, pady=5)

Label(velocity_frame, text="벨로시티 시크릿:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
cv_velocity_secret = Entry(velocity_frame)
cv_velocity_secret.grid(row=1, column=1, sticky=W, padx=5, pady=5)

root.mainloop()
