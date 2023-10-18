import os
cap_seq = ''
with open('cap_seq.txt') as f:
    for line in f:
        if line[0] == '#' or line.strip() == '':
            continue
        cap_seq = line.strip()

template_seq = ''
with open('template_seq.txt') as f:
    for line in f:
        if line[0] == '#' or line.strip() == '':
            continue
        template_seq = line.strip()

R1R2s = []
with open('R1R2.txt') as f:
    for line in f:
        if line[0] == '#' or line.strip() == '':
            continue
        name, R1R2_dir, R1, R2 = line.strip().split()
        R1R2s.append((name, R1R2_dir, R1, R2))

result_dir = './result/'
os.makedirs(result_dir, exist_ok=True)

bowtie_dir = './result/bowtie/'
os.makedirs(bowtie_dir, exist_ok=True)

match_dir = './result/match/'
os.makedirs(match_dir, exist_ok=True)

merge_dir = './result/merge/'
os.makedirs(merge_dir, exist_ok=True)

merge_both_dir = './result/merge-both/'
os.makedirs(merge_both_dir, exist_ok=True)

def reverse_and_complement(in_seq):
    reverse_seq = in_seq[::-1]
    complement_seq_list = []
    for s in reverse_seq:
        c_s = None
        if s == 'A':
            c_s = 'T'
        elif s == 'T':
            c_s = 'A'
        elif s == 'G':
            c_s = 'C'
        elif s == 'C':
            c_s = 'G'
        elif s == 'N':
            c_s = 'N'
        else:
            print(f'unkown nt: {s}', flush=True)
            exit()
        complement_seq_list.append(c_s)
    return ''.join(complement_seq_list)
