from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import pandas as pd
class Solver:

    def __init__(self,file) -> None:
        self.df = self.read_file(file)
        self.estudantes:list[str] = self.get_students()
        self.empresarios = self.get_empresarios()
        print(self.empresarios)
        self.preferencia = self.get_preferencia()
        #print(self.preferencia)
        self.modelo = LpProblem(name="atribuicao_de_mesas", sense=LpMaximize)
    
    def get_students(self):
        return self.df.loc[:,self.df.columns[0]].values.tolist()
    
    def get_empresarios(self) -> list[str]:
        return list(set(self.df.iloc[:, 1:].dropna().values.flatten()))
    
    @staticmethod
    def read_file(csv_file):
        file = pd.read_csv(csv_file,header=0,index_col=None)
        

        #df = pd.DataFrame({k: pd.Series(v) for k, v in preferencias.items()})
        return file
    
    def get_preferencia(self):
        preferencias = {}
        for index, row in self.df.iterrows():
            key = row[0]
            values = row[1:].tolist()
            preferencias[key] = values
        return preferencias
    
    def solve(self):
        self.modelo.solve()
    
    def define_problem(self):

        # Criação do modelo

        # Variáveis de decisão
        self.mesa = [(e, s) for e in self.empresarios for s in self.estudantes]
        self.x = LpVariable.dicts("mesa",
                            [(w[0], w[1]) for w in self.mesa],
                            cat='Binary')

        # Função objetivo
        self.modelo += lpSum(self.x[e, s] for e, s in self.mesa)
        
        # Restrições
        # Cada estudante se senta em uma mesa
        for s in self.estudantes:
            self.modelo += lpSum(self.x[e, s] for e in self.empresarios) == 1

        # Cada empresário se senta com no máximo 4 estudantes
        for e in self.empresarios:
            self.modelo += lpSum(self.x[e, s] for s in self.estudantes) <= 4

        # Restrições de preferências dos estudantes
        for s, prefs in self.preferencia.items():
            for e in self.empresarios:
                if e not in prefs:
                    self.modelo += self.x[e, s] == 0

    def resultados(self):

        # Extraindo resultados
        mesas_atribuidas = [(e, s) for e, s in self.mesa if self.x[e, s].varValue == 1]
        #for e, s in mesas_atribuidas:
            #print(f"{s} irá jantar com {e}")
        return mesas_atribuidas


    def resultados_negativos(self):
        estudantes_insatisfeitos = 0
        for s in self.estudantes:
            preferencia_atendida = False
            for e in self.empresarios:
                if e in self.preferencia[s] and self.x[e, s].varValue == 1:
                    preferencia_atendida = True
                    break
            if not preferencia_atendida:
                estudantes_insatisfeitos += 1

        #print(f"Quantidade de estudantes cujas preferências não foram atendidas: {estudantes_insatisfeitos}")
        return estudantes_insatisfeitos


if __name__ == "__main__":
    solver = Solver('test2.csv')
    solver.define_problem()
    solver.solve()
    solver.resultados()