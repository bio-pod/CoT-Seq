import os
import sys
from common import *
print(f'cap_seq: {cap_seq}  len: {len(cap_seq)}', flush=True)
print(f'template_seq: {template_seq}  len: {len(template_seq)}', flush=True)
print(f'len(R1R2s): {len(R1R2s)}', flush=True)
print(f'************************************************************', flush=True)
print(f'*                      0-decompress.py                     *', flush=True)
print(f'************************************************************', flush=True)

for name, R1R2_dir, R1, R2 in R1R2s:
    print(f'------------------------------------------------------------', flush=True)
    print(f'process R1 -> {R1} R2 -> {R2}', flush=True)
    in_R1 = f'{R1R2_dir}/{R1}.gz'
    in_R2 = f'{R1R2_dir}/{R2}.gz'
    out_R1 = f'{result_dir}/{R1}'
    out_R2 = f'{result_dir}/{R2}'

    print(f'decompress R1 -> {R1}', flush=True)
    os.system(f'gzip -dkc < {in_R1} > {out_R1}')
    print(f'decompress R2 -> {R2}', flush=True)
    os.system(f'gzip -dkc < {in_R2} > {out_R2}')
