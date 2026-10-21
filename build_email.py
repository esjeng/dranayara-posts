"""Monta o e-mail de aprovação (HTML + texto) no mesmo formato usado para @pediatraflavia."""
import json, html, sys

REPO = sys.argv[1] if len(sys.argv) > 1 else "esjeng/dranayara-posts"
REF = sys.argv[2] if len(sys.argv) > 2 else "main"
BASE = f"https://raw.githubusercontent.com/{REPO}/{REF}/posts"
CANVAS = "/tmp/claude-0/-home-claude/7412402b-69f7-5a57-b2e3-dd49cd79411d/scratchpad/canvas/project/canvas.json"

notes = json.load(open(CANVAS))["notes"]

def legenda(key):
    t = notes[key]["text"]
    return t.split("LEGENDA\n", 1)[1].strip() if "LEGENDA\n" in t else t.strip()

def roteiro_html(key):
    t = notes[key]["text"]
    if not t.startswith("ROTEIRO"):
        return ""
    r = t.split("LEGENDA\n", 1)[0].replace("ROTEIRO", "", 1).strip()
    return ('<div style="font-size:12px;color:#888;margin-top:10px">Roteiro de gravação</div>'
            f'<div style="white-space:pre-wrap;font-size:13px;color:#333;background:#f3f5f9;padding:10px 12px;border-radius:8px">{html.escape(r)}</div>')


POSTS = [
    ("2026-10-26-reel-viagem", "Reel · capa + 2 telas + tela final", "Viajou e o intestino ficou em casa?", "Seg 26/10", "VIAGEM", 4, "l1"),
    ("2026-10-27-plicoma-hemorroida", "Carrossel (7 slides)", "Plicoma ou hemorroida? 5 diferenças", "Ter 27/10", "PLICOMA", 7, "l2"),
    ("2026-10-28-reel-crise", "Reel · capa + 2 telas + tela final", "Você faz isso na crise de hemorroida?", "Qua 28/10", "CRISE", 4, "l3"),
    ("2026-10-29-reel-mito-alimentos", "Reel · capa + 2 telas + tela final", "Mito ou verdade: pimenta dá hemorroida?", "Qui 29/10", "ALIMENTOS", 4, "l4"),
    ("2026-10-30-trilha-barriga-inchada", "Carrossel (7 slides) · Método TRILHA", "Barriga inchada todo dia não é normal", "Sex 30/10", "TRILHA", 7, "l5"),
    ("2026-10-31-reel-colonoscopia", "Reel · capa + 2 telas + tela final", "O que mais assusta meus pacientes (colonoscopia)", "Sáb 31/10", "COLONOSCOPIA", 4, "l6"),
    ("2026-11-01-novembro-azul", "Carrossel (3 slides)", "Novembro Azul também é sobre o intestino", "Dom 01/11", "NOVEMBRO AZUL", 3, "l7"),
]

GOLD, NAVY = "#B8893E", "#031634"
blocks = []
for d, tipo, titulo, data, chave, n, lk in POSTS:
    links = " · ".join(f'<a href="{BASE}/{d}/slide-0{i}.jpg">{"Capa" if i == 1 else ("Final" if i == n else f"Slide {i}")}</a>' for i in range(1, n + 1))
    blocks.append(f"""<div style="border:1px solid #e6e1d6;border-radius:14px;padding:16px 18px;margin:18px 0">
<div style="font-size:12px;color:#888;text-transform:uppercase;letter-spacing:.05em">{html.escape(tipo)}</div>
<h3 style="margin:4px 0 6px;color:{NAVY}">{html.escape(titulo)}</h3>
<div style="font-size:14px;margin-bottom:10px">📅 <b>{data}</b> · Para aprovar: <b style="background:#f6ecd9;padding:2px 8px;border-radius:6px">APROVADO {chave}</b></div>
<a href="{BASE}/{d}/preview.jpg"><img src="{BASE}/{d}/preview.jpg" alt="{html.escape(titulo)}" style="width:100%;max-width:600px;border-radius:10px;display:block"></a>
<div style="font-size:14px;margin:8px 0">{links}</div>
{roteiro_html(lk)}<div style="font-size:12px;color:#888;margin-top:10px">Legenda</div>
<div style="white-space:pre-wrap;font-size:13px;color:#333;background:#faf8f3;padding:10px 12px;border-radius:8px">{html.escape(legenda(lk))}</div>
</div>""")

chaves = ", ".join(f"APROVADO {p[4]}" for p in POSTS)
html_body = f"""<div style="font-family:Arial,Helvetica,sans-serif;max-width:640px;color:#2d3142">
<h2 style="color:{GOLD};margin-bottom:4px">Posts para aprovação · Semana 26/10 a 01/11</h2>
<p>Dra. Nayara, seguem os 7 posts da próxima semana: 4 Reels e 3 carrosséis, já na identidade visual do <b>Método TRILHA</b>. Todos os slides finais trazem a sua assinatura, o logo da Proctos e o CRM-MG 48402 / RQE 37264.</p>
<p><b>Para aprovar</b>, responda este e-mail com a palavra de cada post (ex.: <b>APROVADO VIAGEM</b>) ou <b>APROVADO TODOS</b>.<br>
Para mudanças, escreva <b>AJUSTES</b> e o que alterar.</p>
<p style="background:#fdf3e1;border:1px solid #f0d9ae;padding:10px 14px;border-radius:10px;font-size:14px">📸 <b>Sobre as fotos:</b> as suas fotos estão em baixa resolução e, em alguns slides, cortadas, porque foram copiadas da internet. Se você tiver as fotos em alta resolução, o post encaixa muito melhor. Basta responder este e-mail com os arquivos originais que eu atualizo todos os slides.</p>
<p style="font-size:14px">⏰ O primeiro post (<b>Viagem</b>) está previsto para <b>segunda, 26/10</b>. Nos Reels, as imagens são a capa e as telas de texto que entram sobre o vídeo; o roteiro de gravação está em cada bloco.</p>
{''.join(blocks)}
<p style="font-size:13px;color:#777">Só publico o que for aprovado. Clique nas imagens para ver em tamanho real.</p>
</div>"""

text_body = ("Dra. Nayara, seguem os 7 posts da semana 26/10 a 01/11 (4 Reels e 3 carrosséis), na identidade visual do Método TRILHA. "
             f"Para aprovar, responda com a palavra de cada post ({chaves}) ou APROVADO TODOS. Para mudanças, escreva AJUSTES e o que alterar. "
             "Sobre as fotos: estão em baixa resolução e, em alguns slides, cortadas, porque foram copiadas da internet. "
             "Se tiver as fotos em alta resolução, o post encaixa muito melhor; responda com os arquivos originais que eu atualizo os slides. "
             "Os slides e as legendas estão na versão HTML deste e-mail.")

open("/home/claude/dranayara-posts/email.html", "w").write(html_body)
open("/home/claude/dranayara-posts/email.txt", "w").write(text_body)
print(len(html_body), "bytes HTML")
