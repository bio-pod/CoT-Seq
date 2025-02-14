import os
import sys
from common import *
print(f'************************************************************', flush=True)
print(f'*                      2-remove_cap.py                     *', flush=True)
print(f'************************************************************', flush=True)

for name, R1R2_dir, R1, R2 in R1R2s:
    print(f'------------------------------------------------------------', flush=True)
    print(f'process R2 -> {R2}', flush=True)
    in_R2 = f'{result_dir}/{R2}'
    out_R2 = f'{result_dir}/{R2}-without-cap'
    out_R2_f = open(out_R2, 'w')

    # check num of lines
    R2_num_lines = None
    with open(in_R2) as R2_f:
        R2_num_lines = sum(1 for _ in R2_f)
        print(f'R2_num_lines: {R2_num_lines} in {in_R2}', flush=True)
        assert((R2_num_lines % 4) == 0)

    # filter out seq not have the cap and also check seq id matches
    seq_num = 0
    min_len = 999999999
    max_len = 0
    tmp_entry_lines = None
    with open(in_R2) as R2_f:
        for R2_line in R2_f:
            R2_l = R2_line.strip()
            if R2_l[0] == '@':
                # analyze tmp_entry_lines
                if tmp_entry_lines != None:
                    assert(len(tmp_entry_lines) == 4)
                    R2_seq = tmp_entry_lines[1]
                    quality_values = tmp_entry_lines[3]
                    cap_start_index = R2_seq.find(cap_seq)
                    if cap_start_index != -1:
                        cap_next_index = cap_start_index + len(cap_seq)
                        valid_seq = R2_seq[cap_next_index:]
                        valid_seq_len = len(valid_seq)
                        if valid_seq_len >= 2:
                            seq_num += 1
                            valid_qualities = quality_values[cap_next_index:]
                            assert(len(valid_qualities) == valid_seq_len)
                            if valid_seq_len < min_len:
                                min_len = valid_seq_len
                            if valid_seq_len > max_len:
                                max_len = valid_seq_len
                            out_R2_f.write(f'{tmp_entry_lines[0]}\n')
                            out_R2_f.write(f'{valid_seq}\n')
                            out_R2_f.write(f'{tmp_entry_lines[2]}\n')
                            out_R2_f.write(f'{valid_qualities}\n')
                tmp_entry_lines = []
            tmp_entry_lines.append(R2_l)
    # deal with last tmp_entry_lines
    if tmp_entry_lines != None:
        assert(len(tmp_entry_lines) == 4)
        R2_seq = tmp_entry_lines[1]
        quality_values = tmp_entry_lines[3]
        cap_start_index = R2_seq.find(cap_seq)
        if cap_start_index != -1:
            cap_next_index = cap_start_index + len(cap_seq)
            valid_seq = R2_seq[cap_next_index:]
            valid_seq_len = len(valid_seq)
            if valid_seq_len >= 2:
                seq_num += 1
                valid_qualities = quality_values[cap_next_index:]
                assert(len(valid_qualities) == valid_seq_len)
                if valid_seq_len < min_len:
                    min_len = valid_seq_len
                if valid_seq_len > max_len:
                    max_len = valid_seq_len
                out_R2_f.write(f'{tmp_entry_lines[0]}\n')
                out_R2_f.write(f'{valid_seq}\n')
                out_R2_f.write(f'{tmp_entry_lines[2]}\n')
                out_R2_f.write(f'{valid_qualities}\n')

    print(f'valid seq_num: {seq_num} ({seq_num/(R2_num_lines/4)*100.0:.2f})%  total seq_num: {R2_num_lines/4}', flush=True)
    print(f'min_len: {min_len}  max_len: {max_len}', flush=True)
    out_R2_f.close()
