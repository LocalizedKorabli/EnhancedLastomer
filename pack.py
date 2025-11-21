from pathlib import Path
import os
import shutil
import zipfile

mkmod_path = Path('mkmod')
mods_path = Path('mods')
res_mods_path = Path('res_mods')
reference_path = Path('reference')

def main():
    shutil.rmtree(mkmod_path, ignore_errors=True)
    shutil.rmtree(mods_path, ignore_errors=True)
    shutil.rmtree(res_mods_path, ignore_errors=True)
    
    os.makedirs(mkmod_path, exist_ok=True)
    os.makedirs(mods_path, exist_ok=True)
    os.makedirs(res_mods_path, exist_ok=True)
    os.makedirs(reference_path, exist_ok=True)

    ignore_list = shutil.ignore_patterns(
        'PnfModsLoader.py',
        'PnfMods'
    )

    # Copy mkmod contents
    shutil.copytree(reference_path, mkmod_path, ignore=ignore_list, dirs_exist_ok=True)

    # Copy res_mods contents
    shutil.copy(reference_path.joinpath('PnFModsLoader.py'), res_mods_path.joinpath('PnFModsLoader.py'))
    shutil.copytree(reference_path.joinpath('PnFMods'), res_mods_path.joinpath('PnFMods'), dirs_exist_ok=True)

    # Pack mkmod
    with zipfile.ZipFile(mods_path.joinpath('UI_BattleFrame_Lastomer.mkmod'), mode='w', compression=zipfile.ZIP_STORED) as zip:
        for root, dirs, files in os.walk(mkmod_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, mkmod_path)
                zip.write(file_path, arcname=arcname)


try:
    main()
except Exception as ex:
    print(ex)
input('Press Enter to exit.')