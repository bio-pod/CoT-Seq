import os
import sys
from common import *
print(f'************************************************************', flush=True)
print(f'*                6-merge-seq-with-offset.py                *', flush=True)
print(f'************************************************************', flush=True)

len_template_seq = len(template_seq)

def append_file_to_file(in_file, out_file):
    if os.path.exists(in_file):
        os.system(f'cat {in_file} >> {out_file}')

for name, R1R2_dir, R1, R2 in R1R2s:
    print(f'------------------------------------------------------------', flush=True)
    print(f'process R1 -> {R1} R2 -> {R2}', flush=True)

    for target_pos in range(1, len_template_seq+1):
        offsets = [0, -1, 1]
        if target_pos == 1:
            offsets = [0, 1]
        if target_pos == len_template_seq:
            offsets = [0, -1]
        out_R1_dir = f'{merge_dir}/{name}/matched/{target_pos:0{len(str(len_template_seq))}d}/{target_pos:0{len(str(len_template_seq))}d}-R1'
        out_R2_dir = f'{merge_dir}/{name}/matched/{target_pos:0{len(str(len_template_seq))}d}/{target_pos:0{len(str(len_template_seq))}d}-R2'
        os.makedirs(out_R1_dir, exist_ok=True)
        os.makedirs(out_R2_dir, exist_ok=True)

        for offset in offsets:
            pos = target_pos + offset
            append_file_to_file(f'{match_dir}/{name}/matched/{pos:0{len(str(len_template_seq))}d}/{pos:0{len(str(len_template_seq))}d}-R1/{R1}', f'{out_R1_dir}/{R1}')
            append_file_to_file(f'{match_dir}/{name}/matched/{pos:0{len(str(len_template_seq))}d}/{pos:0{len(str(len_template_seq))}d}-R2/{R2}', f'{out_R2_dir}/{R2}')
