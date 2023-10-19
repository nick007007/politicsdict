from pathlib import Path
from json import loads, dumps

import PySimpleGUI as sg


db_path = Path(r'db.json')


def load_text(path):
    try:
        return path.read_text(encoding='utf-8')
    except:
        print('json 不存在, 将新建')
        return '{}'


def load_json(path):
    text = load_text(path)

    try:
        return loads(text)
    except:
        print('json 无法解析, 将被覆盖')
        return {}


def save_json(path, obj):
    text = dumps(obj, ensure_ascii=False, indent=4)
    path.write_text(text, encoding='utf-8')


politics_list = ['马原', '毛中特', '新思想', '史纲', '思修']

politics_radio = [sg.Radio(politics, 'nana', k=politics + 'radio') for politics in politics_list]
politics_checkbox = [sg.Checkbox(politics, k=politics + 'checkbox') for politics in politics_list]

layout_1 = [
    politics_radio + [sg.Button('添加词条', key='添加词条')],
    [sg.Multiline(size=(55, 10), key='text')]
]

layout_2 = [
    politics_checkbox + [sg.Button('导出词条', key='导出词条')],
    [sg.Output(size=(55, 10))]
]

layout = [
    [sg.Frame('', layout_1)],
    [sg.Frame('', layout_2)],
]

window = sg.Window('政治词条', layout, finalize=True)

db = load_json(db_path)
print('成功载入 json')


for politics in politics_list:
    if politics not in db:
        db[politics] = []

def add(tag, s):
    if s == '':
        print('词条为空')
    else:
        if s in db[tag]:
            print('词条已存在')
            return

        db[tag].append(s)
        save_json(db_path, db)
        print(f'{tag}成功添加词条:')
        print(s)

        window['text'].update('')


def render_txt(tag):
    path = Path(tag + '.txt')

    l = []

    for i, s in enumerate(db[tag], 1):
        l.append(
            f'{i}.\n' + s + '\n'
        )

    path.write_text('\n'.join(l), encoding='utf-8')
    print(f'{tag}.txt 成功导出至当前目录')



def out(tags):
    if not tags:
        print('未选择科目')
        return

    for tag in tags:
        render_txt(tag)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '添加词条':
        for politics in politics_list:
            if values[politics + 'radio']:
                add(politics, values['text'])
                break
        else:
            print('未选择科目')

    if event == '导出词条':
        tags = [politics for politics in politics_list if values[politics + 'checkbox']]
        out(tags)

window.close()