import os
import sys
from common import *
print(f'************************************************************', flush=True)
print(f'*                        1-clean.py                        *', flush=True)
print(f'************************************************************', flush=True)

for name, R1R2_dir, R1, R2 in R1R2s:
    print(f'------------------------------------------------------------', flush=True)
    print(f'process R1 -> {R1} R2 -> {R2}', flush=True)
    in_R1 = f'{result_dir}/{R1}'
    in_R2 = f'{result_dir}/{R2}'
    out_R1 = f'{result_dir}/{R1}-clean'
    out_R2 = f'{result_dir}/{R2}-clean'
    out_R1_f = open(out_R1, 'w')
    out_R2_f = open(out_R2, 'w')

    # check num of lines equal
    with open(in_R1) as R1_f, open(in_R2) as R2_f:
        R1_num_lines = sum(1 for _ in R1_f)
        R2_num_lines = sum(1 for _ in R2_f)
        print(f'R1_num_lines: {R1_num_lines} in {in_R1}', flush=True)
        print(f'R2_num_lines: {R2_num_lines} in {in_R2}', flush=True)
        assert(R1_num_lines == R2_num_lines)
        assert((R1_num_lines % 4) == 0)

    # filter out seq not have the cap and also check seq id matches
    seq_id_list = []
    tmp_entry_lines = None
    valid_seq_num = 0
    with open(in_R1) as R1_f, open(in_R2) as R2_f:
        for R1_line, R2_line in zip(R1_f, R2_f):
            R1_l, R2_l = R1_line.strip(), R2_line.strip()
            if R1_l[0] == '@':
                # analyze tmp_entry_lines
                if tmp_entry_lines != None:
                    assert(len(tmp_entry_lines) == 4)
                    R1_seq, R2_seq = tmp_entry_lines[1][0], tmp_entry_lines[1][1]
                    if R2_seq[:len(cap_seq)] == cap_seq:
                        #if R1_seq.find('N') == -1 and R2_seq.find('N') == -1:
                        valid_seq_num += 1
                        for out_R1_line, out_R2_line in tmp_entry_lines:
                            out_R1_f.write(f'{out_R1_line}\n')
                            out_R2_f.write(f'{out_R2_line}\n')
                tmp_entry_lines = []
                # check seq id match
                assert(R2_l[0] == '@')
                R1_id_items = R1_l.split()
                R2_id_items = R2_l.split()
                assert(len(R1_id_items) == 2)
                assert(len(R2_id_items) == 2)
                R1_id_str = R1_id_items[0] + ' ' + R1_id_items[1][2:]
                R2_id_str = R2_id_items[0] + ' ' + R2_id_items[1][2:]
                if R1_id_str != R2_id_str:
                    print(f'mismatch id: {R1_id_str} -> {R2_id_str}', flush=True)
                    exit()
                seq_id_list.append(R1_id_str)
            tmp_entry_lines.append((R1_l,R2_l))
    # deal with last tmp_entry_lines
    if tmp_entry_lines != None:
        assert(len(tmp_entry_lines) == 4)
        R1_seq, R2_seq = tmp_entry_lines[1][0], tmp_entry_lines[1][1]
        if R2_seq[:len(cap_seq)] == cap_seq:
            #if R1_seq.find('N') == -1 and R2_seq.find('N') == -1:
            valid_seq_num += 1
            for out_R1_line, out_R2_line in tmp_entry_lines:
                out_R1_f.write(f'{out_R1_line}\n')
                out_R2_f.write(f'{out_R2_line}\n')
    assert((R1_num_lines / 4) == len(seq_id_list))
    print(f'num: {len(seq_id_list)} seqs', flush=True)
    seq_id_set = set(seq_id_list)
    print(f'len(seq_id_list) -> {len(seq_id_list)} len(seq_id_set) -> {len(seq_id_set)}', flush=True)
    assert(len(seq_id_list) == len(set(seq_id_list)))
    print(f'valid_seq_num: {valid_seq_num} ({valid_seq_num/len(seq_id_list)*100.0})%', flush=True)
    out_R1_f.close()
    out_R2_f.close()

    # os.system(f'rm {in_R1}')
    # os.system(f'rm {in_R2}')
