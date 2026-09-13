import io,re,os,tempfile
from flask import Flask,request,render_template_string,send_file
from PIL import Image
from docx import Document
from docx.shared import Pt,Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import pytesseract

app=Flask(__name__)
KD={"क्ष":"{k","त्र":"=","ज्ञ":"K","श्र":"J","अ":"v","आ":"vk","इ":"b","ई":"bZ","उ":"m","ऊ":"Å","ऋ":"_","ए":",","ऐ":",s","ओ":"vks","औ":"vkS","क":"d","ख":"[k","ग":"x","घ":"?","ङ":"³","च":"p","छ":"N","ज":"t","झ":"÷","ञ":"¥","ट":"V","ठ":"B","ड":"M","ढ":"<","ण":".k","त":"r","थ":"Fk","द":"n","ध":"èk","न":"u","प":"i","फ":"Q","ब":"c","भ":"Hk","म":"e","य":";","र":"j","ल":"y","व":"o","श":"'k","ष":".k","स":"l","ह":"g","ा":"k","ि":"f","ी":"h","ु":"q","ू":"w","ृ":"`","े":"s","ै":"S","ो":"ks","ौ":"kS","ं":"a","ः":"%","ँ":"¡","्":"~","़":"़","ॅ":"W","ॉ":"kW","।":"A","॥":"AA"}
def kruti(s):
    for k in sorted(KD,key=len,reverse=True): s=s.replace(k,KD[k])
    return s
def setfont(r,n,z):
    r.font.name=n;r.font.size=Pt(z);p=r._r.get_or_add_rPr();f=p.rFonts
    if f is None:f=OxmlElement("w:rFonts");p.append(f)
    for a in ("ascii","hAnsi","eastAsia","cs"):f.set(qn("w:"+a),n)
def mixed(doc,s):
    p=doc.add_paragraph()
    for c in re.findall(r'[\u0900-\u097F]+|[A-Za-z0-9]+|[^A-Za-z0-9\u0900-\u097F]+',s):
        hi=bool(re.search(r'[\u0900-\u097F]',c));r=p.add_run(kruti(c) if hi else c);setfont(r,"Kruti Dev 010" if hi else "Times New Roman",14 if hi else 12)
def eq_like(s): return bool(re.search(r'(=|≤|≥|≠|≈|∫|∑|√|π|\\frac|\^|[A-Za-z]\s*=\s*|[0-9]+\s*[+\-*/]\s*[0-9]+)',s))
def equation(doc,s):
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;o=OxmlElement("m:oMath");r=OxmlElement("m:r");t=OxmlElement("m:t");t.text=s;r.append(t);o.append(r);p._p.append(o)
def source_image(doc,img):
    b=io.BytesIO();img.save(b,"PNG");b.seek(0);p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run().add_picture(b,width=Inches(6))

HTML=r"""<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Image to DOCX</title><style>body{font-family:system-ui;background:#f5f7fb;margin:0}.wrap{max-width:760px;margin:auto;padding:16px}.card{background:white;padding:20px;border-radius:18px;margin:12px 0;box-shadow:0 4px 20px #0001}input,select,button{width:100%;box-sizing:border-box;padding:14px;margin-top:8px;border-radius:12px;border:1px solid #ccd3df;font-size:16px}button{background:#111827;color:white;font-weight:700}.tag{display:inline-block;background:#eef2ff;padding:7px;margin:3px;border-radius:20px;font-size:13px}</style></head><body><div class="wrap"><div class="card"><h2>📄 Image → DOCX</h2><span class="tag">Kruti Dev 010 / 14</span><span class="tag">Times New Roman / 12</span><span class="tag">Paper-by-paper</span><span class="tag">Word Equation</span></div><div class="card"><input id="files" type="file" accept="image/*" multiple><select id="lang"><option value="hin+eng">Hindi + English</option><option value="hin">Hindi</option><option value="eng">English</option></select><select id="eq"><option value="omml">Editable Word Equation</option><option value="image">Equation as image</option></select><label><input id="src" type="checkbox" style="width:auto"> Keep original paper image</label><button onclick="go()">🚀 Convert to DOCX</button><p id="s"></p></div></div><script>async function go(){let f=document.getElementById('files').files;if(!f.length)return alert('Images चुनें');let d=new FormData();[...f].forEach(x=>d.append('files',x));d.append('lang',lang.value);d.append('eq',eq.value);d.append('src',document.getElementById('src').checked?'1':'0');s.textContent='Processing...';let r=await fetch('/convert',{method:'POST',body:d});if(!r.ok){s.textContent=await r.text();return}let b=await r.blob(),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='converted_kruti_dev_010.docx';a.click();s.textContent='Done';}</script></body></html>"""
@app.get("/")
def home():return render_template_string(HTML)
@app.post("/convert")
def convert():
    files=request.files.getlist("files");lang=request.form.get("lang","hin+eng");mode=request.form.get("eq","omml");keep=request.form.get("src")=="1"
    doc=Document();sec=doc.sections[0];sec.top_margin=Inches(.55);sec.bottom_margin=Inches(.55);sec.left_margin=Inches(.65);sec.right_margin=Inches(.65)
    for i,f in enumerate(files):
        img=Image.open(f.stream).convert("RGB");txt=pytesseract.image_to_string(img,lang=lang,config="--psm 6")
        for line in [x.strip() for x in txt.splitlines() if x.strip()]:
            if mode=="omml" and eq_like(line):equation(doc,line)
            else:mixed(doc,line)
        if keep:source_image(doc,img)
        if i<len(files)-1:doc.add_page_break()
    out=tempfile.NamedTemporaryFile(suffix=".docx",delete=False);out.close();doc.save(out.name)
    return send_file(out.name,as_attachment=True,download_name="converted_kruti_dev_010.docx",mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
if __name__=="__main__":app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
