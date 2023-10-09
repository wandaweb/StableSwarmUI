import ctypes
import json
import os
import requests
import subprocess
import sys
import wget
from pathlib import Path

COMFY_SUBFOLDER = "dlbackend/comfy/ComfyUI" if os.name == 'nt' else "dlbackend/ComfyUI"

def run(command):
    subprocess.run(command, shell=True, capture_output=True)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def already_downloaded(url):
    # Check if the file downloaded from the given url exists in the current folder
    filename = url.split('/')[-1]
    if os.path.exists(filename):
        print('Already downloaded: ' + url)
        return True
    else:
        return False

def navigate_to_stableswarm(arguments):
    # Navigates to the StableSwarmUI directory and returns its path

    if len(arguments) >= 2:
        # cd to the provided path
        print(arguments[1])
        directory_path = arguments[1]
        if not os.path.exists(directory_path):
          print(f"Error: The directory '{directory_path}' does not exist.")
          sys.exit(1)
        run(f'cd {directory_path}')
        run(f'pwd')
        parent = directory_path
    elif len(arguments) == 1:
        # If a path is not provided check if StableSwarmUI is the parent folder
        print("Looking for StableSwarmUI")
        parent = os.path.dirname(os.getcwd())
        print(parent)
        found_sln = [file for file in Path(parent).glob("StableSwarmUI.sln") if file.is_file()]
        if not found_sln:
            print("Usage: python install-anim.py <StableSwarmUI_directory_path>")
            sys.exit(1) 
        run(f'cd {parent}')
        run(f'pwd')
    else:
        print("Usage: python install-anim.py <StableSwarmUI_directory_path>")
        sys.exit(1)    

    # Check the ComfyUI directory exists
    comfy_path = parent + "/" + COMFY_SUBFOLDER
    if not os.path.exists(comfy_path):
        print(f"Error: ComfyUI backend not found in {comfy_path}")
        sys.exit(1)

    return parent

if __name__ == "__main__":
  # Get admin privilege on windows to create symlinks
  if os.name == 'nt' and not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
  else:
    f = open('config.json')
    conf = json.load(f)   

    stableswarm_path = navigate_to_stableswarm(sys.argv)
    os.chdir(f'{stableswarm_path}/{COMFY_SUBFOLDER}/custom_nodes')
    
    # Get AnimateDiff
    run(f'git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved')

    # Get the video helper suite
    run(f'git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite')

    # Get FizzNodes for scheduled prompts
    run(f'git clone https://github.com/FizzleDorf/ComfyUI_FizzNodes')

    # Get ControlNet
    run(f'git clone https://github.com/Fannovel16/comfyui_controlnet_aux')
    run(f'git clone https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet')
    
    # Download motion modules
    if (conf['download_motion_modules'] == True):
        foldername = f'{stableswarm_path}/{COMFY_SUBFOLDER}/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/' 
        os.chdir(foldername)
        print(foldername)
        for module_url in conf['motion_modules']:
            if not already_downloaded(module_url):
                print(f'Downloading {module_url}')
                wget.download(module_url, bar=wget.bar_adaptive)
                print('\n')

    # Download Stable Diffusion models
    os.chdir(f'{stableswarm_path}/Models/Stable-Diffusion')
    os.makedirs('checkpoints', exist_ok=True)
    foldername = f'{stableswarm_path}/Models/Stable-Diffusion/checkpoints'
    os.chdir(foldername)
    print(foldername)
    for model in conf['stable_diffusion_checkpoints']:
        if not os.path.exists(model["file_name"]):
            print(f'Downloading {model["file_name"]} from {model["url"]}')
            r = requests.get(model["url"], allow_redirects=True)  
            with open(model["file_name"], 'wb') as f:
                f.write(r.content)
            print('')
        else:
            print(f'File {model["file_name"]} exists.')

    # Download LoRAs
    foldername = f'{stableswarm_path}/Models/Lora'
    os.chdir(foldername)
    print(foldername)
    for model in conf['stable_diffusion_loras']:
        if not os.path.exists(model["file_name"]):
            print(f'Downloading {model["file_name"]} from {model["url"]}')
            r = requests.get(model["url"], allow_redirects=True)  
            with open(model["file_name"], 'wb') as f:
                f.write(r.content)
            print('\n')
        else:
            print(f'File {model["file_name"]} exists.')

    # Download VAE
    foldername = f'{stableswarm_path}/Models/VAE'
    os.chdir(foldername)
    print(foldername)
    for model in conf['vae']:
        if not already_downloaded(model):
            print(f'Downloading {model}')
            wget.download(model, bar=wget.bar_adaptive)
            print('\n')

    # Download Motion LoRAs
    foldername = f'{stableswarm_path}/{COMFY_SUBFOLDER}/custom_nodes/ComfyUI-AnimateDiff-Evolved/loras'
    os.chdir(foldername)
    print(foldername)
    for model in conf['motion_loras']:
        if not already_downloaded(model):
            print(f'Downloading {model}')
            wget.download(model, bar=wget.bar_adaptive)
            print('\n')

    # Install IP Adapter
    foldername = f'{stableswarm_path}/{COMFY_SUBFOLDER}/custom_nodes/'
    os.chdir(foldername)
    print(foldername)
    
    if (conf['ip_adapter']):
        
        # Download the repo
        run(f'git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus')

        # Download the model
        foldername = f'{stableswarm_path}/{COMFY_SUBFOLDER}/custom_nodes/ComfyUI_IPAdapter_plus/models'
        os.chdir(foldername)
        print(foldername)
        for model in conf['ip_adapter_models']:
            if not already_downloaded(model):
                print(f'Downloading {model}')
                wget.download(model, bar=wget.bar_adaptive)
                print('\n')
        
        # Download the clip vision model 
        foldername = f'{stableswarm_path}/Models/clip_vision'
        os.chdir(foldername)
        print(foldername)
        for model in conf['ip_adapter_models']:
            if not already_downloaded(model):
                print(f'Downloading {model}')
                wget.download(model, bar=wget.bar_thermometer)
                print('\n')
        
        # Link IP Adapter output models to a Models folder so they get recognized by StableSwarm
        try:
            os.makedirs(f'{stableswarm_path}/Models/Stable-Diffusion/', exist_ok=True)
            os.symlink(f'{stableswarm_path}/{COMFY_SUBFOLDER}/output/ip_output', f'{stableswarm_path}/Models/Stable-Diffusion/IP-Adapter-Outputs')
        except (FileExistsError):
            print(f"File {stableswarm_path}/Models/Stable-Diffusion/IP-Adapter-Outputs already exists")

    # Link the animations output folder
    try:
        os.makedirs(f'{stableswarm_path}/Output/local/', exist_ok=True)
        os.symlink(f'{stableswarm_path}/{COMFY_SUBFOLDER}/output', f'{stableswarm_path}/Output/local/AnimateDiff')
    except (FileExistsError):
        print(f"File {stableswarm_path}/Output/local/AnimateDiff already exists")

    print("Installation complete.")


