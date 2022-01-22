import datetime
import os
from pprint import pprint
import inquirer


class TrashAnalyser:
    files = []
    default_trash_path = '/mnt/c/Users/rafae.DESKTOP-RS4NIMH/Downloads'
    executor = os

    def __init__(self):
        self.get_trash_files()

    def get_trash_files(self):
        print('Buscando arquivos na pasta de Downloads...')
        for file_name in self.executor.listdir(self.default_trash_path):
            name, extension = self.executor.path.splitext(file_name)
            self.files.append(
                TrashFile(name, extension, self.executor.path.getatime(self.default_trash_path+'/'+file_name)))
        self.ask_if_show_files()

    def ask_if_show_files(self):
        questions = [
            inquirer.List(
                "size",
                message="Deseja mostrar os arquivos da lixeira?",
                choices=["Sim", "Não"],
            ),
        ]
        answers = inquirer.prompt(questions)
        self.show_trash_files() if answers['size'] == "Sim" else self.pick_old_files()

    def pick_old_files(self):
        day_lapse = int(input('Digite a quantidade de minima de dias sem ação para filtrar os arquivos: '))
        print(f'Filtrando os arquivos por {day_lapse} dias...')
        self.files = list(filter(
            lambda f: datetime.datetime.fromtimestamp(f.modification_date) < (datetime.datetime.now() - datetime.timedelta(day_lapse)), self.files))
        self.show_trash_files()
        self.delete_files()

    def delete_files(self):
        for f in self.files:
            if f.ask_if_delete():
                self.executor.remove(self.default_trash_path+"/"+f.name)

    def show_trash_files(self):
        print(f'-----------------Printando informações----------------------')
        for f in self.files:
            print('---------------------------------------------')
            print(f'Nome: {f.name}\n')
            print(f"Ultimo acesso: {datetime.datetime.fromtimestamp(f.modification_date).strftime('%d-%m-%Y %H:%M:%S')}")
            print(f'Extensão: {f.extension}')
            print('---------------------------------------------')
        print(f'Encontrados: {len(self.files)} arquivos')


class TrashFile:
    name = ''
    extension = ''
    modification_date = datetime.datetime.now()

    def __init__(self, name, extension, modification_date):
        self.name=name
        self.extension=extension if extension.startswith('.') else "."+extension
        self.modification_date = modification_date
        #datetime.datetime.fromtimestamp(modification_date).strftime('%d-%m-%Y %H:%M:%S')

    def ask_if_delete(self):
        questions = [
            inquirer.List(
                "size",
                message="Deseja apagar o arquivo "+self.name+"?",
                choices=["Sim", "Não"],
            ),
        ]
        answers = inquirer.prompt(questions)
        return answers['size'] == 'Sim'


TrashAnalyser()

