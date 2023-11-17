
from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfMerger
from PIL import Image
import io
import base64

app = Flask(__name__)
CORS(app, origins="http://127.0.0.1:5500")# O, si solo quieres permitir ciertos dominios:
# O, si solo quieres permitir ciertos dominios:
# CORS(app, origins=["http://127.0.0.1:5500", "http://otro-dominio.com"])

@app.route('/merge', methods=['POST'])
def merge():
    try:
        uploaded_files = request.files.getlist('file[]')
        output_filename = request.form.get('nombreArchivo')

        merger = PdfMerger()

        for file in uploaded_files:
            file_data = file.read()
            try:
                # Intenta abrir el archivo como PDF y agregarlo al merger
                pdf_file = io.BytesIO(file_data)
                merger.append(pdf_file)
            except:
                try:
                    # Si no es un PDF, intenta abrirlo como imagen
                    image = Image.open(io.BytesIO(file_data))
                    # Convierte la imagen a PDF y agrega al merger
                    image_pdf = io.BytesIO()
                    image.save(image_pdf, format='PDF', resolution=100.0)
                    merger.append(image_pdf)
                except:
                    return jsonify({"error": "Formato de archivo no admitido."})

        # Guarda el resultado en un nuevo PDF
        output_pdf = io.BytesIO()
        merger.write(output_pdf)
        encoded_file = base64.b64encode(output_pdf.getvalue()).decode('utf-8')

        return jsonify({"message": "Fusión exitosa", "output_filename": output_filename, "output_pdf": encoded_file})

    except Exception as e:
        return jsonify({"error": str(e)})

      

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    CORS(app)
    # CORS(app, origins=["http://127.0.0.1:5500", "http://otro-dominio.com"])
    app.run(debug=True)

