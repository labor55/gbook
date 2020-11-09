# -*- coding: utf-8 -*-
import warnings
from peewee_mysql import Peewee, databases
from scrapy.utils.project import get_project_settings
import logging
import threading
logger = logging.getLogger(__name__)


def synchronized(func):
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func

class Menu:
    id = None
    menu_id = None
    name = None
    parent_menu_id = None
    seq = None
    path = None
    parent = None
    children = None

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.menu_id = kwargs.get('menu_id')
        self.name = kwargs.get('name')
        self.parent_menu_id = kwargs.get('parent_menu_id')
        self.seq = kwargs.get('seq')
        self.path = kwargs.get('path')
        self.parent = {} if kwargs.get('parent') is None else kwargs.get('parent')
        self.children = [] if kwargs.get('children') is None else kwargs.get('children')


class MenuIdGenerator:
    _instance = None
    settings = get_project_settings()
    tree_menu = {}
    root_menu = Menu()
    print('&'*60)

    @synchronized
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        初始化menu表，判断是否有初始菜单
        """

        if not Peewee.table_exists():
            Peewee.create_table()
            Peewee.create(menu_id=str(self.settings.get('G_ROOT_ID')),
                          name=self.settings.get('G_ROOT_NAME'),
                          parent_menu_id='0',
                          path=self.settings.get('G_ROOT_NAME'))

    def _init_menu(self):
        """
        初始化tree_menu， 查询出所有的菜单， 并将其包装成树状结构，放置于tree_menu变量中
        :return:
        """
        menu_item_total = Peewee.select()
        for m_ite in menu_item_total:
            menu_id = m_ite.menu_id
            menu = Menu()
            if menu_id in self.tree_menu.keys():
                menu = self.tree_menu.get(menu_id)

            menu.menu_id = menu_id
            menu.name = m_ite.name
            menu.path = m_ite.path
            menu.seq = m_ite.seq
            parent_menu_id = m_ite.parent_menu_id
            menu.parent_menu_id = parent_menu_id

            if parent_menu_id in self.tree_menu.keys():
                self.tree_menu.get(parent_menu_id).children.append(menu)
                menu.parent = self.tree_menu.get(parent_menu_id)
            elif parent_menu_id != '0':
                # 虚拟父级菜单
                parent_menu = Menu()
                parent_menu.menu_id = parent_menu_id
                parent_menu.children.append(menu)
                menu.parent = parent_menu
                self.tree_menu[parent_menu_id] = parent_menu
            self.tree_menu[menu_id] = menu
            if menu_id == str(self.settings.get('G_ROOT_ID')):
                self.root_menu = menu

        no_exists_id = []
        delete_keys = []

        for key in self.tree_menu.keys():
            value = self.tree_menu.get(key)
            if (value.name is None or value.parent_menu_id is None) and self.root_menu.parent != value:
                # 这个and self.root_menu.parent != value判断主要是有些顶层菜单的parent_menu_id可能不为0，那么就不管这个顶层菜单项
                no_exists_id.append(key)
                self._delete_tree_menu_keys(key, delete_keys)

        for menu_id_t in delete_keys:
            self.tree_menu.pop(menu_id_t)
        if len(no_exists_id) != 0:
            logging.warning('》》》》》》》 菜单表中，menu-id为 {} 的菜单可能不存在'.format(no_exists_id))

    def _delete_tree_menu_keys(self, dkey, delete_keys):
        children = self.tree_menu.get(dkey).children
        delete_keys.append(dkey)

        for t_m in children:
            self._delete_tree_menu_keys(t_m.menu_id, delete_keys)

    def get_menu_id(self, arr, parent_menu_id=str(settings.get('G_ROOT_ID'))):
        """
        输入菜单列表，例如['ab', 'dc', 'aaa'] ,会自动在菜单表中生成对应的菜单，并返回最后一级菜单对应的menu_id
        :param arr: 菜单列表
        :param parent_menu_id: 父menu_id，不用填
        :return:
        """
        if not self.tree_menu:
            self._init_menu()
        insert_menu = []
        for level, name in enumerate(arr):

            name_list = self._get_level_menu_name_list(parent_menu_id)
            if name not in name_list:
                tree_seq = self.tree_menu.get(parent_menu_id).seq
                seq = str(tree_seq + 1)
                self.tree_menu.get(parent_menu_id).seq = tree_seq + 1

                new_id = (parent_menu_id + seq) if len(seq) >= 3 else (parent_menu_id + '0' + seq if len(seq) == 2 else
                                                                       parent_menu_id + '00' + seq)
                path = self.tree_menu.get(parent_menu_id).path + '->' + name
                insert_menu.append({
                    'menu_id': new_id,
                    'name': name,
                    'parent_menu_id': parent_menu_id,
                    'path': path
                })
                child = Menu(menu_id=new_id, name=name, parent_menu_id=parent_menu_id, path=path, seq=0,
                             parent=self.tree_menu.get(parent_menu_id))
                self.tree_menu.get(parent_menu_id).children.append(child)
                self.tree_menu[new_id] = child
                parent_menu_id = new_id
            else:
                parent_menu_id = self._get_menu_by_name(name, parent_menu_id).menu_id
        with databases.atomic():
            try:
                Peewee.insert_many(insert_menu).execute()
                for item in insert_menu:
                    p = item['parent_menu_id']
                    Peewee.update(seq=Peewee.seq+1).where(Peewee.menu_id == p).execute()
            except Exception as e:
                logger.error('》》》》》》》》》》》》》》》》》菜单插入异常')
                self.tree_menu = {}
                raise e
        return parent_menu_id

    def _get_menu_by_name(self, name, parent_menu_id):
        """
        从tree_menu 中通过name, parent_menu_id获取对应的菜单Menu类
        :param name:
        :param parent_menu_id:
        :return:
        """
        for m in self.tree_menu.get(parent_menu_id).children:
            if m.name == name:
                return m
        raise Exception('未找到菜单')

    def _get_level_menu_name_list(self, menu_id):
        """
        获取某个菜单的所有直接子菜单的名字
        :param menu_id:
        :return:
        """
        level_menu = self.tree_menu.get(menu_id).children
        name_list = []
        for menu in level_menu:
            name_list.append(menu.name)
        return name_list

    def getMenuId(self, arr, parent_menu_id=str(settings.get('G_ROOT_ID'))):
        warnings.warn(
            "the method is deprecated, please use 'get_menu_id()'",
            DeprecationWarning,
            stacklevel=2)
        return self.get_menu_id(arr, parent_menu_id)
        # for name in arr:
        #     t = Peewee.select().where((Peewee.name == name) & (Peewee.parent_menu_id == parent_menu_id))
        #     if not t.exists():
        #         # 将menu_id为parent_menu_id的数据seq加一
        #         Peewee.update(seq=Peewee.seq + 1).where(Peewee.menu_id == parent_menu_id).execute()
        #         parent_node = Peewee.get(Peewee.menu_id == parent_menu_id)
        #         path = parent_node.path
        #         peq = str(parent_node.seq)
        #         pid = parent_node.menu_id
        #         new_id = (pid + peq) if len(peq) >= 3 else (pid + '0' + peq if len(peq) == 2 else pid + '00' + peq)
        #         new_path = path + '->' + name
        #
        #         Peewee.insert(menu_id=new_id, name=name, parent_menu_id=pid, path=new_path).execute()
        #         parent_menu_id = new_id
        #
        #     else:
        #         parent_menu_id = t.get().menu_id
        # return parent_menu_id
    