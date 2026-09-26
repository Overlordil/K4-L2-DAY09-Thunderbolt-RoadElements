import csv  
path = 'project/07_blind_handoff/transfer_score.csv'  
with open(path, newline='') as f:  
   rows = list(csv.DictReader(f))  
assert rows, 'CSV tr?ng'  
assert len(rows) == 10, f'expected 10 rows, got {len(rows)}'  
print('validated rows=', len(rows))  
print('correct_counts=', {k: sum(1 for r in rows if r['correct']==k) for k in ['0','1']})  
