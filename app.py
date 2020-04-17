from flask import Flask, url_for, session, escape, render_template, redirect, request, send_from_directory
from markupsafe import escape
import time
import uuid
from forms import ContactForm
import os
from PIL import Image, ImageDraw, ImageFont


signatureImage = Image.open("static/templatedip/signature.png").convert("RGBA")
AmaticSC = ImageFont.truetype("static/font/AmaticSC-Bold.ttf",100)
AmaticSCpetit = ImageFont.truetype("static/font/AmaticSC-Bold.ttf",70)
Quicksand = ImageFont.truetype("static/font/Quicksand-Regular.ttf",30)
Sacramento = ImageFont.truetype("static/font/Sacramento-Regular.ttf",80)

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = b'_5#y2L"F4vbzhbvpqhzbQ8z\n\xec]/'

@app.route('/', methods=('GET', 'POST'))
def diplomeform():
	if not 'username' in session:
		session['username'] = uuid.uuid4()
	form = ContactForm()
	if request.method == "POST" :
		now = int(round(time.time() * 1000))
		chemins = []
		anim = form.name.data
		lieu = form.lieu.data
		techno = form.techno.data
		date = form.date.data

		LieuDate = "Fait à "+lieu+" le "+date

		enfants = form.enfants.data.split("\n")
		count = 0
		for enfant in enfants:
			certificat = Image.open("static/templatedip/diplome.png").convert("RGBA")
			#phraseRemise et prenom :
			imagePrenom = ImageDraw.ImageDraw(certificat)
			imagePrenom.text((470,405), "Décerné à "+enfant, font=AmaticSC, fill=(0,0,0))

			#phrase de Stage :
			imageStage = ImageDraw.ImageDraw(certificat)
			imageStage.text((470,530), "pour son stage "+techno, font=AmaticSCpetit, fill=(0,0,0))

			#date et lieu :
			datation = ImageDraw.ImageDraw(certificat)
			datation.text ((770,720), LieuDate, font=Quicksand, fill=(0,0,0))

			#Signature Anim :
			certificat.alpha_composite(signatureImage, dest=(170,850))
			signature = ImageDraw.ImageDraw(certificat)
			signature.text ((340,850), anim, font=Sacramento, fill=(0,0,0))
			nom_dip = str(now)+str(session['username'])+str(count)+".png"
			chemin_dip = os.path.join(app.config['UPLOAD_FOLDER'],nom_dip)

			certificat.save(chemin_dip)
			chemins.append(chemin_dip)
			count+=1
		liste_chemins_str =""	
		for chemin in chemins:
			liste_chemins_str += chemin+","

		return redirect(url_for('success', chemins=liste_chemins_str))

	return render_template('contact.html', form=form)

@app.route('/success', methods=('GET', 'POST'))
def success():	
	chemins = request.args.get("chemins", [])
	chemins = chemins.split(",")
	return render_template('success.html', data=chemins)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
							   filename)

if __name__ == '__main__':
	app.run()