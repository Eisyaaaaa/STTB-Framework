"""
Sarawak Tech-Trust Barometer (STTB) - Core Survey & Scoring Engine
This module contains the structured 75-question survey database and implements 
the 4-step mathematical scoring formula to compute individual and aggregated 
digital trust indices as defined in Chapter 3.
"""

import numpy as np

# ---------------------------------------------------------
# 1. THE 75-ITEM SURVEY INSTRUMENT DATABASE
# ---------------------------------------------------------

SURVEY_METADATA = {
    "scale": {
        1: "Strongly Disagree",
        2: "Disagree",
        3: "Neutral",
        4: "Agree",
        5: "Strongly Agree"
    },
    "pillars": {
        "P1": {
            "name": "Transparency & Accessibility",
            "islamic_concept": "Sidq (Truthfulness) & Tabayyun (Verification)",
            "definition": "The degree to which digital institutions in Sarawak are open, honest, and accessible in their communication of data usage, policies, and decisions.",
            "variables": {
                "V1.1": "Information Asymmetry",
                "V1.2": "Digital Exclusion",
                "V1.3": "Concealment of Truth"
            }
        },
        "P2": {
            "name": "Ethics & Responsibility",
            "islamic_concept": "Amanah (Trustworthiness) & Stewardship",
            "definition": "The degree to which digital institutions in Sarawak prioritise ethical behaviour, accountability, and responsible governance beyond mere legal compliance.",
            "variables": {
                "V2.1": "Algorithmic Bias",
                "V2.2": "Lack of Accountability",
                "V2.3": "Breach of Amanah"
            }
        },
        "P3": {
            "name": "Privacy & Control",
            "islamic_concept": "Tajassus (Prohibition of Intrusion) & Haya (Dignity/Modesty)",
            "definition": "The degree to which users feel empowered with meaningful agency over their personal information, protected from intrusion, in accordance with PDPA 2010.",
            "variables": {
                "V3.1": "Digital Resignation",
                "V3.2": "Unauthorised Intrusion (Tajassus)",
                "V3.3": "Identity Theft & Data Falsification"
            }
        },
        "P4": {
            "name": "Security & Reliability",
            "islamic_concept": "Itqan (Excellence and Precision)",
            "definition": "The degree to which Sarawak's digital infrastructure and services are technically protected, resilient, and consistently available.",
            "variables": {
                "V4.1": "Systemic Fragility",
                "V4.2": "Frequent Outages",
                "V4.3": "Software Integrity Gaps"
            }
        },
        "P5": {
            "name": "Digital Inclusion & Equity",
            "islamic_concept": "Adl (Justice and Fairness)",
            "definition": "The degree to which digital services, infrastructure, and literacy support are equitably accessible to all communities across Sarawak.",
            "variables": {
                "V5.1": "Geographic Coverage",
                "V5.2": "Digital Literacy Support",
                "V5.3": "Inclusivity for Marginalised Groups"
            }
        }
    }
}

