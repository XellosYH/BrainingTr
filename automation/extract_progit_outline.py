import pypdf, sys

r = pypdf.PdfReader(r'C:\Claude_code\progit.pdf')
print(f'Total pages: {len(r.pages)}')

# Build page lookup: destination -> page number
page_for_dest = {}
for i, p in enumerate(r.pages):
    page_for_dest[p.indirect_reference.idnum] = i + 1

def walk(items, depth=0, limit_depth=2):
    if depth > limit_depth:
        return
    for it in items:
        if isinstance(it, list):
            walk(it, depth + 1, limit_depth)
        else:
            try:
                title = str(it.title)
                page_num = ''
                try:
                    page_obj = r.get_destination_page_number(it)
                    page_num = f' (p.{page_obj + 1})'
                except Exception:
                    pass
                print('  ' * depth + title + page_num)
            except Exception as e:
                pass

print('--- Outline ---')
walk(r.outline)
