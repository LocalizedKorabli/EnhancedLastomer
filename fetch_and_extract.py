import os
from pathlib import Path
import shutil
import zipfile

bin_base_path = Path(r'C:\Games\Korabli\bin')

extracted_path = Path('extracted')

def get_mkmod_path(build_number: int) -> Path:
    return bin_base_path.joinpath(build_number).joinpath('mods').joinpath('UI_BattleFrame_Lastomer.mkmod')

def get_pnfmod_path(build_number: int) -> Path:
    return bin_base_path.joinpath(build_number).joinpath('res_mods').joinpath('PnFMods').joinpath('BattleFrame_Lastomer').joinpath('Main.pyc')

def main():
    build_numbers_list = []

    try:
        build_numbers_list = [num for num in os.listdir(bin_base_path) if num.isnumeric()]
    except Exception as ex:
        print(f'Exception thrown while collecting a list of build numbers: {ex}')

    while True:
        try:
            if build_numbers_list:
                print('Build numbers detected:')
                for num in build_numbers_list:
                    print(num)
            else:
                print('No build number detected.')
            build_number = int(input('Enter the build number: '))
            build_number = str(build_number)
            mkmod_path = get_mkmod_path(build_number)
            pnfmod_path = get_pnfmod_path(build_number)
            if not mkmod_path.is_file():
                print(f'.mkmod not found at {str(mkmod_path.absolute())}')
                continue
            if not pnfmod_path.is_file():
                print(f'Main.pyc not found at {str(pnfmod_path.absolute())}')
                continue
            break
        except ValueError:
            continue

    os.makedirs(extracted_path, exist_ok=True)

    try:
        shutil.rmtree(extracted_path)
    except Exception as ex:
        print(f'Exception thrown while wiping the extracted directory: {ex}')

    # Fetch .mkmod
    with zipfile.ZipFile(mkmod_path, 'r') as zip:
        print('Extracting .mkmod')
        zip.extractall(extracted_path)

    # Fetch .pyc
    print('Fetching Main.pyc...')
    pnfmod_target_path = extracted_path.joinpath('PnFMods').joinpath('BattleFrame_Lastomer')
    os.makedirs(pnfmod_target_path, exist_ok=True)
    shutil.copy(pnfmod_path, pnfmod_target_path)

    # Create an empty file
    with open(extracted_path.joinpath('PnFModsLoader.py'), 'w', encoding='utf-8') as f:
        print(f'Creating an empty \'PnFModsLoader.py\' file at {str(extracted_path.absolute())}...')

try:
    main()
except Exception as ex:
    print(ex)

input('Press Enter to exit.')