QUESTIONS = [
    # --- PILLAR 1: TRANSPARENCY & ACCESSIBILITY ---
    # Variable 1.1: Information Asymmetry
    {"code": "TA1.1", "pillar": "P1", "variable": "V1.1", "question": "I feel confident that digital platforms in Sarawak can accurately verify my identity to prevent errors or fraud."},
    {"code": "TA1.2", "pillar": "P1", "variable": "V1.1", "question": "I believe there is no 'Information Asymmetry' (gap) between official government reports and independent data sources."},
    {"code": "TA1.3", "pillar": "P1", "variable": "V1.1", "question": "I feel I can easily verify the accuracy and ethics of state-led digital initiatives without relying on external sources."},
    {"code": "TA1.4", "pillar": "P1", "variable": "V1.1", "question": "I trust that the organisation provides information on major plans (e.g., resettlement or project changes) well in advance."},
    {"code": "TA1.5", "pillar": "P1", "variable": "V1.1", "question": "I believe that environmental and land-use data should be made publicly accessible under international standards."},
    
    # Variable 1.2: Digital Exclusion
    {"code": "TA2.1", "pillar": "P1", "variable": "V1.2", "question": "I perceive the current digital government initiatives in Sarawak as being truly 'citizen-centric.'"},
    {"code": "TA2.2", "pillar": "P1", "variable": "V1.2", "question": "I believe digital services in Sarawak are accessible to everyone, ensuring no one is left behind due to a lack of information."},
    {"code": "TA2.3", "pillar": "P1", "variable": "V1.2", "question": "The digital terms and conditions I encounter are written in plain language that allows me to make informed decisions."},
    {"code": "TA2.4", "pillar": "P1", "variable": "V1.2", "question": "I believe that Sarawak is currently at a 'defining moment' regarding how it handles digital trust and inclusion."},
    {"code": "TA2.5", "pillar": "P1", "variable": "V1.2", "question": "In my opinion, digital trust is built more through the effective execution of policies than through strict government regulation alone."},
    
    # Variable 1.3: Concealment of Truth
    {"code": "TA3.1", "pillar": "P1", "variable": "V1.3", "question": "I believe that Sarawak is successfully transitioning from simply 'using technology' to building a 'systemic digital trust' environment."},
    {"code": "TA3.2", "pillar": "P1", "variable": "V1.3", "question": "To what extent do you agree that the organisation is upfront about its business practices and how it uses your data?"},
    {"code": "TA3.3", "pillar": "P1", "variable": "V1.3", "question": "I believe the service provider should follow the principle of Sidq (truthfulness) by not concealing important information."},
    {"code": "TA3.4", "pillar": "P1", "variable": "V1.3", "question": "I am aware of my personal vulnerability to information gaps and identity theft when using digital services in Sarawak."},
    {"code": "TA3.5", "pillar": "P1", "variable": "V1.3", "question": "I am confident that I can rely on official digital platforms in Sarawak for accurate and complete information."},

    # --- PILLAR 2: ETHICS & RESPONSIBILITY ---
    # Variable 2.1: Algorithmic Bias
    {"code": "ER1.1", "pillar": "P2", "variable": "V2.1", "question": "I believe the design and deployment of digital technology in Sarawak are guided by moral principles rather than just profit."},
    {"code": "ER1.2", "pillar": "P2", "variable": "V2.1", "question": "To what extent do you agree that digital platforms in Sarawak contribute positively to social equity and community well-being?"},
    {"code": "ER1.3", "pillar": "P2", "variable": "V2.1", "question": "I trust that the AI and automation used in Sarawak's digital systems remain fair and unbiased in their decision-making."},
    {"code": "ER1.4", "pillar": "P2", "variable": "V2.1", "question": "I trust that local talent (qualified technologists) is being sufficiently developed to protect Sarawak's digital sovereignty."},
    {"code": "ER1.5", "pillar": "P2", "variable": "V2.1", "question": "I feel that digital risks in Sarawak are being addressed with deliberate, coordinated action by institutions."},
    
    # Variable 2.2: Lack of Accountability
    {"code": "ER2.1", "pillar": "P2", "variable": "V2.2", "question": "I feel the organisation prioritises ethical behaviour in its digital operations, even when it is not legally required to do so."},
    {"code": "ER2.2", "pillar": "P2", "variable": "V2.2", "question": "I am confident that the 'Good Governance' frameworks in place effectively monitor the operations of digital platforms in Sarawak."},
    {"code": "ER2.3", "pillar": "P2", "variable": "V2.2", "question": "I believe the leaders (developers and providers) of digital systems in Sarawak feel accountable for my digital welfare."},
    {"code": "ER2.4", "pillar": "P2", "variable": "V2.2", "question": "I am confident that responsibility for data protection is embedded across all levels of the organisations I interact with."},
    {"code": "ER2.5", "pillar": "P2", "variable": "V2.2", "question": "I believe that Sarawak's institutions take deliberate action to address current digital risks rather than waiting for incidents to occur."},
    
    # Variable 2.3: Breach of Amanah
    {"code": "ER3.1", "pillar": "P2", "variable": "V2.3", "question": "I perceive the developers of digital technology in Sarawak as having high Amanah (trustworthiness and responsibility) toward their users."},
    {"code": "ER3.2", "pillar": "P2", "variable": "V2.3", "question": "I trust the organisations managing Sarawak's digital platforms to act as responsible stewards of the community's digital well-being."},
    {"code": "ER3.3", "pillar": "P2", "variable": "V2.3", "question": "I believe that the ethical management of technology in Sarawak reflects a genuine duty of care toward citizens."},
    {"code": "ER3.4", "pillar": "P2", "variable": "V2.3", "question": "I am satisfied with the level of transparency shown by digital institutions in communicating their governance decisions to the public."},
    {"code": "ER3.5", "pillar": "P2", "variable": "V2.3", "question": "I believe that the ethical behaviour of digital service providers in Sarawak fosters long-term community goodwill."},

    # --- PILLAR 3: PRIVACY & CONTROL ---
    # Variable 3.1: Digital Resignation
    {"code": "PC1.1", "pillar": "P3", "variable": "V3.1", "question": "I feel I have a high level of agency (power) over how my personal information is used by digital platforms in Sarawak."},
    {"code": "PC1.2", "pillar": "P3", "variable": "V3.1", "question": "I share my data because I genuinely want to, rather than feeling a sense of 'digital resignation' (feeling I have no real choice)."},
    {"code": "PC1.3", "pillar": "P3", "variable": "V3.1", "question": "I am more likely to engage with Sarawak's digital services because I believe my data is handled responsibly."},
    {"code": "PC1.4", "pillar": "P3", "variable": "V3.1", "question": "I feel that my personal data represents my personal identity, rather than just being information stored on a platform."},
    {"code": "PC1.5", "pillar": "P3", "variable": "V3.1", "question": "I believe that Sarawak's digital institutions take deliberate action to prevent 'digital resignation' among users."},
    
    # Variable 3.2: Unauthorised Intrusion (Tajassus)
    {"code": "PC2.1", "pillar": "P3", "variable": "V3.2", "question": "I trust that digital platforms in Sarawak respect the prohibition of Tajassus (unauthorized spying or intrusion) into my personal life."},
    {"code": "PC2.2", "pillar": "P3", "variable": "V3.2", "question": "I feel that my inherent dignity and modesty (Haya) are respected in the way my personal data is handled by digital platforms."},
    {"code": "PC2.3", "pillar": "P3", "variable": "V3.2", "question": "I trust that organisations in Sarawak do not collect data beyond what is necessary for the services I use."},
    {"code": "PC2.4", "pillar": "P3", "variable": "V3.2", "question": "I feel secure knowing that organisations do not share my data with third parties without my explicit consent."},
    {"code": "PC2.5", "pillar": "P3", "variable": "V3.2", "question": "I believe that digital platforms in Sarawak provide me with granular control over what I choose to disclose versus what I keep private."},
    
    # Variable 3.3: Identity Theft & Data Falsification
    {"code": "PC3.1", "pillar": "P3", "variable": "V3.3", "question": "I am confident that my sensitive data is protected in accordance with Malaysia's Personal Data Protection Act (PDPA) 2010."},
    {"code": "PC3.2", "pillar": "P3", "variable": "V3.3", "question": "I feel safer knowing that organisations in Sarawak use strategic measures such as encryption and audits to prevent data breaches."},
    {"code": "PC3.3", "pillar": "P3", "variable": "V3.3", "question": "I am concerned about the risk of identity theft when using digital services in Sarawak."},
    {"code": "PC3.4", "pillar": "P3", "variable": "V3.3", "question": "I trust that digital service providers in Sarawak proactively work to prevent data falsification and unauthorised alteration of my records."},
    {"code": "PC3.5", "pillar": "P3", "variable": "V3.3", "question": "I believe the existing digital infrastructure in Sarawak is reliable and secure enough to protect my personal data from exploitation."},

    # --- PILLAR 4: SECURITY & RELIABILITY ---
    # Variable 4.1: Systemic Fragility
    {"code": "SR1.1", "pillar": "P4", "variable": "V4.1", "question": "I believe the digital system's infrastructure in Sarawak is robust enough to remain resilient against modern cyber threats."},
    {"code": "SR1.2", "pillar": "P4", "variable": "V4.1", "question": "I am concerned about the rising number of cyber incidents (such as fraud, intrusions, and malicious codes) in the Malaysian digital landscape."},
    {"code": "SR1.3", "pillar": "P4", "variable": "V4.1", "question": "I believe that 'malicious codes' and 'unauthorised intrusions' pose a significant threat to my digital safety in Sarawak."},
    {"code": "SR1.4", "pillar": "P4", "variable": "V4.1", "question": "I feel more confident using digital platforms that are actively monitored by agencies such as CyberSecurity Malaysia."},
    {"code": "SR1.5", "pillar": "P4", "variable": "V4.1", "question": "I believe that a 'Secure and Trusted Environment' is essential for maintaining my confidence in Sarawak's digital initiatives."},
    
    # Variable 4.2: Frequent Outages
    {"code": "SR2.1", "pillar": "P4", "variable": "V4.2", "question": "I expect digital services in Sarawak to be available whenever I need them, without frequent outages or disruptions."},
    {"code": "SR2.2", "pillar": "P4", "variable": "V4.2", "question": "I am satisfied with the high-speed connectivity and infrastructure supporting Sarawak's digital ecosystem."},
    {"code": "SR2.3", "pillar": "P4", "variable": "V4.2", "question": "I feel confident that technology systems in Sarawak are being secured by qualified people rather than just automated software alone."},
    {"code": "SR2.4", "pillar": "P4", "variable": "V4.2", "question": "I believe that digital risks in Sarawak are a present reality that requires immediate technical defence and investment."},
    {"code": "SR2.5", "pillar": "P4", "variable": "V4.2", "question": "I trust that Sarawak's digital infrastructure can support the state's overall digital transformation goals reliably."},
    
    # Variable 4.3: Software Integrity Gaps
    {"code": "SR3.1", "pillar": "P4", "variable": "V4.3", "question": "I trust that this digital platform has adequate measures to protect me from the high financial risks associated with cybercrime in Malaysia."},
    {"code": "SR3.2", "pillar": "P4", "variable": "V4.3", "question": "I feel secure knowing that cutting-edge tools such as encryption, firewalls, and multi-factor authentication (MFA) are implemented to protect my information."},
    {"code": "SR3.3", "pillar": "P4", "variable": "V4.3", "question": "I trust the organisation to proactively identify and rectify software vulnerabilities before they can be exploited."},
    {"code": "SR3.4", "pillar": "P4", "variable": "V4.3", "question": "I perceive the security of digital systems in Sarawak as a reflection of Itqan (pursuing excellence and perfection) in their development."},
    {"code": "SR3.5", "pillar": "P4", "variable": "V4.3", "question": "Seeing certifications like ISO 27001 (for information security) instils greater confidence in me regarding the safety of my data."},

    # --- PILLAR 5: DIGITAL INCLUSION & EQUITY ---
    # Variable 5.1: Geographic Coverage
    {"code": "DI1.1", "pillar": "P5", "variable": "V5.1", "question": "I believe that reliable internet access is available to all communities across Sarawak, including rural and remote areas."},
    {"code": "DI1.2", "pillar": "P5", "variable": "V5.1", "question": "I trust that digital infrastructure development in Sarawak is distributed fairly across all districts and not limited to major urban centres only."},
    {"code": "DI1.3", "pillar": "P5", "variable": "V5.1", "question": "I feel that the cost of digital devices and internet services in Sarawak is affordable for people from all income levels."},
    {"code": "DI1.4", "pillar": "P5", "variable": "V5.1", "question": "I believe that the gap in digital access between urban and rural Sarawak is being actively addressed by the government."},
    {"code": "DI1.5", "pillar": "P5", "variable": "V5.1", "question": "I am confident that Sarawak's digital economy growth benefits all communities equitably, not just those in urban centres."},
    
    # Variable 5.2: Digital Literacy Support
    {"code": "DI2.1", "pillar": "P5", "variable": "V5.2", "question": "I am aware of programmes or initiatives in Sarawak that help people develop the digital skills needed to use online services safely and effectively."},
    {"code": "DI2.2", "pillar": "P5", "variable": "V5.2", "question": "I believe that digital literacy programmes in Sarawak are reaching the communities that need them most, including the elderly and indigenous groups."},
    {"code": "DI2.3", "pillar": "P5", "variable": "V5.2", "question": "I feel confident that I personally have the digital skills needed to safely use and evaluate digital services in Sarawak."},
    {"code": "DI2.4", "pillar": "P5", "variable": "V5.2", "question": "I believe that digital education campaigns in Sarawak adequately prepare citizens to protect themselves online."},
    {"code": "DI2.5", "pillar": "P5", "variable": "V5.2", "question": "I trust that investments in digital literacy in Sarawak will lead to greater public confidence in digital institutions over time."},
    
    # Variable 5.3: Inclusivity for Marginalised Groups
    {"code": "DI3.1", "pillar": "P5", "variable": "V5.3", "question": "I believe that digital services in Sarawak are designed to be accessible and usable by all groups, including the elderly, persons with disabilities, and indigenous communities."},
    {"code": "DI3.2", "pillar": "P5", "variable": "V5.3", "question": "I feel that digital platforms in Sarawak are designed with consideration for users of varying digital literacy levels."},
    {"code": "DI3.3", "pillar": "P5", "variable": "V5.3", "question": "I trust that the principle of Adl (justice and fairness) guides the equitable distribution of digital services across all communities in Sarawak."},
    {"code": "DI3.4", "pillar": "P5", "variable": "V5.3", "question": "I believe that no Sarawakian should be excluded from the benefits of digital transformation due to their location, age, ability, or income."},
]


