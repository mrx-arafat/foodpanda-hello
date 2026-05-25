"""Area centroids per city. Each entry: (name, lat, lng)."""

DHAKA = [
    ("Gulshan", 23.7806, 90.4193), ("Banani", 23.7937, 90.4066),
    ("Baridhara", 23.8050, 90.4180), ("Bashundhara", 23.8103, 90.4254),
    ("Uttara", 23.8759, 90.3795), ("Mirpur", 23.8060, 90.3680),
    ("Mohammadpur", 23.7660, 90.3590), ("Dhanmondi", 23.7460, 90.3760),
    ("Lalmatia", 23.7560, 90.3680), ("Mohakhali", 23.7780, 90.4060),
    ("Tejgaon", 23.7610, 90.3920), ("Khilgaon", 23.7440, 90.4250),
    ("Rampura", 23.7610, 90.4250), ("Badda", 23.7800, 90.4250),
    ("Motijheel", 23.7330, 90.4170), ("Old Dhaka", 23.7106, 90.4112),
    ("Wari", 23.7170, 90.4220), ("Mugda", 23.7400, 90.4380),
    ("Jatrabari", 23.7110, 90.4350), ("Demra", 23.7140, 90.4730),
    ("Savar", 23.8580, 90.2670), ("Tongi", 23.8920, 90.4040),
    ("Gazipur", 23.9990, 90.4200), ("Narayanganj", 23.6238, 90.5000),
    ("Keraniganj", 23.6920, 90.3700),
]

CHITTAGONG = [
    ("GEC Circle",    22.3590, 91.8214),
    ("Nasirabad",     22.3640, 91.8120),
    ("Khulshi",       22.3650, 91.8050),
    ("Panchlaish",    22.3640, 91.8330),
    ("Probortok",     22.3580, 91.8330),
    ("Mehedibag",     22.3520, 91.8260),
    ("CDA Avenue",    22.3640, 91.8270),
    ("Agrabad",       22.3260, 91.8090),
    ("Halishahar",    22.3290, 91.7700),
    ("Pahartali",     22.3870, 91.7800),
    ("Akbar Shah",    22.3760, 91.7770),
    ("Bahaddarhat",   22.3680, 91.8550),
    ("Chawk Bazar",   22.3520, 91.8430),
    ("Kotwali",       22.3380, 91.8350),
    ("Anderkilla",    22.3430, 91.8400),
    ("Murad Pur",     22.3690, 91.8430),
    ("Bayazid",       22.3850, 91.8440),
    ("Oxygen",        22.3920, 91.8520),
    ("Chandgaon",     22.3870, 91.8650),
    ("Kalurghat",     22.3820, 91.8830),
    ("Patenga",       22.2330, 91.7980),
    ("Bandar",        22.2900, 91.7670),
    ("EPZ",           22.2700, 91.7660),
    ("New Market",    22.3370, 91.8310),
    ("Lalkhan Bazar", 22.3460, 91.8120),
    ("Sholoshahar",   22.3720, 91.8400),
]

SYLHET = [
    ("Zindabazar",    24.8949, 91.8687),
    ("Amberkhana",    24.9080, 91.8730),
    ("Shibganj",      24.9020, 91.8540),
    ("Subhanighat",   24.8830, 91.8650),
    ("Uposhohor",     24.8810, 91.8770),
    ("Tilagor",       24.8950, 91.8870),
    ("Akhalia",       24.9050, 91.8400),
    ("Bondor Bazar",  24.8920, 91.8700),
    ("Kazitula",      24.9000, 91.8770),
    ("Mejortila",     24.9150, 91.8470),
    ("Pathantula",    24.9080, 91.8870),
    ("Shahjalal Uposhohor", 24.8770, 91.8810),
]

