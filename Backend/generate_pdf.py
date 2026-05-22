# -*- coding: utf-8 -*-
"""
Sarawak Tech-Trust Barometer (STTB) - Survey PDF Generator
Creates a professional, academic, print-ready PDF for the Rapid Mini-Survey.
"""

import os
from fpdf import FPDF
import sys

# Append Backend relative path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import survey

class STTBSurveyPDF(FPDF):
    def header(self):
        # Draw top banner border
        self.set_fill_color(0, 51, 102) # Sarawak Dark Blue
        self.rect(0, 0, 210, 10, 'F')
        
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, "SARAWAK TECH-TRUST BAROMETER (STTB)", ln=True, align='C')
        
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "Bilingual Rapid Mini-Survey Form / Borang Tinjauan Mini Pantas Dwibahasa", ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        # Footer text
        self.cell(0, 10, "Sarawak Tech-Trust Barometer (STTB) FYP R&D. PDPA 2010 Compliant. Page " + str(self.page_no()) + "/{nb}", align='C')

def create_survey_pdf(output_path):
    pdf = STTBSurveyPDF(orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # 1. Background info box
    pdf.set_fill_color(245, 246, 249)
    pdf.rect(10, 30, 190, 25, 'F')
    
    pdf.set_xy(12, 32)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 4, "ENG: This rapid mini-survey collects civic opinions regarding digital trust in Sarawak. (Anonymized & Secure)", ln=True)
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(0, 4, "Instruction: Answer all 15 questions by selecting your level of agreement: 1 = Strongly Disagree to 5 = Strongly Agree.", ln=True)
    
    pdf.ln(2)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(0, 4, "BM: Tinjauan mini pantas ini mengumpul pandangan sivik mengenai kepercayaan digital di Sarawak. (Tanpa Nama)", ln=True)
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(0, 4, "Arahan: Jawab semua 15 soalan dengan memilih tahap setuju anda: 1 = Sangat Tidak Setuju ke 5 = Sangat Setuju.", ln=True)
    
    # 2. Demographics Section
    pdf.ln(8)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 6, "1. DEMOGRAPHICS / DEMOGRAFI", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    # Demographic details
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(60, 60, 60)
    
    # Line 1: Age Group & Gender
    pdf.cell(100, 5, "Age Group / Umur:   [  ] 18-24   [  ] 25-34   [  ] 35-44   [  ] 45-54   [  ] 55-64   [  ] 65+", ln=False)
    pdf.cell(90, 5, "Gender / Jantina:   [  ] Male/Lelaki   [  ] Female/Perempuan", ln=True)
    pdf.ln(2)
    
    # Line 2: Occupation & Division
    pdf.cell(100, 5, "Occupation / Pekerjaan:   [  ] Student/Pelajar   [  ] Civil Servant/Awam   [  ] Private/Swasta   [  ] Self/Bekerja Sendiri", ln=False)
    pdf.cell(90, 5, "Sarawak Division / Bahagian: ____________________", ln=True)
    
    # 3. Questions Section
    pdf.ln(6)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 6, "2. EVALUATION ITEMS / ITEM PENILAIAN (15 REPRESENTATIVE ITEMS)", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    variables_featured = [
        "TA1.2", "TA2.2", "TA3.3",  # Pillar 1
        "ER1.3", "ER2.1", "ER3.1",  # Pillar 2
        "PC1.2", "PC2.1", "PC3.1",  # Pillar 3
        "SR1.1", "SR2.2", "SR3.4",  # Pillar 4
        "DI1.1", "DI2.3", "DI3.3",  # Pillar 5
    ]
    
    rep_questions = [q for q in survey.QUESTIONS if q["code"] in variables_featured]
    
    # Mini BM pillars for heading
    bm_pillar_names = {
        "P1": "Ketelusan & Kebolehcapaian",
        "P2": "Etika & Tanggungjawab",
        "P3": "Privasi & Kawalan",
        "P4": "Keselamatan & Kebolehkenyamanan",
        "P5": "Inklusi Digital & Kesaksamaan"
    }
    
    bm_var_names = {
        "V1.1": "Asimetri Maklumat",
        "V1.2": "Pengecualian Digital",
        "V1.3": "Penyembunyian Kebenaran",
        "V2.1": "Bias Algoritma",
        "V2.2": "Kekurangan Kebertanggungjawaban",
        "V2.3": "Pecah Amanah",
        "V3.1": "Kepasrahan Digital",
        "V3.2": "Pencerobohan Tanpa Kebenaran (Tajassus)",
        "V3.3": "Kecurian Identiti & Pemalsuan Data",
        "V4.1": "Kerapuhan Sistemik",
        "V4.2": "Gangguan Perkhidmatan Kerap",
        "V4.3": "Jurang Integriti Perisian",
        "V5.1": "Liputan Geografi",
        "V5.2": "Sokongan Literasi Digital",
        "V5.3": "Inklusiviti untuk Kumpulan Terpinggir"
    }
    
    q_num = 1
    for q in rep_questions:
        # Check height to avoid orphan questions
        if pdf.get_y() > 250:
            pdf.add_page()
            
        p_code = q["pillar"]
        v_code = q["variable"]
        
        p_name_en = survey.SURVEY_METADATA["pillars"][p_code]["name"]
        p_name_bm = bm_pillar_names[p_code]
        
        v_name_en = survey.SURVEY_METADATA["pillars"][p_code]["variables"][v_code]
        v_name_bm = bm_var_names[v_code]
        
        q_en = q["question"]
        q_bm = survey.QUESTIONS_BM[q["code"]]
        
        # Display Pillar/Variable Header
        pdf.set_font('Helvetica', 'B', 8.5)
        pdf.set_text_color(168, 124, 0) # Dark Gold Accent
        pdf.cell(190, 4, f"Pillar: {p_name_en} ({p_name_bm}) - Variable: {v_name_en} ({v_name_bm})", ln=True)
        
        # English Question
        pdf.set_font('Helvetica', '', 9.5)
        pdf.set_text_color(40, 40, 40)
        # Using multi_cell to handle line wraps
        pdf.multi_cell(190, 4.5, f"Q{q_num} (ENG): {q_en}")
        
        # Malay Question
        pdf.set_font('Helvetica', 'I', 9)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(190, 4, f"Q{q_num} (BM): {q_bm}")
        
        # Likert Scale Checkboxes
        pdf.ln(1)
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(80, 80, 80)
        # Custom checkbox spacing
        pdf.cell(8, 5, "", ln=False) # Indent
        pdf.cell(35, 5, "[  ] Strongly Disagree / Sangat Tidak", ln=False)
        pdf.cell(28, 5, "[  ] Disagree / Tidak Setuju", ln=False)
        pdf.cell(22, 5, "[  ] Neutral", ln=False)
        pdf.cell(26, 5, "[  ] Agree / Setuju", ln=False)
        pdf.cell(35, 5, "[  ] Strongly Agree / Sangat Setuju", ln=True)
        pdf.ln(3.5)
        
        q_num += 1
        
    # Save the file
    pdf.output(output_path)
    print(f"Bilingual printable survey PDF successfully generated at: {output_path}")

if __name__ == "__main__":
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Frontend'))
    out_file = os.path.join(out_dir, 'sttb_rapid_survey.pdf')
    create_survey_pdf(out_file)