# ---------------------------------------------------------
# 1.5. SURVEY QUESTIONS TRANSLATIONS (BAHASA MELAYU)
# ---------------------------------------------------------
QUESTIONS_BM = {
    "TA1.1": "Saya berkeyakinan bahawa platform digital di Sarawak dapat mengesahkan identiti saya dengan tepat untuk mencegah ralat atau penipuan.",
    "TA1.2": "Saya percaya tiada 'Asimetri Maklumat' (jurang) antara laporan rasmi kerajaan dengan sumber data bebas.",
    "TA1.3": "Saya rasa saya boleh mengesahkan ketepatan dan etika inisiatif digital pimpinan negeri dengan mudah tanpa bergantung kepada sumber luar.",
    "TA1.4": "Saya percaya bahawa organisasi menyediakan maklumat tentang rancangan utama (cth., penempatan semula atau perubahan projek) lebih awal.",
    "TA1.5": "Saya percaya bahawa data alam sekitar dan guna tanah harus diakses secara terbuka di bawah piawaian antarabangsa.",
    
    "TA2.1": "Saya melihat inisiatif kerajaan digital semasa di Sarawak sebagai benar-benar 'berpusatkan rakyat'.",
    "TA2.2": "Saya percaya perkhidmatan digital di Sarawak boleh diakses oleh semua orang, memastikan tiada siapa yang ketinggalan kerana kekurangan maklumat.",
    "TA2.3": "Terma dan syarat digital yang saya temui ditulis dalam bahasa mudah yang membolehkan saya membuat keputusan termaklum.",
    "TA2.4": "Saya percaya bahawa Sarawak kini berada di 'saat penentu' tentang cara ia mengendalikan kepercayaan dan inklusi digital.",
    "TA2.5": "Pada pendapat saya, kepercayaan digital lebih terbina melalui pelaksanaan dasar yang berkesan berbanding peraturan kerajaan yang ketat semata-mata.",
    
    "TA3.1": "Saya percaya bahawa Sarawak berjaya beralih daripada sekadar 'menggunakan teknologi' kepada membina persekitaran 'kepercayaan digital sistemik'.",
    "TA3.2": "Sejauh manakah anda bersetuju bahawa organisasi bersikap berterus-terang tentang amalan perniagaan mereka dan cara data anda digunakan?",
    "TA3.3": "Saya percaya penyedia perkhidmatan harus mematuhi prinsip Sidq (kebenaran) dengan tidak menyembunyikan maklumat penting.",
    "TA3.4": "Saya sedar tentang kerentanan peribadi saya terhadap jurang maklumat dan kecurian identiti apabila menggunakan perkhidmatan digital di Sarawak.",
    "TA3.5": "Saya yakin bahawa saya boleh bergantung pada platform digital rasmi di Sarawak untuk maklumat yang tepat dan lengkap.",
    
    "ER1.1": "Saya percaya reka bentuk dan penggunaan teknologi digital di Sarawak dipandu oleh prinsip moral dan bukannya keuntungan semata-mata.",
    "ER1.2": "Sejauh manakah anda bersetuju bahawa platform digital di Sarawak menyumbang secara positif kepada kesaksamaan sosial dan kesejahteraan komuniti?",
    "ER1.3": "Saya percaya bahawa AI dan automasi yang digunakan dalam sistem digital Sarawak kekal adil dan tidak berat sebelah dalam membuat keputusan.",
    "ER1.4": "Saya percaya bahawa bakat tempatan (ahli teknologi berkelayakan) sedang dibangunkan secukupnya untuk melindungi kedaulatan digital Sarawak.",
    "ER1.5": "Saya rasa risiko digital di Sarawak sedang ditangani dengan tindakan yang sengaja dan diselaraskan oleh institusi.",
    
    "ER2.1": "Saya rasa organisasi mengutamakan tingkah laku etika dalam operasi digital mereka, walaupun ia tidak diperlukan oleh undang-undang.",
    "ER2.2": "Saya yakin bahawa kerangka 'Tadbir Urus Baik' yang sedia ada berkesan memantau operasi platform digital di Sarawak.",
    "ER2.3": "Saya percaya para pemimpin (pembangun dan penyedia) sistem digital di Sarawak berasa bertanggungjawab terhadap kebajikan digital saya.",
    "ER2.4": "Saya yakin bahawa tanggungjawab untuk perlindungan data diterapkan di semua peringkat organisasi yang saya berinteraksi dengannya.",
    "ER2.5": "Saya percaya bahawa institusi Sarawak mengambil tindakan sengaja untuk menangani risiko digital semasa daripada menunggu insiden berlaku.",
    
    "ER3.1": "Saya melihat pembangun teknologi digital di Sarawak mempunyai Amanah (kebolehpercayaan dan tanggungjawab) yang tinggi terhadap pengguna mereka.",
    "ER3.2": "Saya mempercayai organisasi yang menguruskan platform digital Sarawak untuk bertindak sebagai pentadbir yang bertanggungjawab bagi kesejahteraan digital komuniti.",
    "ER3.3": "Saya percaya bahawa pengurusan teknologi yang beretika di Sarawak mencerminkan kewajipan penjagaan yang tulen terhadap rakyat.",
    "ER3.4": "Saya berpuas hati dengan tahap ketelusan yang ditunjukkan oleh institusi digital dalam menyampaikan keputusan tadbir urus mereka kepada orang ramai.",
    "ER3.5": "Saya percaya bahawa tingkah laku beretika penyedia perkhidmatan digital di Sarawak memupuk hubungan baik komuniti jangka panjang.",
    
    "PC1.1": "Saya rasa saya mempunyai tahap agensi (kuasa) yang tinggi terhadap bagaimana maklumat peribadi saya digunakan oleh platform digital di Sarawak.",
    "PC1.2": "Saya berkongsi data saya kerana saya benar-benar mahu, dan bukannya merasakan 'peletakan jawatan digital' (merasa saya tiada pilihan sebenar).",
    "PC1.3": "Saya lebih cenderung untuk terlibat dengan perkhidmatan digital Sarawak kerana saya percaya data saya dikendalikan secara bertanggungjawab.",
    "PC1.4": "Saya rasa data peribadi saya mewakili identiti peribadi saya, dan bukannya sekadar maklumat yang disimpan di dalam platform.",
    "PC1.5": "Saya percaya bahawa institusi digital Sarawak mengambil tindakan sengaja untuk mengelakkan 'peletakan jawatan digital' dalam kalangan pengguna.",
    
    "PC2.1": "Saya percaya platform digital di Sarawak menghormati larangan Tajassus (mengintip atau pencerobohan tanpa kebenaran) ke dalam kehidupan peribadi saya.",
    "PC2.2": "Saya rasa maruah dan kesopanan (Haya) saya dihormati dalam cara data peribadi saya dikendalikan oleh platform digital.",
    "PC2.3": "Saya percaya bahawa organisasi di Sarawak tidak mengumpul data melebihi apa yang diperlukan untuk perkhidmatan yang saya gunakan.",
    "PC2.4": "Saya merasa selamat mengetahui bahawa organisasi tidak berkongsi data saya dengan pihak ketiga tanpa persetujuan jelas saya.",
    "PC2.5": "Saya percaya platform digital di Sarawak memberikan saya kawalan terperinci terhadap apa yang saya pilih untuk didedahkan berbanding apa yang saya simpan sebagai rahsia.",
    
    "PC3.1": "Saya yakin bahawa data sensitif saya dilindungi mengikut Akta Perlindungan Data Peribadi (PDPA) 2010 Malaysia.",
    "PC3.2": "Saya merasa lebih selamat mengetahui bahawa organisasi di Sarawak menggunakan langkah strategik seperti penyulitan dan audit untuk mencegah pelanggaran data.",
    "PC3.3": "Saya bimbang tentang risiko kecurian identiti apabila menggunakan perkhidmatan digital di Sarawak.",
    "PC3.4": "Saya percaya penyedia perkhidmatan digital di Sarawak berusaha secara proaktif untuk mencegah pemalsuan data dan pengubahan tanpa kebenaran pada rekod saya.",
    "PC3.5": "Saya percaya infrastruktur digital sedia ada di Sarawak adalah cukup dipercayai dan selamat untuk melindungi data peribadi saya daripada eksploitasi.",
    
    "SR1.1": "Saya percaya infrastruktur sistem digital di Sarawak cukup teguh untuk kekal berdaya tahan terhadap ancaman siber moden.",
    "SR1.2": "Saya bimbang tentang peningkatan bilangan insiden siber (seperti penipuan, pencerobohan dan kod berniat jahat) dalam landskap digital Malaysia.",
    "SR1.3": "Saya percaya bahawa 'kod berniat jahat' dan 'pencerobohan tanpa kebenaran' menimbulkan ancaman ketara kepada keselamatan digital saya di Sarawak.",
    "SR1.4": "Saya merasa lebih yakin menggunakan platform digital yang dipantau secara aktif oleh agensi seperti CyberSecurity Malaysia.",
    "SR1.5": "Saya percaya bahawa 'Persekitaran yang Selamat dan Dipercayai' adalah penting untuk mengekalkan keyakinan saya terhadap inisiatif digital Sarawak.",
    
    "SR2.1": "Saya mengharapkan perkhidmatan digital di Sarawak tersedia bila-bila masa saya memerlukannya, tanpa gangguan atau terputus yang kerap.",
    "SR2.2": "Saya berpuas hati dengan ketersambungan berkelajuan tinggi dan infrastruktur yang menyokong ekosistem digital Sarawak.",
    "SR2.3": "Saya merasa yakin bahawa saya secara peribadi mempunyai kemahiran digital yang diperlukan untuk menggunakan dan menilai perkhidmatan digital di Sarawak secara selamat.",
    "SR2.4": "Saya percaya bahawa risiko digital di Sarawak adalah realiti semasa yang memerlukan pertahanan teknikal dan pelaburan segera.",
    "SR2.5": "Saya percaya infrastruktur digital Sarawak dapat menyokong matlamat transformasi digital keseluruhan negeri secara dipercayai.",
    
    "SR3.1": "Saya percaya platform digital ini mempunyai langkah-langkah yang memadai untuk melindungi saya daripada risiko kewangan tinggi berkaitan jenayah siber di Malaysia.",
    "SR3.2": "Saya berasa selamat mengetahui bahawa alat termaju seperti penyulitan, dinding api, dan pengesahan pelbagai faktor (MFA) dilaksanakan untuk melindungi maklumat saya.",
    "SR3.3": "Saya mempercayai organisasi untuk mengenal pasti dan memperbetulkan kelemahan perisian secara proaktif sebelum ia dieksploitasi.",
    "SR3.4": "Saya melihat keselamatan sistem digital di Sarawak sebagai cerminan Itqan (menuntut kecemerlangan dan kesempurnaan) dalam pembangunannya.",
    "SR3.5": "Melihat pensijilan seperti ISO 27001 (untuk keselamatan maklumat) memberikan keyakinan yang lebih besar kepada saya tentang keselamatan data saya.",
    
    "DI1.1": "Saya percaya akses internet yang boleh dipercayai tersedia untuk semua komuniti di seluruh Sarawak, termasuk kawasan luar bandar dan pedalaman.",
    "DI1.2": "Saya percaya pembangunan infrastruktur digital di Sarawak diagihkan secara adil ke seluruh daerah dan tidak terhad kepada pusat bandar utama sahaja.",
    "DI1.3": "Saya rasa kos peranti digital dan perkhidmatan internet di Sarawak adalah berpatutan untuk semua peringkat pendapatan.",
    "DI1.4": "Saya percaya jurang dalam akses digital antara kawasan bandar dan luar bandar Sarawak sedang ditangani secara aktif oleh kerajaan.",
    "DI1.5": "Saya yakin pertumbuhan ekonomi digital Sarawak memberi manfaat kepada semua komuniti secara saksama, bukan sahaja di pusat bandar.",
    
    "DI2.1": "Saya menyedari program atau inisiatif di Sarawak yang membantu orang ramai mengembangkan kemahiran digital yang diperlukan untuk menggunakan perkhidmatan dalam talian secara selamat dan berkesan.",
    "DI2.2": "Saya percaya program literasi digital di Sarawak menjangkau komuniti yang paling memerlukan, termasuk warga emas dan kumpulan peribumi.",
    "DI2.3": "Saya merasa yakin bahawa saya secara peribadi mempunyai kemahiran digital yang diperlukan untuk menggunakan dan menilai perkhidmatan digital di Sarawak secara selamat.",
    "DI2.4": "Saya percaya kempen pendidikan digital di Sarawak menyediakan rakyat dengan mencukupi untuk melindungi diri mereka secara dalam talian.",
    "DI2.5": "Saya percaya pelaburan dalam literasi digital di Sarawak akan membawa kepada keyakinan awam yang lebih besar terhadap institusi digital dari semasa ke semasa.",
    
    "DI3.1": "Saya percaya perkhidmatan digital di Sarawak direka bentuk supaya boleh diakses dan digunakan oleh semua kumpulan, termasuk warga emas, orang kurang upaya, dan komuniti peribumi.",
    "DI3.2": "Saya rasa platform digital di Sarawak direka dengan mengambil kira pengguna pelbagai tahap literasi digital.",
    "DI3.3": "Saya percaya prinsip Adl (keadilan dan kesaksamaan) membimbing pengagihan perkhidmatan digital secara saksama kepada semua komuniti di Sarawak.",
    "DI3.4": "Saya percaya tiada rakyat Sarawak yang harus dikecualikan daripada manfaat transformasi digital kerana lokasi, umur, keupayaan, atau pendapatan mereka.",
    "DI3.5": "Secara keseluruhan, saya berpuas hati bahawa inisiatif digital Sarawak benar-benar bertujuan untuk memastikan tiada komuniti yang ketinggalan."
}


