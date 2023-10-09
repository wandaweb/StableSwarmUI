pushd %~dp0
..\dlbackend\comfy\python_embeded\python.exe -m pip install wget
..\dlbackend\comfy\python_embeded\python.exe install_animate_diff.py
..\dlbackend\comfy\python_embeded\python.exe -m pip install -r ..\dlbackend\comfy\ComfyUI\custom_nodes\comfyui_controlnet_aux\requirements.txt
..\dlbackend\comfy\python_embeded\python.exe -m pip install -r ..\dlbackend\comfy\ComfyUI\custom_nodes\comfyui-animatediff\requirements.txt
popd
pause