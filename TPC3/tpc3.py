import re
import json

def read_dataset():
    data = []
    file = open('processos.txt')
    exp = r'(?P<Pasta>\d+)::(?P<Data>\d{4}-\d{2}-\d{2})::(?P<Nome>[aA-zZ\s]*)::(?P<Pai>[aA-zZ\s]*)::(?P<Mae>[aA-zZ\s]*)::(?P<Obs>[^::]*)::'
    regex = re.compile(exp)
    for line in file:
        res = regex.match(line)
        if res != None:
            data.append(res.groupdict())
    return data    


def processos_ano(data):
    res = {}
    for d in data:
        ano = d['Data'][:4]
        if ano not in res:
            res[ano] = 0
        res[ano] += 1
    return res


def show_processos_ano(res):
    print("\n    +-----------------------------------+")
    print("    | Distribuição de processos por ano |")
    print("    +-----------------------------------+")
    print("    |     Ano     |      Frequência     |")
    print("    +-----------------------------------+")
    sorted_dict = sorted(res)
    sorted_res = {key:res[key] for key in sorted_dict}
    for key in sorted_res:
        print('    |{:^13}|{:^21}|'.format(key,sorted_res[key]))
    print("    +-----------------------------------+\n")


def nomes(data):
    res = {}
    exp = r'([aA-zZ]+) .* ([aA-zZ]+)'
    regex  = re.compile(exp)
    for d in data:
        seculo = (int(d['Data'][:4]) // 100) + 1
        if seculo not in res:
            res[seculo] = {'P': {}, 'A': {}}
        m = regex.match(d['Nome'])
        if m != None:
            p = m.group(1) 
            a = m.group(2)          
            if p not in res[seculo]['P']:
                res[seculo]['P'][p] = 0
            if a not in res[seculo]['A']:
                res[seculo]['A'][a] = 0
            res[seculo]['P'][p] += 1
            res[seculo]['A'][a] += 1
    return res


def show_nomes(res):
    print("\n    +-------------------------------------------------+")
    print("    |    Distribuição de nomes próprios e apelidos    |")
    print("    +-------------------------------------------------+")
    print("    |  Século  |   Nomes Próprios  |     Apelidos     |")
    print("    +-------------------------------------------------+")
    seculos = list(res.keys())
    seculos.sort()
    for s in seculos:
        p = res[s]['P']
        sorted_p = {i : p[i] for i in sorted(p, key = p.get, reverse = True)[:5]}
        p_list = list(sorted_p.keys())
        
        a = res[s]['A']
        sorted_a = {i : a[i] for i in sorted(a, key = a.get, reverse = True)[:5]}
        a_list = list(sorted_a.keys())
        
        for i in range(0,5):
            if i == 2:
                print('    |{:^10}| {:^10} - {:^5}|{:^10} - {:^5}|'.format(s,p_list[i],sorted_p[p_list[i]],a_list[i],sorted_a[a_list[i]]))
            else:
                print('    |          | {:^10} - {:^5}|{:^10} - {:^5}|'.format(p_list[i],sorted_p[p_list[i]],a_list[i],sorted_a[a_list[i]]))
        print("    +-------------------------------------------------+")  
        
        
def relacoes(data):
    res = {}
    # Manuel Jose Sousa Machado,Irmao. Proc.8239.
    exp = r'[aA-zZ\s]*,([aA-zZ\s]*)\.[\s]*Proc\.[\d]+\.'
    regex = re.compile(exp)
    for d in data:
        r = regex.findall(d['Obs'])
        for i in r:
            if i not in res:
                res[i] = 0
            res[i] += 1
    return res


def show_relacoes(res):
    print("\n    +------------------------------------------+")
    print("    |         Distribuição de relações         |")
    print("    +------------------------------------------+")
    print("    |          Relação          |  Frequência  |")
    print("    +------------------------------------------+")
    for i in res:
        print('    |{:^27}|{:^14}|'.format(i,res[i]))
    print("    +------------------------------------------+")      
    

def formato(data):
    res = data[:20]
    file = open("formatado.json",'w')
    json.dump(res,file,indent=4)
    file.close()

def main():
    data = read_dataset()
    show_processos_ano(processos_ano(data))
    show_nomes(nomes(data))
    show_relacoes(relacoes(data))
    formato(data)
    
if __name__ == "__main__":
    main()   