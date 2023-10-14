import os
import sys
from common import *
print(f'************************************************************', flush=True)
print(f'*                 4-valid_seq_alignment.py                 *', flush=True)
print(f'************************************************************', flush=True)

for name, R1R2_dir, R1, R2 in R1R2s:
    print(f'------------------------------------------------------------', flush=True)
    print(f'process R2 -> {R2}', flush=True)
    in_sam = f'{bowtie_dir}/{R2}-clean-without-cap.sam'
    valid_out_f = open(f'{bowtie_dir}/{R2}-valid-alignment.txt', 'w')
    invalid_out_f = open(f'{bowtie_dir}/{R2}-invalid-alignment.txt', 'w')
    align_to_reverse_out_f = open(f'{bowtie_dir}/{R2}-align-to-reverse.txt', 'w')

    # check num of alignments
    num_of_alignments = None
    with open(in_sam) as sam_f:
        num_of_alignments = sum(1 for line in sam_f if line[0] != '@')
        print(f'num of alignments: {num_of_alignments} in {in_sam}', flush=True)

    # filter out seq not have the cap and also check seq id matches
    valid_num = 0
    invalid_num = 0
    align_to_reverse_strand = 0
    with open(in_sam) as sam_f:
        for sam_line in sam_f:
            sam_l = sam_line.strip()
            if sam_l[0] == '@':
                continue
            items = sam_l.split('\t')
            assert(len(items) >= 12)
            seq_id, alignment_flag, pos, seq_without_cap = items[0], items[1], items[3], items[9]
            # print(f'###{seq_id}###{alignment_flag}###{pos}###')
            real_pos = len(template_seq) - int(pos) + 1
            if alignment_flag == '0':
                valid_num += 1
                valid_out_f.write(f'{seq_id}\t{real_pos}\t{seq_without_cap}\n')
            elif alignment_flag == '4':
                invalid_num += 1
                invalid_out_f.write(f'{seq_id}\t{real_pos}\t{seq_without_cap}\n')
            elif alignment_flag == '16':
                align_to_reverse_strand += 1
                align_to_reverse_out_f.write(f'{seq_id}\t{real_pos}\t{seq_without_cap}\n')
    assert((valid_num+invalid_num+align_to_reverse_strand) == num_of_alignments)

    print(f'valid_num: {valid_num} ({valid_num/num_of_alignments*100.0})% invalid_num: {invalid_num} ({invalid_num/num_of_alignments*100.0})% align_to_reverse_num: {align_to_reverse_strand} ({align_to_reverse_strand/num_of_alignments*100.0})%', flush=True)
    valid_out_f.close()
    invalid_out_f.close()
    align_to_reverse_out_f.close()
