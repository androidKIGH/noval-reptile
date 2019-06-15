import os
import json

root_dir = '/home/speng/Desktop/book/'


# 获取当前目录下所有文件夹
def get_all_file(path):
    return os.listdir(path)


# 打开文件,返回json
def form_file_to_json(file_name):
    with open(file_name, 'r') as f:
        json_format = json.loads(f.read())

    return json_format


# 比较两个文件名是否一致
def comparison_file_name(name1, name2):
    return str(name1).__eq__(name2)


def start():
    for each_dir in get_all_file(root_dir):
        is_success = True
        chapter_detail = {}
        if each_dir.endswith('.zip'):
            continue
        book_dir_path = os.path.join(root_dir, each_dir)

        for each_file in get_all_file(book_dir_path):
            if comparison_file_name(each_file, 'index'):
                book_json = form_file_to_json(os.path.join(book_dir_path, each_file))
                chapter_detail = book_json['detail']

        chapter_list = get_all_file(book_dir_path)
        for each_index in chapter_detail:
            if each_index['index'] in chapter_list:
                continue
            else:
                is_success = False
                print(each_index['name'] + 'is not exist')

        if is_success:
            print('{} is ok!'.format(each_dir))
        else:
            print('{} don^t ok !'.format(each_dir))


if __name__ == '__main__':
    start()