# ---------------------------------------------------------
# 2. MATHEMATICAL SCORING ENGINE IMPLEMENTATION
# ---------------------------------------------------------

def get_trust_level(score):
    """
    Classify the trust score based on STTB thresholds (Table 3.19).
    Returns a dict containing the text level, interpretation, and hex color code.
    """
    if 75.0 <= score <= 100.0:
        return {
            "level": "High Trust",
            "interpretation": "Strong public confidence in digital institutions.",
            "color": "#1E4620",  # Dark Green
            "badge_color": "green"
        }
    elif 50.0 <= score < 75.0:
        return {
            "level": "Moderate Trust",
            "interpretation": "Reasonable but improvable public digital trust.",
            "color": "#7FA334",  # Light Green / Olive-Yellow
            "badge_color": "olive"
        }
    elif 25.0 <= score < 50.0:
        return {
            "level": "Low Trust",
            "interpretation": "Notable trust deficits requiring policy attention.",
            "color": "#E67E22",  # Orange
            "badge_color": "orange"
        }
    else:  # 0.0 <= score < 25.0
        return {
            "level": "Very Low Trust",
            "interpretation": "Severe trust breakdown requiring urgent intervention.",
            "color": "#C0392B",  # Red
            "badge_color": "red"
        }


def calculate_sttb_index(answers):
    """
    Processes raw survey responses through the 4-step mathematical engine.
    
    Parameters:
    - answers: A dict mapping question codes (e.g. 'TA1.1') to Likert values (1 to 5).
               Alternatively, a raw list of answers in the database format.
               
    Returns:
    - A dict containing:
      * variable_means: Dict of {variable_code: value} (1.0 to 5.0)
      * pillar_means: Dict of {pillar_code: value} (1.0 to 5.0)
      * pillar_scores: Dict of {pillar_code: value} (0.0 to 100.0)
      * sttb_index: Float, final aggregate score (0.0 to 100.0)
      * trust_evaluation: Dict containing trust level and colors.
    """
    # Quick validation - check if we have all 75 questions
    missing = [q["code"] for q in QUESTIONS if q["code"] not in answers]
    if missing:
        # If answers are missing, fill them with a default value (3 = Neutral) or raise an error.
        # For flexibility, we fill missing questions with 3.
        for code in missing:
            answers[code] = 3

    # --- Step 1: Variable Means (VM) ---
    # Map questions into variables
    variable_groups = {}
    for q in QUESTIONS:
        key = (q["pillar"], q["variable"])
        if key not in variable_groups:
            variable_groups[key] = []
        variable_groups[key].append(answers[q["code"]])
        
    variable_means = {}
    for key, responses in variable_groups.items():
        pillar_id, var_id = key
        # VM = sum(Q) / 5
        variable_means[f"{pillar_id}_{var_id}"] = float(np.mean(responses))

    # --- Step 2: Pillar Means (PM) ---
    # PM = (VM1 + VM2 + VM3) / 3
    pillar_means = {}
    for p_code in ["P1", "P2", "P3", "P4", "P5"]:
        vars_for_pillar = [v for k, v in variable_means.items() if k.startswith(p_code)]
        pillar_means[p_code] = float(np.mean(vars_for_pillar))

    # --- Step 3: Normalized Pillar Scores (PS) ---
    # PS = [(PM - 1) / 4] * 100
    pillar_scores = {}
    for p_code, pm_val in pillar_means.items():
        ps_val = ((pm_val - 1.0) / 4.0) * 100.0
        pillar_scores[p_code] = round(float(ps_val), 2)

    # --- Step 4: Aggregate STTB Index ---
    # Index = sum(PS) / 5
    sttb_index = float(np.mean(list(pillar_scores.values())))
    sttb_index = round(sttb_index, 2)

    # Get trust levels
    evaluation = get_trust_level(sttb_index)

    return {
        "variable_means": {k: round(v, 2) for k, v in variable_means.items()},
        "pillar_means": {k: round(v, 2) for k, v in pillar_means.items()},
        "pillar_scores": pillar_scores,
        "sttb_index": sttb_index,
        "trust_evaluation": evaluation
    }


