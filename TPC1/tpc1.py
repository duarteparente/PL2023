import matplotlib.pyplot as plt

model = {
    "idade": [],
    "sexo": [],
    "tensão": [],
    "colesterol": [],
    "batimento": [],
    "temDoença": []
}

totalDoentes = 0

def read_csv():
    file = [l.rstrip() for l in open("myheart.csv")]
    file.remove('idade,sexo,tensão,colesterol,batimento,temDoença')
    for l in file:
        line = l.split(",")
        model["idade"].append(line[0])
        model["sexo"].append(line[1])
        model["tensão"].append(line[2])
        model["colesterol"].append(line[3])
        model["batimento"].append(line[4])
        model["temDoença"].append(line[5])
    return quantos_doentes()

def tem_doenca(i):
    if model["temDoença"][i] == '1':
        return 1
    return 0     

def quantos_doentes():
    counter = 0
    for i in model["temDoença"]:
        if i == '1':
            counter += 1
    return counter
    
def dist_sex():
    s = model["sexo"]
    distribution = {}
    counterM, counterMD, counterF, counterFD = 0, 0, 0, 0
    for i in range(len(s)):
        if s[i] == 'M':
            counterM += 1
            counterMD += tem_doenca(i) 
        else:
            counterF += 1
            counterFD += tem_doenca(i)
    distribution['M'] = (f"{((counterMD/counterM)*100):.1f} %", counterMD)
    distribution['F'] = (f"{((counterFD/counterF)*100):.1f} %", counterFD)
    return distribution

def dist_idade():
    distribution = {}
    escaloes = []
    idade = model["idade"]
    for _ in range(50):
        escaloes.append(0)
    for i in range(len(idade)):
        if tem_doenca(i) == 1:
            escaloes[int(idade[i])-30] += 1
    for i in range(0,len(escaloes),5):
        sum = 0
        for j in range(i,i+5):
            sum += escaloes[j]
        distribution[f"[{i+30}-{i+34}]"] = (f"{((sum/totalDoentes)*100):.1f} %", sum)
    return distribution
    
def dist_col():
    distribution = {}
    counterND = 0
    colesterol = []
    col = [ int(i) for i in model["colesterol"]]
    for _ in range(520):
        colesterol.append(0)
    for i in range(len(col)):
        if tem_doenca(i) == 1:
            if col[i] == 0:
                counterND += 1
            else:
                colesterol[col[i]-85] += 1
    distribution["N/D [0]"] = (f"{((counterND/totalDoentes)*100):.1f} %", counterND)
    for i in range(0,len(colesterol),10):
        sum = 0
        for j in range(i,i+10):
            sum += colesterol[j]
        distribution[f"[{i+85}-{i+94}]"] = (f"{((sum/totalDoentes)*100):.1f} %", sum)
    return distribution


def dist_to_table(dist):
    print("    +-----------+--------+-----+")
    for i in dist:
        print ("    | {:^9} | {:<6} | {:<3} |".format(i,dist[i][0],dist[i][1]))
    print("    +-----------+--------+-----+")
    

def dist_to_plot(dist):
    names = list(dist.keys())
    values = list(dist.values())
    freq = [int(i[1]) for i in values]
    plt.bar(range(len(dist)), freq, tick_label=names)
    plt.show()

   
if __name__ == "__main__":
    totalDoentes = read_csv()
    print("\n > Distribuição da doença por sexo\n")
    sex = dist_sex()
    dist_to_table(sex)
    print("\n > Distribuição da doença por escalões etários\n")
    idade = dist_idade()
    dist_to_table(idade)
    print("\n > Distribuição da doença por níveis de colesterol\n")
    col = dist_col()
    dist_to_table(col)
    #dist_to_plot(sex)
    #dist_to_plot(idade)
    #dist_to_plot(col)