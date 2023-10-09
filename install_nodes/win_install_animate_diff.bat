pushd %~dp0
..\dlbackend\comfy\python_embeded\python.exe -m pip install wget
START /W ..\dlbackend\comfy\python_embeded\python.exe install_animate_diff.py
ECHO Back from ..\dlbackend\comfy\python_embeded\python.exe
..\dlbackend\comfy\python_embeded\python.exe -m pip install -r ..\dlbackend\comfy\ComfyUI\custom_nodes\comfyui_controlnet_aux\requirements.txt
..\dlbackend\comfy\python_embeded\python.exe -m pip install -r ..\dlbackend\comfy\ComfyUI\custom_nodes\ComfyUI-VideoHelperSuite\requirements.txt
..\dlbackend\comfy\python_embeded\python.exe -m pip install -r ..\dlbackend\comfy\ComfyUI\custom_nodes\ComfyUI_FizzNodes\requirements.txt
..\dlbackend\comfy\python_embeded\python.exe -m pip install -r ..\dlbackend\comfy\ComfyUI\custom_nodes\ComfyUI-Advanced-ControlNet\requirements.txt
popd
pause