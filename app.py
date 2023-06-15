import streamlit as st
import pandas as pd
import numpy as np
import pickle

clf = pickle.load(open('model.sav','rb'))

st.set_page_config(page_title="Shrimp Disease App")

input_dict = {}

st.title('Shrimp Disease Classification')

with st.expander("Identity"):
    nama = st.text_input("Nama")
    kolam = st.text_input("Lokasi kolam")

with st.expander("Ciri-ciri fisik"):
    foto = st.camera_input("Foto")

    warna = st.multiselect(
        "Warna",
        options=[
            'Putih',
            'Bening',
            'Pucat',
            'Gelap',
            'Ekor berwarna merah']
        )
        
    input_dict['warna_putih'] = 1 if ('Putih' in warna) else 0
    input_dict['warna_bening'] = 1 if ('Bening' in warna) else 0
    input_dict['warna_pucat'] = 1 if ('Pucat' in warna) else 0
    input_dict['warna_gelap'] = 1 if ('Gelap' in warna) else 0
    input_dict['warna_ekor_merah'] = 1 if ('Ekor berwarna merah' in warna) else 0

    kulit = st.selectbox(
        "Kulit",
        options=[
            'Ada bintik putih',
            'Ada bintik hitam',
            'Tidak ada bintik'
        ]
    )

    input_dict['kulit_spot_putih'] = 1 if kulit == 'Ada bintik putih' else 0
    input_dict['kulit_spot_hitam'] = 1 if kulit == 'Ada bintik hitam' else 0
    input_dict['kulit_spot_false'] = 1 if kulit == 'Tidak ada bintik' else 0

    tekstur = st.selectbox(
        "Tekstur",
        options=[
            'Lembek',
            'Keras',
            'Keropos'
        ]
    )

    input_dict['tekstur_lembek'] = 1 if tekstur == 'Lembek' else 0
    input_dict['tekstur_keras'] = 1 if tekstur == 'Keras' else 0
    input_dict['tekstur_keropos'] = 1 if tekstur == 'Keropos' else 0

    fisik = st.multiselect(
        "Visual fisik",
        options=[
            'Normal',
            'Ngapas',
            'Insang gelap',
            'Anggota badan tidak lengkap'
        ]
    )

    input_dict['visual_normal'] = 1 if ('Normal' in fisik) else 0
    input_dict['visual_ngapas'] = 1 if ('Ngapas' in fisik) else 0
    input_dict['visual_insang_gelap'] = 1 if ('Insang gelap' in fisik) else 0
    input_dict['visual_tidak_lengkap'] = 1 if ('Anggota badan tidak lengkap' in fisik) else 0

    nafsu = st.selectbox(
        "Nafsu makan",
        options=[
            'Normal',
            'Menurun',
            'Meningkat'
        ]
    )

    input_dict['makan_normal'] = 1 if nafsu == 'Normal' else 0
    input_dict['makan_turun'] = 1 if nafsu == 'Menurun' else 0
    input_dict['makan_naik'] = 1 if nafsu == 'Meningkat' else 0

    ukuran = st.multiselect(
        "Size",
        options=[
            'Normal',
            'Kerdil',
            'Tidak seragam'
        ]
    )

    input_dict['size_normal'] = 1 if ('Normal' in ukuran) else 0
    input_dict['size_kerdil'] = 1 if ('Kerdil' in ukuran) else 0
    input_dict['size_tidak_seragam'] = 1 if ('Tidak seragam' in ukuran) else 0

    mortalitas = st.selectbox(
        'Mortalitas',
        options=[
            'Ada mortalitas',
            'Tidak ada mortalitas'
        ]
    )

    input_dict['mortalitas_true'] = 1 if mortalitas == 'Ada mortalitas' else 0
    input_dict['mortalitas_false'] = 1 if mortalitas == 'Tidak ada mortalitas' else 0

    hepa1, hepa2 = st.columns(2)
    with hepa1:
        hepatopankreas_size = st.selectbox(
            'Ukuran hepatopankreas',
            options=[
                'Normal',
                'Mengkerut',
                'Membengkak'
            ]
        )

        input_dict['hepa_size_normal'] = 1 if hepatopankreas_size == 'Normal' else 0
        input_dict['hepa_size_kerut'] = 1 if hepatopankreas_size == 'Mengkerut' else 0
        input_dict['hepa_size_bengkak'] = 1 if hepatopankreas_size == 'Membengkak' else 0
    with hepa2:
        hepatopankreas_warna = st.multiselect(
            "Warna hepatopankreas",
            options=[
                'Coklat kehijauan (normal)',
                'Coklat kehitaman',
                'Putih/Pucat',
            ]
        )
        input_dict['hepa_warna_coklathijau'] = 1 if ('Coklat kehijauan (normal)' in hepatopankreas_warna) else 0
        input_dict['hepa_warna_coklathitam'] = 1 if ('Coklat kehitaman' in hepatopankreas_warna) else 0
        input_dict['hepa_warna_pucat'] = 1 if ('Putih/Pucat' in hepatopankreas_warna) else 0

    feces1, feces2 = st.columns(2)
    with feces1:
        feces_warna = st.selectbox(
            "Warna feces",
            options=[
                'Putih',
                'Coklat/hijau',
                'Hitam/gelap'
            ]
        )
        input_dict['feces_warna_putih'] = 1 if feces_warna == 'Putih' else 0
        input_dict['feces_warna_coklathijau'] = 1 if feces_warna == 'Coklat/hijau' else 0
        input_dict['feces_warna_hitamgelap'] = 1 if feces_warna == 'Hitam/gelap' else 0
    with feces2:
        feces_bentuk = st.selectbox(
            "Bentuk feces",
            options=[
                'Utuh (normal)',
                'Lembek'
            ]
        )
        input_dict['feces_bentuk_utuh'] = 1 if feces_bentuk == 'Utuh (normal)' else 0
        input_dict['feces_bentuk_lembek'] = 1 if feces_bentuk == 'Lembek' else 0

