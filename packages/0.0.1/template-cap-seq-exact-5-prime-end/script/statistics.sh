#!/bin/bash

while IFS= read -r line
do
    if [[ ${line::1} != "#" ]]
    then
        name=$(echo ${line} | cut -d' ' -f1)
        R1R2_dir=$(echo ${line} | cut -d' ' -f2)
        R1=$(echo ${line} | cut -d' ' -f3)
        R2=$(echo ${line} | cut -d' ' -f4)
        echo ${name} ${R1R2_dir} ${R1} ${R2}

        match_stat="./result/match/${name}_match_statistics.txt"
        nomatch_stat="./result/match/${name}_not_match_statistics.txt"
        merge_stat="./result/merge/${name}_merge_statistics.txt"
        merge_both_stat="./result/merge-both/${name}_merge_statistics.txt"
        :> ${match_stat}
        :> ${nomatch_stat}
        :> ${merge_stat}
        :> ${merge_both_stat}

        for i in {001..357}
        do
            # for match
            if [ -f "./result/match/${name}/matched/${i}/${i}-R1/${R1}" ]; then
                num_of_matched_seq=$(grep "^@" ./result/match/${name}/matched/${i}/${i}-R1/${R1} | wc -l)
            else
                num_of_matched_seq=0
            fi
            if [ -f "./result/match/${name}/not-matched/${i}/${i}-R1/${R1}" ]; then
                num_of_not_matched_seq=$(grep "^@" ./result/match/${name}/not-matched/${i}/${i}-R1/${R1} | wc -l)
            else
                num_of_not_matched_seq=0
            fi
            echo "${i}  ${num_of_matched_seq}" >> ${match_stat}
            echo "${i}  ${num_of_not_matched_seq}" >> ${nomatch_stat}

            # for merge
            if [ -f "./result/merge/${name}/matched/${i}/${i}-R1/${R1}" ]; then
                num_of_merged_seq=$(grep "^@" ./result/merge/${name}/matched/${i}/${i}-R1/${R1} | wc -l)
            else
                num_of_merged_seq=0
            fi
            echo "${i}  ${num_of_merged_seq}" >> ${merge_stat}

            # for merge-both
            if [ -f "./result/merge-both/${name}/matched/${i}/${i}-R1/${R1}" ]; then
                num_of_merged_both_seq=$(grep "^@" ./result/merge-both/${name}/matched/${i}/${i}-R1/${R1} | wc -l)
            else
                num_of_merged_both_seq=0
            fi
            echo "${i}  ${num_of_merged_both_seq}" >> ${merge_both_stat}
        done
    fi
done < R1R2.txt

