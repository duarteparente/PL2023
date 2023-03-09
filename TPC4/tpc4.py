import re
import statistics

def read_csv(filepath):
    file = [l.rstrip().split(',') for l in open(filepath)]
    header = [x for x in file.pop(0) if x != '']
    aux = []
    for i in range(len(header)):
        if '}' in header[i] and header[i-1][-1].isdigit():
            aux.append(header[i])
            header[i-1] += ',' + header[i]
    for i in aux:
        header.remove(i)
    data = []
    for i in file:
        d = {}
        for j in range(len(header)):
            r1 = re.search(r'{(\d+),*(\d*)}', header[j])
            r3 = re.search(r'(\w+){(\d+),*(\d*)}::(\w+)', header[j])
            if r3 != None: # Funções
                func = r3.group(3)
                max_value = int(r1.group(2))
                if r3.group(4) != '':
                    func = r3.group(4)
                    max_value = int(r3.group(3))
                l = []
                for index in range(max_value):
                    if i[j+index] != '':
                        l.append(int(i[j+index]))
                n = sum(l)
                if func == "media":
                    n = statistics.mean(l)
                d[r3.group(1) + '_' + func] = n
            elif r1 != None: # Listas
                temp = re.sub(r'{(\d+),*(\d*)}','',header[j])
                l = []
                max_value = int(r1.group(1))
                if r1.group(2) != '':
                    max_value = int(r1.group(2))
                for index in range(max_value):
                    if i[j+index] != '':
                        l.append(int(i[j+index]))
                d[temp] = l 
            else:        
                d[header[j]] = i[j]
        data.append(d)
    return data


def to_json(filepath,data):
    file = open(filepath,'w')
    gen = '[\n'
    for i in data:
        gen += '    {\n'
        for j in i:
            if j == list(i)[-1]:
                if type(i[j]) in [list,int,float]:
                    gen += f'        "{j}": {i[j]}\n'
                else:
                    gen += f'        "{j}": "{i[j]}"\n'
            else: 
                if type(i[j]) in [list,int,float]:
                    gen += f'        "{j}": {i[j]},\n'
                else:
                    gen += f'        "{j}": "{i[j]}",\n'
        if i == data[-1]:
            gen += '    }\n'
        else:
            gen += '    },\n'
            
    gen += ']'
        
    file.write(gen)
    file.close()


to_json("alunos.json",read_csv("alunos.csv"))
to_json("alunos2.json", read_csv("alunos2.csv"))
to_json("alunos3.json", read_csv("alunos3.csv"))
to_json("alunos4.json", read_csv("alunos4.csv"))
to_json("alunos5.json", read_csv("alunos5.csv"))