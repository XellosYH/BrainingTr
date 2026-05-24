import pypdf, os, sys

src = r'C:\Claude_code\progit.pdf'
out_dir = r'C:\Claude_code\research\progit_text'
os.makedirs(out_dir, exist_ok=True)

chapters = {
    'ch1_getting_started': (13, 27),
    'ch2_git_basics': (28, 64),
    'ch3_git_branching': (65, 106),
    'ch5_distributed_git': (127, 168),
    'ch7_git_tools': (219, 335),
}

r = pypdf.PdfReader(src)
print(f'Total pages: {len(r.pages)}')

for name, (start, end) in chapters.items():
    out_path = os.path.join(out_dir, f'{name}.txt')
    with open(out_path, 'w', encoding='utf-8') as f:
        for i in range(start - 1, end):
            text = r.pages[i].extract_text()
            f.write(f'\n\n=== PDF Page {i + 1} ===\n\n')
            f.write(text or '')
    size_kb = os.path.getsize(out_path) // 1024
    print(f'{name}: pages {start}-{end} -> {out_path} ({size_kb} KB)')
