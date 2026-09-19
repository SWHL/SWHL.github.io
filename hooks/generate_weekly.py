# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Union

def mkdir(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)

def read_txt(txt_path: Union[Path, str]) -> List[str]:
    with open(txt_path, 'r', encoding='utf-8') as f:
        data = [v.rstrip('\n') for v in f]
    return data

def write_txt(save_path: Union[str, Path],
              contents: Union[List[str], str], mode: str = 'w') -> None:
    if not isinstance(contents, list):
        contents = [contents]

    with open(save_path, mode, encoding='utf-8') as f:
        for value in contents:
            f.write(f'{value}\n')

root_dir = Path('docs/weekly/posts')

template_path = root_dir / '_template.md'

tmp_data = read_txt(template_path)

cur_date = datetime.now()
pre_date = (cur_date - timedelta(days=7))
cur_date_str = cur_date.strftime('%Y%m%d')
pre_date_str = pre_date.strftime('%Y%m%d')

tmp_data[1] = tmp_data[1].replace('$1', cur_date_str).replace('$2', pre_date_str)
tmp_data[3] = tmp_data[3].replace('$3', cur_date.strftime('%Y-%m-%d'))
tmp_data[6] = tmp_data[6].replace('$1', cur_date_str).replace('$2', pre_date_str)

save_path = root_dir / f'{pre_date_str}-{cur_date_str}.md'
write_txt(save_path, tmp_data)
print(save_path.resolve())
