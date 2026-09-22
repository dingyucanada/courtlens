#!/usr/bin/env python3
"""Choose an already installed rendering runtime; never install packages silently."""
import argparse,os,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def choose_renderer():
 candidates=[os.environ.get('COURTLENS_RENDER_PYTHON'),str(ROOT/'.venv'/('Scripts/python.exe' if os.name=='nt' else 'bin/python3')),sys.executable,str(Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')]
 for candidate in dict.fromkeys(c for c in candidates if c):
  if not Path(candidate).is_file():continue
  try:
   if subprocess.run([candidate,'-c','from PIL import Image,ImageDraw,ImageFont'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=8).returncode==0:return candidate
  except (OSError,subprocess.TimeoutExpired):continue
 return sys.executable
if __name__=='__main__':
 renderer=choose_renderer()
 parser=argparse.ArgumentParser(add_help=False)
 parser.add_argument('--port',type=int,default=8765)
 parser.add_argument('--workspace',default=str(ROOT/'workspace'))
 options,_=parser.parse_known_args()
 print(f'CourtLens 本机项目工作区：http://127.0.0.1:{options.port}/projects.html\n停止服务请按 Ctrl+C。项目保存在 {options.workspace}。',flush=True)
 os.execv(sys.executable,[sys.executable,str(ROOT/'server.py'),'--render-python',renderer,*sys.argv[1:]])
