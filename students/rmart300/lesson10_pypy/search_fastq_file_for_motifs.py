import sys
import re
import operator

def search_fastq_for_motif_patterns_count_mid(fastq_file, pattern1, pattern2):
    mid_count_dict = {}
    search_pattern = re.compile(f"({pattern1})(\w+)({pattern2})")
    with open(fastq_file,'r') as fq:
        for line in fq:
             line = line.strip()
             m = search_pattern.search(line)
             if m:
                 mid = m.group(2)
                 cur_cnt = mid_count_dict.get(mid,0)
                 mid_count_dict[mid] = cur_cnt + 1

    max_hit = None
    max_hit_count = 0
    if len(list(mid_count_dict.keys())) > 0:
        max_hit = max(mid_count_dict.items(), key=operator.itemgetter(1))[0] if len(mid_count_dict.keys()) > 0 else None
        max_hit_count = mid_count_dict[max_hit]

    return max_hit, max_hit_count

if __name__ == '__main__':

    fastq_file = sys.argv[1]
    # motif1 = sys.argv[2]
    # motif2 = sys.argv[3]
    motif1 = 'GTCCGCATGGGT'
    motif2 = 'CTTCAACATGTG'
   
    max_hit, max_hit_count = search_fastq_for_motif_patterns_count_mid(fastq_file, motif1, motif2)

    print(f"max hit is {max_hit} found {max_hit_count} between {motif1} and {motif2}")
