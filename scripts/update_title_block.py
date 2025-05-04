from io import SEEK_SET
from os import path, environ
from glob import glob
import re


SRC_PATH = path.join(path.dirname(__file__), "..")
TITLE_BLOCK_AUTHOR = environ["TITLE_BLOCK_AUTHOR"]
TITLE_BLOCK_REVISION = environ["TITLE_BLOCK_REVISION"]
TITLE_BLOCK_DATE = environ["TITLE_BLOCK_DATE"]
TITLE_BLOCK_PROJECT_NAME = environ["TITLE_BLOCK_PROJECT_NAME"]
TITLE_BLOCK_PROJECT_NAME_SHORT = environ["TITLE_BLOCK_PROJECT_NAME_SHORT"]
TITLE_BLOCK_REPOSITORY = environ["TITLE_BLOCK_REPOSITORY"]
TITLE_BLOCK_BASE_REPOSITORY = environ["TITLE_BLOCK_BASE_REPOSITORY"]


def modify_title_block(target: str):
    def replace(target: str, name: str, value: str):
        pattern = re.compile(f'(\\(title_block[\\s\\S]*\\")(\\${{{name}}})(\\")')
        replace_pattern = f"\\g<1>{value}\\g<3>"
        target = pattern.sub(replace_pattern, target)
        return target

    target = replace(target, "TITLE_BLOCK_PROJECT_NAME", TITLE_BLOCK_PROJECT_NAME)
    target = replace(target, "TITLE_BLOCK_DATE", TITLE_BLOCK_DATE)
    target = replace(target, "TITLE_BLOCK_REVISION", TITLE_BLOCK_REVISION)
    target = replace(target, "TITLE_BLOCK_AUTHOR", TITLE_BLOCK_AUTHOR)
    target = replace(target, "TITLE_BLOCK_REPOSITORY", TITLE_BLOCK_REPOSITORY)
    target = replace(
        target, "TITLE_BLOCK_PROJECT_NAME_SHORT", TITLE_BLOCK_PROJECT_NAME_SHORT
    )
    target = replace(target, "TITLE_BLOCK_BASE_REPOSITORY", TITLE_BLOCK_BASE_REPOSITORY)

    return target


def print_title_block():
    print("Modifing title block with following arguments:")
    print(f"\tTITLE_BLOCK_AUTHOR:             {TITLE_BLOCK_AUTHOR}")
    print(f"\tTITLE_BLOCK_BASE_REPOSITORY:    {TITLE_BLOCK_BASE_REPOSITORY}")
    print(f"\tTITLE_BLOCK_REPOSITORY:         {TITLE_BLOCK_REPOSITORY}")
    print(f"\tTITLE_BLOCK_PROJECT_NAME:       {TITLE_BLOCK_PROJECT_NAME}")
    print(f"\tTITLE_BLOCK_PROJECT_NAME_SHORT: {TITLE_BLOCK_PROJECT_NAME_SHORT}")
    print(f"\tTITLE_BLOCK_DATE:               {TITLE_BLOCK_DATE}")
    print(f"\tTITLE_BLOCK_REVISION:           {TITLE_BLOCK_REVISION}")


def main():
    print_title_block()
    for schema_file in glob("*.kicad_sch", root_dir=SRC_PATH):
        print(f"Modifing title block for schematic {schema_file}")
        with open(path.join(SRC_PATH, schema_file), "r") as f:
            file_content = f.read()
        file_content = modify_title_block(file_content)
        with open(path.join(SRC_PATH, schema_file), "w") as f:
            f.write(file_content)

    for board_file in glob("*.kicad_pcb", root_dir=SRC_PATH):
        print(f"Modifing title block for board {board_file}")
        with open(path.join(SRC_PATH, board_file), "r") as f:
            file_content = f.read()
        file_content = modify_title_block(file_content)
        with open(path.join(SRC_PATH, board_file), "w") as f:
            f.write(file_content)


if __name__ == "__main__":
    main()