KHULNA = [
    ("Khulna Sadar",  22.8456, 89.5403),
    ("Sonadanga",     22.8230, 89.5400),
    ("Khalishpur",    22.8650, 89.5230),
    ("Daulatpur",     22.8830, 89.5170),
    ("Boyra",         22.8470, 89.5320),
    ("Nirala",        22.8290, 89.5470),
    ("Shibbari",      22.8260, 89.5560),
    ("Royal Mor",     22.8400, 89.5480),
    ("New Market KH", 22.8390, 89.5520),
    ("Mujgunni",      22.8800, 89.5320),
]

RAJSHAHI = [
    ("Shaheb Bazar",  24.3636, 88.6241),
    ("Talaimari",     24.3690, 88.6310),
    ("Court",         24.3690, 88.6010),
    ("Kazla",         24.3700, 88.6450),
    ("Vodra",         24.3760, 88.6080),
    ("Upashahar",     24.3850, 88.5990),
    ("Padma",         24.3550, 88.6090),
    ("Binodpur",      24.3680, 88.6390),
    ("Motihar",       24.3680, 88.6450),
    ("New Market RJ", 24.3650, 88.6180),
]

BARISAL = [
    ("Barisal Sadar", 22.7010, 90.3535),
    ("Nuthullabad",   22.7080, 90.3450),
    ("Kawnia",        22.7230, 90.3540),
    ("Notullabad",    22.7100, 90.3380),
    ("Rupatali",      22.6810, 90.3470),
    ("Police Line",   22.6960, 90.3530),
]

RANGPUR = [
    ("Rangpur Sadar", 25.7439, 89.2752),
    ("Modern Mor",    25.7510, 89.2820),
    ("Shapla Chottor",25.7460, 89.2750),
    ("Lalbagh",       25.7560, 89.2670),
    ("Jail Road",     25.7400, 89.2750),
    ("Jahaj Company", 25.7480, 89.2770),
]

MYMENSINGH = [
    ("Mymensingh Sadar", 24.7471, 90.4203),
    ("Charpara",       24.7530, 90.4170),
    ("Maskanda",       24.7700, 90.4060),
    ("Town Hall",      24.7530, 90.4070),
    ("New Market MS",  24.7510, 90.4110),
    ("Kachari Bazar",  24.7470, 90.4080),
]

COMILLA = [
    ("Kandirpar",     23.4607, 91.1809),
    ("Race Course",   23.4640, 91.1840),
    ("Kotbari",       23.4290, 91.1490),
    ("Tomsom Bridge", 23.4540, 91.1690),
    ("Cantonment",    23.4720, 91.1600),
    ("Chartha",       23.4480, 91.1860),
]

COXS_BAZAR = [
    ("Cox's Bazar Sadar", 21.4272, 92.0058),
    ("Kalatali",      21.4220, 91.9920),
    ("Sugandha",      21.4360, 91.9930),
    ("Bus Terminal",  21.4470, 92.0060),
    ("Laldighi",      21.4400, 92.0080),
]

BOGURA = [
    ("Bogura Sadar",  24.8465, 89.3776),
    ("Satmatha",      24.8490, 89.3720),
    ("Banani BG",     24.8410, 89.3680),
    ("Charmatha",     24.8530, 89.3700),
    ("Naomatha",      24.8470, 89.3770),
]

JESSORE = [
    ("Jessore Sadar", 23.1664, 89.2081),
    ("Chowrasta",     23.1700, 89.2080),
    ("Daratana",      23.1660, 89.2030),
    ("Palbari",       23.1730, 89.2100),
    ("New Market JS", 23.1670, 89.2070),
]

REGISTRY = {
    "dhaka": DHAKA,
    "chittagong": CHITTAGONG,
    "sylhet": SYLHET,
    "khulna": KHULNA,
    "rajshahi": RAJSHAHI,
    "barisal": BARISAL,
    "rangpur": RANGPUR,
    "mymensingh": MYMENSINGH,
    "comilla": COMILLA,
    "coxsbazar": COXS_BAZAR,
    "bogura": BOGURA,
    "jessore": JESSORE,
}
