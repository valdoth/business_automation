from typing import Optional
from fastapi import UploadFile
import io
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

class PDFService:
    @staticmethod
    async def extract_text_from_pdf(pdf_file: UploadFile) -> str:
        """
        Extrait le texte d'un fichier PDF.
        
        Args:
            pdf_file: Le fichier PDF à traiter
            
        Returns:
            str: Le texte extrait du PDF
        """
        # Créer un buffer pour stocker le texte extrait
        output_string = io.StringIO()
        
        # Configurer les paramètres d'extraction
        laparams = LAParams()
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=laparams)
        
        # Lire le contenu du fichier PDF
        pdf_content = await pdf_file.read()
        
        # Créer un buffer pour le contenu PDF
        pdf_buffer = io.BytesIO(pdf_content)
        
        # Extraire le texte
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        extract_text_to_fp(
            pdf_buffer,
            output_string,
            codec='utf-8',
            laparams=laparams,
            output_type='text'
        )
        
        # Fermer les ressources
        device.close()
        output_string.close()
        
        # Retourner le texte extrait
        return output_string.getvalue()

# Exporter la méthode statique pour une utilisation directe
extract_text_from_pdf = PDFService.extract_text_from_pdf 