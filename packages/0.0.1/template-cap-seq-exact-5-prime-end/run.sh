#!/bin/bash
back_id=`date +"%FT%H%M"`
backup_path="./result-${back_id}"

if [ -d "./result/" ]
then
    if [ "$(ls ./result/ | wc -l)" -gt 1 ]; then
        mv ./result/ ${backup_path}
    fi
fi

mkdir -p ./result/
log='./result/log.txt'
:> ${log}
python ./script/0-decompress.py >> ${log}
python ./script/1-clean.py >> ${log}
python ./script/2-remove_cap.py >> ${log}
python ./script/3-reverse_complement_template_seq_and_align.py >> ${log} 2>&1
python ./script/4-valid_seq_alignment.py >> ${log}
python ./script/5-match_position.py >> ${log}
python ./script/6-merge-seq-with-offset.py >> ${log}
python ./script/7-merge-seq-with-offset-both-matched-and-not-matched.py >> ${log}
bash ./script/statistics.sh >> ${log}
