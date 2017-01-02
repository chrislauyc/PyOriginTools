This bug causes Origin to have a HARD CRASH whenever GetData() is called from a column which has NANNUM values. It crashes around 3,000 reads and seems to be cumulative across python scripts.
