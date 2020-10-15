import os

def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

root_files = os.listdir('/')
fs_info_list = []
for f in root_files:
    fs_path = '/' + f
    fs_stat = os.statvfs(fs_path)
    bs1 = fs_stat[0]
    bs2 = fs_stat[1]
    total_blocks = fs_stat[2]
    free_blocks = fs_stat[3]
    info = "%s total=%s free=%s" % (
        fs_path,
        sizeof_fmt(bs1 * total_blocks),
        sizeof_fmt(bs2 * free_blocks)
    )
    fs_info_list.append(info)
    print(info)
