indexes = {'mrmullock': 590, 'Eggdude68': 932, 'RBX_Library': 90, 'youtuberpro21': 13, 'Infinifea': 
321, 'Huanblast': 32, 'TempristIsAlbert': 5, 'MI1ME': 473, 'PRO_OMG': 16, 'Cuber_78': 8, 'Zyoxuz': 5, 'Mayusachi': 2955, '8BitColours': 1324, 'Cheesebaker3': 6, 'EuropeanTruck': 763, 'lazzzt': 825, '171_d00r': 434, 'DIP3333': 717, 'CultMount': 31, 'marenda321': 790, 'kekesteto13': 81, 'Royal254Ryan123': 224, 'AceSpirals': 4, 'roastedhunter223': 17, '41_3x': 173, 'ZaccPax2003': 253, 'hanoyukii': 23, 'xNolifer': 25, 'TaxFraudBruh': 25, 'FlipsAero': 425, 'zombiefire12345677': 494, 'jmantoney': 1, 'Getnoob97': 1, 'TheDarkShadow214': 220, 'Polesslingen': 21, 'Monkeyology': 5, 'Codered_Steel': 419, 'Lord_Basilisk': 2, 'Infected_pilot': 163, 'cem2806': 179, 'drphilipsen': 157, 'Mati_dup1': 106, 'Outlory': 128, 'Noobslikedirt': 165, 'ciousedd': 206, 'vAX_XA': 294, 'ryan977ftw': 27, 'TheKacper122': 325, 'uvalm': 6, 'SnowGoId': 191, 'DisillusionedRage': 291, '0118621': 11, 'MSCOBoi': 139, 'danielthepoo': 396, 'xAuroraDragon': 166, 'catgirI1x': 27, '62tar': 45, 'holiatak12': 126, 'Rackyism': 58, 'sir_flaperjak': 115, 'SWTORDarthMarr': 171, 'Spectrum_2OOO': 685, 'BAAAAC0N': 35, 'Mraples': 172, 'nahvaja': 45, 'DereXerel': 310, 'Trophy_Warning': 58, 'peanut_want': 46, 'w_ondr': 12, 'ICannotAimPleaseHelp': 717, 'chaxate': 505, 'kietnguhoc123': 18, 'reecescupsx': 1678, 'lockmekid': 196, 'DaBabyissafe': 74, 'MlgDerps': 149, '05Ruz': 15, 'blackforest517': 131, 'Catg_rls': 172, 'FerdOperator': 41, 'n_lif': 2, 'Rackyyzz': 62, 'starmarine253945': 6, 'firebro90': 5, 'TransitGuy333': 9, 'Chromeologic': 118, 'PopularDank': 98, 'unpreserved': 26, 'SMRSamirim': 157, 'ASERBYEyt': 18, 'sugabadle': 33, 'CodeGen_05': 59, 'AnthonyIX': 46, 'FeudalKingdom': 104, 'CommandoTooch': 89, 'antikiller123123': 59, 'l0keysoulx': 109, 'zidanedoan2': 44, 'Johndoe32hacker': 60, 'Timpy23': 26, 'elemental2free': 123, 'Freddy5151FR': 7, 'LevCrafter12': 232, 'cocobuddy8509': 2, 'thewolve_king': 23, 'GoldenExousia': 3, 'sebubby': 1, 'jellycaat': 4, 'Desir3dChaos': 24}
def max_key(indexes):
    max1 = list(indexes.values())[0]
    user = ''
    for i in range(len(list(indexes.values()))):
        if list(indexes.values())[i] > max1:
            max1 = list(indexes.values())[i]
            user = list(indexes)[i]

    print(user + " ::  " + str(max1))

def sort_dict(indexes, pretty):
    dict_len = len(indexes)
    # Sorts the dict by value in least to greatest
    sorted_dict = {}
    sorted_keys = sorted(indexes, key=indexes.get)

    for w in sorted_keys:
        sorted_dict[w] = indexes[w]

    # Creates two separate sorted arrays for the values and keys 
    rev_vals = list(reversed(list(sorted_dict.values())))
    rev_keys = list(reversed(list(sorted_dict.keys())))

    # Zips the two sorted arrays
    final = dict(zip(rev_keys, rev_vals))
    
    if pretty == 'n':
        print(final)

    elif pretty == 'y':
        for i in range(dict_len):
            print(str(i+1) + ". " + str(rev_keys[i]) + " ::: " + str(rev_vals[i])) 

pretty = input("Pretty? [y/n] :: ")
sort_dict(indexes, pretty)
