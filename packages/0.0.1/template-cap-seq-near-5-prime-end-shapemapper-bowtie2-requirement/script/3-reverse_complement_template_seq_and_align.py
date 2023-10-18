import os
import sys
from common import *
print(f'************************************************************', flush=True)
print(f'*      3-reverse_complement_template_seq_and_align.py      *', flush=True)
print(f'************************************************************', flush=True)

with open(f'{bowtie_dir}/template_seq_reverse_and_complement.fa', 'w') as f:
    rc_seq = reverse_and_complement(template_seq)
    f.write(">template seq reverse and complement\n")
    for sub_seq in [rc_seq[i:i+70] for i in range(0, len(rc_seq), 70)]:
        f.write(f'{sub_seq}\n')
# bowtie2 build
os.system(f'bowtie2-build {bowtie_dir}/template_seq_reverse_and_complement.fa {bowtie_dir}/template_seq_reverse_and_complement')

# bowtie2 align
for name, R1R2_dir, R1, R2 in R1R2s:
    print(f'------------------------------------------------------------', flush=True)
    print(f'process R2 -> {R2}', flush=True)
    os.system(f'cd {bowtie_dir} ; bowtie2 --local --sensitive-local --ignore-quals --mp 3,1 --rdg 5,1 --rfg 5,1 --dpad 30 -x template_seq_reverse_and_complement -U ../{R2}-without-cap -S {R2}-without-cap.sam -p 24 --reorder')
