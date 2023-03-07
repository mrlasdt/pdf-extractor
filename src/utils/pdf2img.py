#%%
from pathlib import Path
from pdf2image import convert_from_path
from tqdm import tqdm
DATA_DIR = Path("/mnt/ssd500/hungbnt/Cello/data/Allnex")
SAVE_DIR = Path("/mnt/ssd500/hungbnt/Cello/data/AllnexImg")


# %% convert pdf to images
if not SAVE_DIR.is_dir():
    SAVE_DIR.mkdir()
for f in DATA_DIR.glob('*.pdf|*.PDF'):
    SAVE_DIR_SUB = SAVE_DIR.joinpath(f.stem)
    if not SAVE_DIR_SUB.is_dir():
        SAVE_DIR_SUB.mkdir()
    images = convert_from_path(str(f), grayscale=False)
    for i in tqdm(range(len(images))):
        images[i].save(str(SAVE_DIR_SUB.joinpath(f.stem + f'_{i}.jpg')), 'JPEG')  # save only the first pages