# ---------------------------------------------------------
# 3. VERIFICATION UNIT TEST (Section 3.3.2 Worked Example)
# ---------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("STTB SCORING ENGINE: MATHEMATICAL INTEGRITY CHECK")
    print("=" * 60)
    print("This suite runs the worked example described in Section 3.3.2.")
    print("Verifying mathematical algorithms against theoretical framework...")
    print("-" * 60)
    
    # We will simulate a respondent that answers in a way that yields the exact 
    # variable averages of Table 3.20:
    # Pillar 1 (Transparency): VM1.1 = 3.80, VM1.2 = 3.20, VM1.3 = 3.60 -> Expected PM1 = 3.53 -> Expected PS1 = 63.33
    # Pillar 2 (Ethics):       VM2.1 = 2.40, VM2.2 = 3.00, VM2.3 = 2.20 -> Expected PM2 = 2.53 -> Expected PS2 = 38.33
    # Pillar 3 (Privacy):      VM3.1 = 3.20, VM3.2 = 2.80, VM3.3 = 2.60 -> Expected PM3 = 2.87 -> Expected PS3 = 46.67
    # Pillar 4 (Security):     VM4.1 = 3.60, VM4.2 = 3.40, VM4.3 = 3.80 -> Expected PM4 = 3.60 -> Expected PS4 = 65.00
    # Pillar 5 (Inclusion):    VM5.1 = 2.40, VM5.2 = 2.80, VM5.3 = 2.00 -> Expected PM5 = 2.40 -> Expected PS5 = 35.00
    # Expected Aggregate Index = (63.33 + 38.33 + 46.67 + 65.00 + 35.00) / 5 = 49.67 (Low Trust)
    
    # Construct synthetic survey answers corresponding to these variable averages
    # Since each variable mean VM is the average of 5 answers, sum(Q) must equal VM * 5.
    # E.g., for VM1.1 = 3.8, sum(Q) = 19. We can use answers: [4, 4, 4, 4, 3].
    target_vms = {
        ("P1", "V1.1"): 3.8, ("P1", "V1.2"): 3.2, ("P1", "V1.3"): 3.6,
        ("P2", "V2.1"): 2.4, ("P2", "V2.2"): 3.0, ("P2", "V2.3"): 2.2,
        ("P3", "V3.1"): 3.2, ("P3", "V3.2"): 2.8, ("P3", "V3.3"): 2.6,
        ("P4", "V4.1"): 3.6, ("P4", "V4.2"): 3.4, ("P4", "V4.3"): 3.8,
        ("P5", "V5.1"): 2.4, ("P5", "V5.2"): 2.8, ("P5", "V5.3"): 2.0,
    }
    
    synthetic_answers = {}
    for q in QUESTIONS:
        key = (q["pillar"], q["variable"])
        vm = target_vms[key]
        total_needed = int(round(vm * 5))
        # Simple algorithm to distribute total_needed across 5 questions (1 to 5)
        # We index the question to distribute variations
        idx = int(q["code"][-1]) - 1 # 0 to 4
        base_val = total_needed // 5
        remainder = total_needed % 5
        val = base_val + (1 if idx < remainder else 0)
        synthetic_answers[q["code"]] = val

    # Run the scoring engine
    results = calculate_sttb_index(synthetic_answers)

    # Output verification
    worked_pillar_expected = {
        "P1": 63.33,
        "P2": 38.33,
        "P3": 46.67,
        "P4": 65.00,
        "P5": 35.00
    }
    worked_index_expected = 49.67

    passed = True
    print("Verification of Pillar Scores (PS):")
    for p_code, expected_val in worked_pillar_expected.items():
        actual_val = results["pillar_scores"][p_code]
        diff = abs(actual_val - expected_val)
        status = "PASSED" if diff < 0.05 else "FAILED"
        if status == "FAILED":
            passed = False
        print(f" - Pillar {p_code}: Expected={expected_val:.2f}, Actual={actual_val:.2f} [{status}]")

    print("\nVerification of Aggregate STTB Index:")
    actual_index = results["sttb_index"]
    index_diff = abs(actual_index - worked_index_expected)
    index_status = "PASSED" if index_diff < 0.05 else "FAILED"
    if index_status == "FAILED":
        passed = False
    print(f" - STTB Index: Expected={worked_index_expected:.2f}, Actual={actual_index:.2f} [{index_status}]")
    print(f" - Evaluated Trust Level: {results['trust_evaluation']['level']}")
    print(f" - Badge Color Code: {results['trust_evaluation']['color']}")
    print("-" * 60)
    
    if passed:
        print("RESULT: SCORING ENGINE ALGORITHMS VERIFIED successfully!")
    else:
        print("RESULT: SCORING ENGINE VERIFICATION failed. Check math functions.")
    print("=" * 60)