st.subheader('Result')

to_predict = list(input_dict.values())
disease = clf.predict([to_predict])[0] 

st.write(disease)

result = pd.DataFrame(
    clf.predict_proba([to_predict]),
    columns=clf.classes_
).T.reset_index()

result.columns = ['Disease', 'Probability']
result['Probability'] = result['Probability'] * 100.0
result = result[result['Probability']>=20.0]
result = result.sort_values(by='Probability', ascending=False).reset_index(drop=True)
result['Probability'] = result['Probability'].map('{:,.2f}%'.format)

st.dataframe(result, use_container_width=True)
st.caption("Penyakit yang ditampilkan adalah penyakit dengan peluang >= 20%")


disease_opt = st.selectbox(
    label="Pilih penyakit",
    options=result['Disease'].unique(),
    index=0)

pencegahan_title= 'Pencegahan ' + disease_opt
pengendalian_title= 'Pengendalian ' + disease_opt

pencegahan, pengendalian = st.tabs([pencegahan_title,pengendalian_title])

pencegahan_dict = {
'AHPND':'''
- Pertahankan kondisi kualitas air (lakukan sipon rutin)
- Pemberian imunostimulan/probiotik pada air maupun feed secara rutin 
- PL atau indukan diperoleh dari sumber terpercaya dan sudah SPF                        
- Pengecekan kondisi udang secara rutin
- Menerapkan biosecurity       
- PCR benur, dan PL pada DOC 15
''',
'IMNV':'''
- Pertahankan kondisi kualitas air (shipon rutin)
- Pemberian imunostimulan/probiotik pada air maupun feed secara rutin 
- PL atau indukan diperoleh dari sumber terpercaya dan sudah SPF                        
- Pengecekan kondisi udang secara rutin 
- Menerapkan biosecurity
- Turunkan kedapatan tebar
- Jaga kestabilan kualits air (plankton), dengan kecerahan 30 sd 40 cm
- Berikan immunostimulant 
- PCR benur, udang DOC 20, 35, 50
''',
'WFD':'''
- Mengurangi jumlah tebar
- Menggunakan desinfektan saat persiapan air
- Pertahankan kondisi kualitas air dan mengurangi penumpukkan bahan organik (shipon rutin)
- Pemberian imunostimulan/probiotik pada air maupun feed secara rutin (control populasi bakteri vibrio) 
- Penggunaan benur berkualitas (SPF atau SPR) 
- Kontrol kestabilan warna air dan rasio C:N:P              
- Pengecekan kondisi udang secara rutin 
- Menerapkan biosecurity 
- Kontrol pemberian pakan  
''',
'WSSV':'''
- Pertahankan kondisi kualitas air (shipon rutin)
- Pemberian imunostimulan/probiotik pada air maupun feed secara rutin 
- PL atau indukan diperoleh dari sumber terpercaya dan sudah SPF                        
- Pengecekan kondisi udang secara rutin 
- Menerapkan biosecurity  
- PCR benur, udang pada DOC 40, dan 60
''',
'EHP':'''
- Mengurangi jumlah padat tebar
- Pertahankan kondisi kualitas air (shipon rutin)
- Pemberian imunostimulan/probiotik pada air maupun feed secara rutin 
- PL atau indukan diperoleh dari sumber terpercaya dan sudah SPF                        
- Pengecekan kondisi udang secara rutin 
- Menerapkan biosecurity
'''
}
pengendalian_dict = {
'AHPND':'''
- Lakukan pengecekan di Lab sedini mungkin jika ditemukan tanda-tanda awal/gejala
- Desinfeksi dasar tambak menghilangkan bahan organik dan pengeringan 15 hari
- Desinfeksi peralatan tambak (kincir, anco, dll), saluran inlet dan outlet kemudian dikeringkan dan diberi kapur tohor 2 ton/Ha
- Desinfeksi udang yang positif AHPND selama 3-7 hari kemudian dikubur
''',
'IMNV':'''
- Stabilisasi kualitas air khususnya suhu, salinitas, dan pH, kesadahan, dan alkalinitas hindari pergantian air secara drastis dan tingkatkan aerasi
- Memberikan molase (25% dari FR/hari) atau diberi probiotik; dan mengurangi jumlah pakan atau menghentikan pakan sementara
- Air buangan tambak yang terinfeksi ada baiknya dilakukan treatment sebelum dibuang untuk meminimalisir penyabaran penyakit ke tambak lainnya
- Bila kematian banyak, nafsu makan menurun lebih baik panen saja
- Bangkai udang harus diambil / dibersihkan tiap hari dari dalam tambak. Bangkai dikubur atau dibakar.
- Turunkan pakan hingga 30 sampai 40% dari keadaan normal hingga kematian tidak ada (sedikit).
- Berikan vitamin C dan imunostimulan secara terus menerus hingga kondisi udang normal (tidak ada kematian)
- Kembalikan konsumsi pakan setelah kematian berhenti."
''',
'WFD':'''
- Kurangi/hentikan pemberian pakan                        
- Meningkatkan aerasi dengan maksimal                         
- Disinfeksi dan sanitasi total ke seluruh sistem budidaya agar tidak menyebar ke tambak yang lainnya
- Tambahkan bubuk bawang putih bersama pakan
- Penggunaan probiotik dengan dosis 3x dari penggunaan normal
''',
'WSSV':'''
- Kurangi pemberian pakan                        
- Meningkatkan aerasi dengan maksimal                         
- Menambahkan klorin untuk membunuh virus di dalam tambak dan air yang telah diberi klorin dibidarkan selama 4 hari sebelum memulai siklus baru                        
- Disinfeksi dan sanitasi total ke seluruh sistem budidaya agar tidak menyebar ke tambak yang lainnya
''',
'EHP':'''
- Bersihkan kolam dari spora, lakukan pemberian kapur atau CaO dengan perhitungan 6 ton/ha
- Dibajak kedalam tanah 10-12 cm lalu diberi air dan biarkan meresap
- Biarkan selama 1 minggu sebelum pengeringan, pada saat itu pH tanah akan naik ke 12 dan selama beberapa hari akan turun ke keadaan normal karena menyerap karbon dioksida dan menjadi CaCO3.
'''
}

with pencegahan:
    st.markdown(pencegahan_dict[disease_opt])

with pengendalian:
    st.markdown(pengendalian_dict[disease_opt])