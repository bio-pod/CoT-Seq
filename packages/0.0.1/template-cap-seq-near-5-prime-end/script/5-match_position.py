import os
import sys
from common import *
print(f'************************************************************', flush=True)
print(f'*                    5-match_position.py                   *', flush=True)
print(f'************************************************************', flush=True)

match_num = 8
len_template_seq = len(template_seq)

for name, R1R2_dir, R1, R2 in R1R2s:
    print(f'------------------------------------------------------------', flush=True)
    print(f'process R1 -> {R1} R2 -> {R2}', flush=True)

    # create folders
    for i in range(len_template_seq):
        os.makedirs(f'{match_dir}/{name}/matched/{i+1:0{len(str(len_template_seq))}d}/{i+1:0{len(str(len_template_seq))}d}-R1')
        os.makedirs(f'{match_dir}/{name}/matched/{i+1:0{len(str(len_template_seq))}d}/{i+1:0{len(str(len_template_seq))}d}-R2')
        os.makedirs(f'{match_dir}/{name}/not-matched/{i+1:0{len(str(len_template_seq))}d}/{i+1:0{len(str(len_template_seq))}d}-R1')
        os.makedirs(f'{match_dir}/{name}/not-matched/{i+1:0{len(str(len_template_seq))}d}/{i+1:0{len(str(len_template_seq))}d}-R2')

    # load valid alignment txt
    seq_id_pos_match_str_dict = {}
    num_of_alignment = 0
    with open(f'{bowtie_dir}/{R2}-valid-alignment.txt') as f:
        for line in f:
            seq_id, pos, seq_without_cap = line.strip().split()
            seq_without_cap_match_str = seq_without_cap[:match_num]
            num_of_alignment += 1
            if seq_id not in seq_id_pos_match_str_dict:
                seq_id_pos_match_str_dict[seq_id] = (int(pos), seq_without_cap_match_str)
            else:
                print(f'{seq_id} already in seq_id_pos_match_str_dict', flush=True)
                exit()
    print(f'len(seq_id_pos_match_str_dict) -> {len(seq_id_pos_match_str_dict)}', flush=True)

    in_R1 = f'{result_dir}/{R1}'
    in_R2 = f'{result_dir}/{R2}'

    # check num of lines equal
    with open(in_R1) as R1_f, open(in_R2) as R2_f:
        R1_num_lines = sum(1 for _ in R1_f)
        R2_num_lines = sum(1 for _ in R2_f)
        print(f'R1_num_lines: {R1_num_lines} in {in_R1}', flush=True)
        print(f'R2_num_lines: {R2_num_lines} in {in_R2}', flush=True)
        assert(R1_num_lines == R2_num_lines)
        assert((R1_num_lines % 4) == 0)

    # check seq id, end matches
    matched_num = 0
    not_matched_num = 0
    tmp_entry_lines = None
    with open(in_R1) as R1_f, open(in_R2) as R2_f:
        for R1_line, R2_line in zip(R1_f, R2_f):
            R1_l, R2_l = R1_line.strip(), R2_line.strip()
            if R1_l[0] == '@':
                # analyze tmp_entry_lines
                if tmp_entry_lines != None:
                    assert(len(tmp_entry_lines) == 4)
                    R1_seq, R2_seq = tmp_entry_lines[1][0], tmp_entry_lines[1][1]
                    R1_seq_id, R2_seq_id = tmp_entry_lines[0][0].split()[0][1:], tmp_entry_lines[0][1].split()[0][1:]
                    assert(R1_seq_id == R2_seq_id)
                    cap_start_index = R2_seq.find(cap_seq)
                    if cap_start_index != -1:
                        cap_next_index = cap_start_index + len(cap_seq)
                        R2_end_seq = R2_seq[cap_next_index:cap_next_index+match_num]
                        match_seq = reverse_and_complement(R2_end_seq)
                        if R2_seq_id in seq_id_pos_match_str_dict:
                            pos, R2_end_seq_from_alignment = seq_id_pos_match_str_dict[R2_seq_id]
                            assert(R2_end_seq == R2_end_seq_from_alignment)

                            out_matched_R1 = f'{match_dir}/{name}/matched/{pos:0{len(str(len_template_seq))}d}/{pos:0{len(str(len_template_seq))}d}-R1/{R1}'
                            out_matched_R2 = f'{match_dir}/{name}/matched/{pos:0{len(str(len_template_seq))}d}/{pos:0{len(str(len_template_seq))}d}-R2/{R2}'
                            out_not_matched_R1 = f'{match_dir}/{name}/not-matched/{pos:0{len(str(len_template_seq))}d}/{pos:0{len(str(len_template_seq))}d}-R1/{R1}'
                            out_not_matched_R2 = f'{match_dir}/{name}/not-matched/{pos:0{len(str(len_template_seq))}d}/{pos:0{len(str(len_template_seq))}d}-R2/{R2}'
                            out_matched_R1_f, out_matched_R2_f, out_not_matched_R1_f, out_not_matched_R2_f = open(out_matched_R1, 'a'), open(out_matched_R2, 'a'), open(out_not_matched_R1, 'a'), open(out_not_matched_R2, 'a')

                            if match_seq == template_seq[pos-match_num:pos]:
                                matched_num += 1
                                for out_R1_line, out_R2_line in tmp_entry_lines:
                                    out_matched_R1_f.write(f'{out_R1_line}\n')
                                    out_matched_R2_f.write(f'{out_R2_line}\n')
                            else:
                                not_matched_num += 1
                                for out_R1_line, out_R2_line in tmp_entry_lines:
                                    out_not_matched_R1_f.write(f'{out_R1_line}\n')
                                    out_not_matched_R2_f.write(f'{out_R2_line}\n')
                            out_matched_R1_f.close(), out_matched_R2_f.close(), out_not_matched_R1_f.close(), out_not_matched_R2_f.close()
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
            tmp_entry_lines.append((R1_l,R2_l))
    # deal with last tmp_entry_lines
    if tmp_entry_lines != None:
        assert(len(tmp_entry_lines) == 4)
        R1_seq, R2_seq = tmp_entry_lines[1][0], tmp_entry_lines[1][1]
        R1_seq_id, R2_seq_id = tmp_entry_lines[0][0].split()[0][1:], tmp_entry_lines[0][1].split()[0][1:]
        assert(R1_seq_id == R2_seq_id)
        cap_start_index = R2_seq.find(cap_seq)
        if cap_start_index != -1:
            cap_next_index = cap_start_index + len(cap_seq)
            R2_end_seq = R2_seq[cap_next_index:cap_next_index+match_num]
            match_seq = reverse_and_complement(R2_end_seq)
            if R2_seq_id in seq_id_pos_match_str_dict:
                pos, R2_end_seq_from_alignment = seq_id_pos_match_str_dict[R2_seq_id]
                assert(R2_end_seq == R2_end_seq_from_alignment)

                out_matched_R1 = f'{match_dir}/{name}/matched/{pos:0{len(str(len_template_seq))}d}/{pos:0{len(str(len_template_seq))}d}-R1/{R1}'
                out_matched_R2 = f'{match_dir}/{name}/matched/{pos:0{len(str(len_template_seq))}d}/{pos:0{len(str(len_template_seq))}d}-R2/{R2}'
                out_not_matched_R1 = f'{match_dir}/{name}/not-matched/{pos:0{len(str(len_template_seq))}d}/{pos:0{len(str(len_template_seq))}d}-R1/{R1}'
                out_not_matched_R2 = f'{match_dir}/{name}/not-matched/{pos:0{len(str(len_template_seq))}d}/{pos:0{len(str(len_template_seq))}d}-R2/{R2}'
                out_matched_R1_f, out_matched_R2_f, out_not_matched_R1_f, out_not_matched_R2_f = open(out_matched_R1, 'a'), open(out_matched_R2, 'a'), open(out_not_matched_R1, 'a'), open(out_not_matched_R2, 'a')

                if match_seq == template_seq[pos-match_num:pos]:
                    matched_num += 1
                    for out_R1_line, out_R2_line in tmp_entry_lines:
                        out_matched_R1_f.write(f'{out_R1_line}\n')
                        out_matched_R2_f.write(f'{out_R2_line}\n')
                else:
                    not_matched_num += 1
                    for out_R1_line, out_R2_line in tmp_entry_lines:
                        out_not_matched_R1_f.write(f'{out_R1_line}\n')
                        out_not_matched_R2_f.write(f'{out_R2_line}\n')
                out_matched_R1_f.close(), out_matched_R2_f.close(), out_not_matched_R1_f.close(), out_not_matched_R2_f.close()

    print(f'matched_num -> {matched_num} ({matched_num/(matched_num+not_matched_num)*100.0:.2f}%)  not_matched_num -> {not_matched_num} ({not_matched_num/(matched_num+not_matched_num)*100.0:.2f}%)', flush=True)
