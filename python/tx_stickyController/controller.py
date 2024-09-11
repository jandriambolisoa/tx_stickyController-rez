import os
import re
import json
from functools import partial
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from . import __author__, __version__


MAIN_PATH = os.path.dirname(__file__)


def get_selection():
    cmds.ConvertSelectionToVertices()
    selection = OpenMaya.MSelectionList()
    soft_selection = OpenMaya.MRichSelection()
    OpenMaya.MGlobal.getRichSelection(soft_selection)
    soft_selection.getSelection(selection)

    dag_path = OpenMaya.MDagPath()
    component = OpenMaya.MObject()

    iterator = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kMeshVertComponent)
    elements, weights = [], []
    while not iterator.isDone():
        iterator.getDagPath(dag_path, component)
        dag_path.pop()
        node = dag_path.fullPathName()
        fn_comp = OpenMaya.MFnSingleIndexedComponent(component)
        get_weight = lambda x: fn_comp.weight(x).influence() if fn_comp.hasWeights() else 1.0

        for i in range(fn_comp.elementCount()):
            elements.append('{0}.vtx[{1}]'.format(node, fn_comp.element(i)))
            weights.append(get_weight(i))
        iterator.next()
    return zip(elements, weights)


def keep_selection(func):
    def wrapper(*args, **kwargs):
        selection = cmds.ls(sl=1)
        result = func(*args, **kwargs)
        if not selection:
            cmds.select(cl=1)
        else:
            cmds.select(selection)
        return result
    return wrapper


def disable_autokey_during_exec(func):
    def wrapper(*args, **kwargs):
        current_state = cmds.autoKeyframe(q=1, state=1)
        cmds.autoKeyframe(state=False)
        result = func(*args, **kwargs)
        cmds.autoKeyframe(state=current_state)
        return result
    return wrapper


class NAME:
    SYSTEM = 'txSticky'

    GROUP = 'grp'
    POINT = 'point'
    POSITION = 'pos'
    NEGATIVE_POSITION = 'negpos'
    CONTROL = 'control'
    CLUSTER_HANDLE = 'clshandle'
    CLUSTER = 'cls'
    CREATION_POSITION = 'posorig'
    DECOMPOSE_ROTATE = 'decrot'
    INVMATRIX_COMPENSATION = 'invcomp'
    MULMATRIX_COMPENSATION = 'mulcomp'
    INVERT_POSITION = 'invpos'

    PARTS = [GROUP, POINT, POSITION, NEGATIVE_POSITION, CONTROL, CLUSTER_HANDLE, CLUSTER, CREATION_POSITION, DECOMPOSE_ROTATE, INVMATRIX_COMPENSATION, MULMATRIX_COMPENSATION, INVERT_POSITION]

    def __init__(self):
        pass

    @staticmethod
    def get_name(part, number, shape=False):
        if not shape:
            return '{0}_{1}_{2}'.format(NAME.SYSTEM, str(number).zfill(4), part)
        return '{0}_{1}_{2}Shape'.format(NAME.SYSTEM, str(number).zfill(4), part)


class REFERENCE_MODE:
    AUTO = 1
    MANUAL = 2


class ORIENT_MODE:
    WORLD = 0
    AS_REFERENCE = 1
    AS_VERTEX = 2


class CONTROL:
    class SPHERE:
        points = [[0.0, 0.5, 0.0], [0.0, 0.46194, 0.1913415], [0.0, 0.3535535, 0.3535535], [0.0, 0.1913415, 0.46194], [0.0, 0.0, 0.5], [0.0, -0.1913415, 0.46194], [0.0, -0.3535535, 0.3535535], [0.0, -0.46194, 0.1913415], [0.0, -0.5, 0.0], [0.0, -0.46194, -0.1913415], [0.0, -0.3535535, -0.3535535], [0.0, -0.1913415, -0.46194], [0.0, 0.0, -0.5], [0.0, 0.1913415, -0.46194], [0.0, 0.3535535, -0.3535535], [0.0, 0.46194, -0.1913415], [0.0, 0.5, 0.0], [0.1913415, 0.46194, 0.0], [0.3535535, 0.3535535, 0.0], [0.46194, 0.1913415, 0.0], [0.5, 0.0, 0.0], [0.46194, -0.1913415, 0.0], [0.3535535, -0.3535535, 0.0], [0.1913415, -0.46194, 0.0], [0.0, -0.5, 0.0], [-0.1913415, -0.46194, 0.0], [-0.3535535, -0.3535535, 0.0], [-0.46194, -0.1913415, 0.0], [-0.5, 0.0, 0.0], [-0.46194, 0.1913415, 0.0], [-0.3535535, 0.3535535, 0.0], [-0.1913415, 0.46194, 0.0], [0.0, 0.5, 0.0], [0.0, 0.46194, -0.1913415], [0.0, 0.3535535, -0.3535535], [0.0, 0.1913415, -0.46194], [0.0, 0.0, -0.5], [-0.1913415, 0.0, -0.46194], [-0.3535535, 0.0, -0.3535535], [-0.46194, 0.0, -0.1913415], [-0.5, 0.0, 0.0], [-0.46194, 0.0, 0.1913415], [-0.3535535, 0.0, 0.3535535], [-0.1913415, 0.0, 0.46194], [0.0, 0.0, 0.5], [0.1913415, 0.0, 0.46194], [0.3535535, 0.0, 0.3535535], [0.46194, 0.0, 0.1913415], [0.5, 0.0, 0.0], [0.46194, 0.0, -0.1913415], [0.3535535, 0.0, -0.3535535], [0.1913415, 0.0, -0.46194], [0.0, 0.0, -0.5]]
        knots = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
        icon = '{0}/icons/shape_sphere.png'.format(MAIN_PATH)
        name = 'Sphere'

    class CUBE:
        points = [[0.5, 0.5, 0.5], [0.5, 0.5, -0.5], [0.5, -0.5, -0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5], [-0.5, 0.5, -0.5], [-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5], [-0.5, 0.5, 0.5], [-0.5, 0.5, -0.5], [0.5, 0.5, -0.5], [0.5, -0.5, -0.5], [-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5]]
        knots = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        icon = '{0}/icons/shape_cube.png'.format(MAIN_PATH)
        name = 'Cube'

    class PYRAMID_INV:
        points = [[0.5, 1, 0.5], [0.5, 1, -0.5], [-0.5, 1, -0.5], [-0.5, 1, 0.5], [0.5, 1, 0.5], [0, -2.98023e-008, 0], [0.5, 1, -0.5], [-0.5, 1, -0.5], [0, -2.98023e-008, 0], [-0.5, 1, 0.5]]
        knots = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        icon = '{0}/icons/shape_pyramid_inv.png'.format(MAIN_PATH)
        name = 'Pyramid Inv'

    class PYRAMID:
        points = [[-0.5, 0, 0.5], [0, 1, 0], [0.5, 0, 0.5], [-0.5, 0, 0.5], [-0.5, 0, -0.5], [0, 1, 0], [0.5, 0, -0.5], [-0.5, 0, -0.5], [0.5, 0, -0.5], [0.5, 0, 0.5]]
        knots = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        icon = '{0}/icons/shape_pyramid.png'.format(MAIN_PATH)
        name = 'Pyramid'

    class CIRCLE_Y:
        points = [[-1.49012e-008, 0, 0.5], [0.129409, 0, 0.482963], [0.25, 0, 0.433013], [0.353553, 0, 0.353553], [0.433013, 0, 0.25], [0.482963, 0, 0.12941], [0.5, 0, 0], [0.482963, 0, -0.129409], [0.433012, 0, -0.25], [0.353553, 0, -0.353553], [0.25, 0, -0.433012], [0.12941, 0, -0.482963], [5.96046e-008, 0, -0.5], [-0.129409, 0, -0.482963], [-0.25, 0, -0.433013], [-0.353553, 0, -0.353553], [-0.433013, 0, -0.25], [-0.482963, 0, -0.12941], [-0.5, 0, -2.98023e-008], [-0.482963, 0, 0.129409], [-0.433013, 0, 0.25], [-0.353553, 0, 0.353553], [-0.25, 0, 0.433013], [-0.12941, 0, 0.482963], [-1.49012e-008, 0, 0.5]]
        knots = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        icon = '{0}/icons/shape_circle_y.png'.format(MAIN_PATH)
        name = 'Circle Y'

    class CIRCLE_Z:
        points = [[0.5, 0, 0], [0.482963, -0.12941, 0], [0.433013, -0.25, 0], [0.353553, -0.353553, 0], [0.25, -0.433013, 0], [0.129409, -0.482963, 0], [-1.49012e-008, -0.5, 0], [-0.12941, -0.482963, 0], [-0.25, -0.433013, 0], [-0.353553, -0.353553, 0], [-0.433013, -0.25, 0], [-0.482963, -0.129409, 0], [-0.5, 2.98023e-008, 0], [-0.482963, 0.12941, 0], [-0.433013, 0.25, 0], [-0.353553, 0.353553, 0], [-0.25, 0.433013, 0], [-0.129409, 0.482963, 0], [5.96046e-008, 0.5, 0], [0.12941, 0.482963, 0], [0.25, 0.433012, 0], [0.353553, 0.353553, 0], [0.433012, 0.25, 0], [0.482963, 0.129409, 0], [0.5, 0, 0]]
        knots = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        icon = '{0}/icons/shape_circle_z.png'.format(MAIN_PATH)
        name = 'Circle Z'

    class CIRCLE_X:
        points = [[0, 0, 0.5], [0, -0.12941, 0.482963], [0, -0.25, 0.433013], [0, -0.353553, 0.353553], [0, -0.433013, 0.25], [0, -0.482963, 0.129409], [0, -0.5, -1.49012e-008], [0, -0.482963, -0.12941], [0, -0.433013, -0.25], [0, -0.353553, -0.353553], [0, -0.25, -0.433013], [0, -0.129409, -0.482963], [0, 2.98023e-008, -0.5], [0, 0.12941, -0.482963], [0, 0.25, -0.433013], [0, 0.353553, -0.353553], [0, 0.433013, -0.25], [0, 0.482963, -0.129409], [0, 0.5, 5.96046e-008], [0, 0.482963, 0.12941], [0, 0.433012, 0.25], [0, 0.353553, 0.353553], [0, 0.25, 0.433012], [0, 0.129409, 0.482963], [0, 0, 0.5]]
        knots = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        icon = '{0}/icons/shape_circle_x.png'.format(MAIN_PATH)
        name = 'Circle X'

    class CROSS:
        points = [[-0.5, 0, 0], [0.5, 0, 0], [0, 0, 0], [0, 0, -0.5], [0, 0, 0.5], [0, 0, 0], [0, 0.5, 0], [0, -0.5, 0]]
        knots = [0, 1, 2, 3, 4, 5, 6, 7]
        icon = '{0}/icons/shape_cross.png'.format(MAIN_PATH)
        name = 'Cross'


class DIALOG_MODE:
    NORMAL = 0
    WARNING = 1
    ERROR = 2


def dialog(message, mode=DIALOG_MODE.NORMAL):
    title = ''
    color = [0.265, 0.265, 0.265]
    if mode == DIALOG_MODE.NORMAL:
        title = 'MESSAGE'
        color = [0.265, 0.265, 0.265]
        icon = None
    elif mode == DIALOG_MODE.WARNING:
        title = 'WARNING'
        color = [0.6, 0.6, 0.265]
    elif mode == DIALOG_MODE.ERROR:
        title = 'ERROR'
        color = [0.4, 0.1, 0.1]

    cmds.confirmDialog(title=title, message='{0}: {1}'.format(title, message), backgroundColor=color)


class StickyController(object):
    def __init__(self):
        if not cmds.pluginInfo('matrixNodes', query=1, loaded=1):
            cmds.loadPlugin('matrixNodes', qt=True)

        if not cmds.pluginInfo('tx_stickyPoint', query=1, loaded=1):
            cmds.loadPlugin('tx_stickyPoint', qt=True)

        if cmds.pluginInfo('tx_stickyPoint', query=1, p=1).endswith('.py'):
            print('This is the slow version of Sticky Controller. If you want to konw how enable fast mode visit \nhttps://gumroad.com/products/wAPzDg')

        cmds.pluginInfo('tx_stickyPoint', edit=1, autoload=True)

    @staticmethod
    def init_system():
        grp = cmds.ls(NAME.SYSTEM)
        if not grp:
            cmds.group(em=1, n=NAME.SYSTEM)
            cmds.addAttr(NAME.SYSTEM, ln='name', dt='string')
            return True
        if grp.__len__() > 1:
            cmds.error('More than one System Found')
            return False
        return True

    @staticmethod
    def get_next():
        next_available = 0
        next_found = False
        while not next_found:
            continue_search = False
            num = next_available
            for part in NAME.PARTS:
                obj = NAME.get_name(part, num)
                if cmds.objExists(obj):
                    continue_search = True
                    break
            if continue_search:
                next_available += 1
            else:
                next_found = True

        return next_available

    @staticmethod
    def list_systems():
        pattern = '^{0}_[0-9]+_{1}$'.format(NAME.SYSTEM, NAME.GROUP)
        systems = [n.rsplit('_', 2)[-2] for n in cmds.ls(ap=1) if re.search(pattern, n)]
        if not systems:
            return []
        systems.sort()
        return systems

    @staticmethod
    def list_selected_systems():
        selected = cmds.ls(sl=1)
        if not selected:
            return []
        pattern = '^{0}_[0-9]+_{1}$'.format(NAME.SYSTEM, NAME.CONTROL)
        systems = [n.rsplit('_', 2)[-2] for n in selected if re.search(pattern, n)]
        return systems

    @staticmethod
    def get_info_group(number):
        node = NAME.get_name(NAME.GROUP, number)
        if cmds.objExists(node):
            return node

    @staticmethod
    def get_info_point(number):
        node = NAME.get_name(NAME.POINT, number)
        if cmds.objExists(node):
            return node

    @staticmethod
    def get_info_position(number):
        node = NAME.get_name(NAME.POSITION, number)
        if cmds.objExists(node):
            return node

    @staticmethod
    def get_info_negative_position(number):
        node = NAME.get_name(NAME.NEGATIVE_POSITION, number)
        if cmds.objExists(node):
            return node

    @staticmethod
    def get_info_control(number):
        node = NAME.get_name(NAME.CONTROL, number)
        if cmds.objExists(node):
            return node

    @staticmethod
    def get_info_cluster_handle(number):
        node = NAME.get_name(NAME.CLUSTER_HANDLE, number)
        if cmds.objExists(node):
            return node

    @staticmethod
    def get_info_cluster(number):
        node = NAME.get_name(NAME.CLUSTER, number)
        if cmds.objExists(node):
            return node

    @staticmethod
    def get_info_creation_position(number):
        node = NAME.get_name(NAME.CREATION_POSITION, number)
        if cmds.objExists(node):
            return node

    @staticmethod
    def get_info_decompose_rotate(number):
        node = NAME.get_name(NAME.DECOMPOSE_ROTATE, number)
        if cmds.objExists(node):
            return node

    @staticmethod
    def get_info_invmatrix_compensation(number):
        node = NAME.get_name(NAME.INVMATRIX_COMPENSATION, number)
        if cmds.objExists(node):
            return node

    @staticmethod
    def get_info_mulmatrix_compensation(number):
        node = NAME.get_name(NAME.MULMATRIX_COMPENSATION, number)
        if cmds.objExists(node):
            return node

    @staticmethod
    def get_info_invert_position(number):
        node = NAME.get_name(NAME.INVERT_POSITION, number)
        if cmds.objExists(node):
            return node

    def get_info_vertex(self, number):
        point = self.get_info_point(number)
        if not point:
            return
        return cmds.getAttr('{0}.vertexId'.format(point))

    def get_info_reference_object(self, number):
        matrix_compensation = self.get_info_mulmatrix_compensation(number)
        if not matrix_compensation:
            return
        reference_object = cmds.listConnections('{0}.matrixIn[1]'.format(matrix_compensation), c=0, d=1, s=1, p=0)
        if not reference_object:
            return
        return reference_object[0]

    def get_info_name(self, number):
        control = self.get_info_control(number)
        if not control:
            return
        name = cmds.getAttr('{0}.name'.format(control))
        if not name:
            return ''
        return name

    def get_info_color(self, number):
        control = self.get_info_control(number)
        if not control:
            return
        shape = cmds.listRelatives(control, shapes=1, ni=1)[0]
        return cmds.getAttr('{0}.overrideColor'.format(shape))

    def get_info_size(self, number):
        control = self.get_info_control(number)
        if not control:
            return
        return cmds.getAttr('{0}.size'.format(control))

    def get_info_shape(self, number):
        control = self.get_info_control(number)
        if not control:
            return
        return cmds.getAttr('{0}.shape'.format(control))

    def get_info_first_vertex(self, number):
        control = self.get_info_control(number)
        if not control:
            return
        return cmds.getAttr('{0}.first_vertex'.format(control))

    def get_info_orient_mode(self, number):
        control = self.get_info_control(number)
        if not control:
            return
        return cmds.getAttr('{0}.orient_mode'.format(control))

    def get_info_members(self, number):
        cluster = self.get_info_cluster(number)
        if not cluster:
            return []
        cluster_set = [n for n in cmds.listConnections('{0}.message'.format(cluster), c=0, d=1, s=0, p=0) if cmds.nodeType(n) == 'objectSet']
        if not cluster_set:
            return []
        members = cmds.sets(cluster_set, q=1)
        if not members:
            return []
        return cmds.ls(members, fl=1)

    def get_info_weights(self, number):
        cluster = self.get_info_cluster(number)
        if not cluster:
            return []
        members = self.get_info_members(number)
        if not members:
            return []

        return cmds.percent(cluster, members, q=1, v=1)

    def delete_system(self, number):
        for part in NAME.PARTS:
            obj = NAME.get_name(part, number)
            if cmds.objExists(obj):
                cmds.delete(obj)
        if not self.list_systems() and cmds.objExists(NAME.SYSTEM):
            cmds.delete(NAME.SYSTEM)

    def save_systems(self, numbers, path):
        dic = {}
        for number in numbers:
            members = self.get_info_members(number)
            weights = self.get_info_weights(number)

            dic[number] = {'name': self.get_info_name(number),
                           'size': self.get_info_size(number),
                           'shape': self.get_info_shape(number),
                           'color': self.get_info_color(number),
                           'orient_mode': self.get_info_orient_mode(number),
                           'reference_object': self.get_info_reference_object(number),
                           'first_vertex': self.get_info_first_vertex(number),
                           'weight_members': zip(members, weights)}
        try:
            with open(path, 'w') as file_path:
                json.dump(dic, file_path, indent=4)
        except:
            return

    def load_systems(self, path):
        try:
            with open(path) as json_file:
                dic = json.load(json_file)
        except:
            return

        for number in dic:
            shape = ''
            exec('shape = CONTROL.{0}'.format(dic[number]['shape']))
            self.create(reference_object=dic[number]['reference_object'],
                        orient=dic[number]['orient_mode'],
                        control_shape=shape,
                        color=dic[number]['color'],
                        size=dic[number]['size'],
                        values=dic[number]['weight_members'],
                        first_component=dic[number]['first_vertex'])

    def create_control(self, number=0, shape=CONTROL.SPHERE, color=1, size=1, first_vertex=0, orient_mode=ORIENT_MODE.WORLD):
        ctl = cmds.curve(n=NAME.get_name(NAME.CONTROL, number), d=1, p=shape.points, k=shape.knots)
        ctl_shape = cmds.listRelatives(ctl, shapes=1, ni=1)[0]
        ctl_shape = cmds.rename(ctl_shape, NAME.get_name(NAME.CONTROL, number, True))

        # Color
        try:
            cmds.setAttr(ctl_shape + '.overrideEnabled', 1)
        except:
            cmds.warning('Can\'t enable override on ' + ctl)
        cmds.setAttr(ctl_shape + '.overrideColor', color)

        # Size
        cmds.scale(size, size, size, '{0}.cv[*]'.format(ctl), a=1)
        cmds.addAttr(ln='size', at='double', dv=1)
        cmds.setAttr(ctl + '.size', size)

        # Name
        cmds.addAttr(ctl, ln='name', dt='string')

        # Shape
        cmds.addAttr(ctl, ln='shape', dt='string')
        self.set_shape(number, shape)

        # First Vertex
        cmds.addAttr(ctl, ln='first_vertex', dt='string')
        cmds.setAttr(ctl + '.first_vertex', first_vertex, type='string')

        # Orient Mode
        cmds.addAttr(ctl, ln='orient_mode', dt='string')
        cmds.setAttr(ctl + '.orient_mode', orient_mode, type='string')

        return ctl

    def set_name(self, number, name):
        ctl = self.get_info_control(number)
        if cmds.objExists(ctl):
            cmds.setAttr('{0}.name'.format(ctl), name, type='string')

    def set_color(self, number, color):
        ctl = self.get_info_control(number)
        if cmds.objExists(ctl):
            ctl_shape = cmds.listRelatives(ctl, shapes=1, ni=1)[0]
            cmds.setAttr('{0}.overrideColor'.format(ctl_shape), color)

    def set_scale(self, number, scale):
        if scale == 0:
            scale = 0.001
        ctl = self.get_info_control(number)
        if cmds.objExists(ctl):
            prev_size = cmds.getAttr('{0}.size'.format(ctl))
            new_scale = float(scale) / float(prev_size)
            cmds.scale(new_scale, new_scale, new_scale, '{0}.cv[*]'.format(ctl), a=1)
            cmds.setAttr(ctl + '.size', scale)

    @keep_selection
    def set_shape(self, number, shape):
        ctl = self.get_info_control(number)
        if not ctl:
            return

        new_ctl = cmds.curve(d=1, p=shape.points, k=shape.knots)
        new_ctl_shape = cmds.listRelatives(new_ctl, shapes=1, ni=1)[0]
        ctl_shape = cmds.listRelatives(ctl, shapes=1, ni=1)[0]
        prev_size = cmds.getAttr('{0}.size'.format(ctl))
        cmds.scale(prev_size, prev_size, prev_size, '{0}.cv[*]'.format(new_ctl), a=1)

        cmds.setAttr('{0}.shape'.format(ctl), str(shape).rsplit('.')[-1], type='string')

        cmds.connectAttr('{0}.worldSpace[0]'.format(new_ctl_shape), '{0}.create'.format(ctl_shape))
        # cmds.evalDeferred('import maya.cmds as cmds;cmds.disconnectAttr("{0}.worldSpace[0]", "{1}.create");cmds.delete("{2}")'.format(new_ctl_shape, ctl_shape, new_ctl))
        cmds.refresh()
        cmds.disconnectAttr('{0}.worldSpace[0]'.format(new_ctl_shape), '{0}.create'.format(ctl_shape))
        cmds.delete(new_ctl)

    @staticmethod
    def get_reference_object():
        selected = cmds.ls(sl=1)
        if not selected:
            return

        if selected.__len__() != 1:
            return

        selected = selected[0]
        if re.search('\.', selected):
            return

        return selected

    @disable_autokey_during_exec
    def __create_multi(self, reference_object, reference_mode, orient=ORIENT_MODE.WORLD, control_shape=CONTROL.SPHERE, color=0, size=1, values=None, scui=None):
        selected = cmds.ls(sl=1, fl=1, long=1)
        if not selected:
            dialog(message='Vertex Not Selected', mode=DIALOG_MODE.ERROR)
            return
        if selected.__len__() > 1:
            dialog(message='More than One Vertex Selected', mode=DIALOG_MODE.ERROR)
            return
        valid_vertex = False
        for v in values:
            if selected[0] == v[0] and v[1] == 1.0:
                valid_vertex = True
                break

        if not valid_vertex:
            dialog(message='Main Vertex must be in the hard selection', mode=DIALOG_MODE.ERROR)
            return

        first_component = cmds.ls(sl=1, fl=1)[0]

        cmds.select(first_component, r=1)
        self.create(reference_object=reference_object, reference_mode=reference_mode, orient=orient, control_shape=control_shape, color=color, size=size, values=values, first_component=first_component)
        cmds.selectMode(object=1)
        scui.external_refresh()

    @disable_autokey_during_exec
    def create(self, reference_object=None, reference_mode=REFERENCE_MODE.MANUAL, orient=ORIENT_MODE.WORLD, control_shape=CONTROL.SPHERE, color=0, size=1, values=None, first_component=None, scui=None):

        if reference_mode == REFERENCE_MODE.MANUAL:
            # Check reference object
            if not cmds.objExists(reference_object):
                dialog(message='Reference object not found', mode=DIALOG_MODE.ERROR)
                return
            if not cmds.ls(reference_object).__len__() == 1:
                dialog(message='More than one reference object found', mode=DIALOG_MODE.ERROR)
                return

        # Check Values if provided
        if values:
            for v in values:
                if not cmds.objExists(v[0]):
                    dialog(message='Vertex not found', mode=DIALOG_MODE.ERROR)
                    return
                if not cmds.ls(v[0]).__len__() == 1:
                    dialog(message='More than one vertex found', mode=DIALOG_MODE.ERROR)
                    return

        if not values:
            # Get selection
            if not cmds.ls(sl=1):
                dialog(message='Nothing Selected', mode=DIALOG_MODE.ERROR)
                return
            values = get_selection()

        if not values:
            dialog(message='Incorrect selection. Select mesh or polyvertex', mode=DIALOG_MODE.ERROR)
            return

        # Check first component if provided
        if first_component:
            if not cmds.objExists(first_component):
                dialog(message='First component not found', mode=DIALOG_MODE.ERROR)
                return
            if not cmds.ls(first_component).__len__() == 1:
                dialog(message='More than one first component found', mode=DIALOG_MODE.ERROR)
                return

        # Get first component
        if not first_component:
            cmds.ConvertSelectionToVertices()
            vertex_selection = cmds.ls(sl=True, fl=True)
            if vertex_selection.__len__() > 1:
                dialog(message='Select main vertex, where the control to be created\nMust be a vertex in the hard selection', mode=DIALOG_MODE.NORMAL)
                cmds.selectMode(component=1)
                cmds.selectType(allComponents=0)
                cmds.selectType(polymeshVertex=1)
                cmds.select(cl=1)
                ctx = cmds.scriptCtx(title='Select Main Vertex',
                                     totalSelectionSets=1,
                                     cumulativeLists=False,
                                     expandSelectionList=True,
                                     setNoSelectionPrompt='Select Main Vertex',
                                     setSelectionPrompt='',
                                     setDoneSelectionPrompt='',
                                     setAutoToggleSelection=True,
                                     setSelectionCount=1,
                                     setAutoComplete=True)

                cmds.setToolTo(ctx)
                cmds.scriptJob(runOnce=True, event=('SelectionChanged', partial(self.__create_multi, reference_object, reference_mode, orient, control_shape, color, size, values, scui=scui)))
                return

            first_component = cmds.ls(sl=True, fl=True)[0]
        if not first_component:
            dialog(message='Nothing Selected\nSelect something', mode=DIALOG_MODE.ERROR)
            return

        if [self.get_info_first_vertex(s) for s in self.list_systems()].__contains__(first_component):
            dialog(message='Main vertex in use', mode=DIALOG_MODE.ERROR)
            return

        if reference_mode == REFERENCE_MODE.AUTO:
            geo = first_component.rsplit('.', 1)[0]

            skins = [node for node in cmds.listHistory(geo) if cmds.nodeType(node) == 'skinCluster']
            if not skins:
                dialog(message='Auto can\'t find skins', mode=DIALOG_MODE.ERROR)
                return
            if not skins.__len__() == 1:
                dialog(message='Auto find more than one skin', mode=DIALOG_MODE.ERROR)
                return
            skin = skins[0]

            joints = cmds.skinCluster(skin, q=1, inf=1)
            if not joints:
                dialog(message='Auto can\'t find joints', mode=DIALOG_MODE.ERROR)

            geo_skinned = cmds.skinCluster(skin, q=1, g=1)
            if not geo_skinned:
                dialog(message='Auto can\'t found skinned geo', mode=DIALOG_MODE.ERROR)
                return
            if not geo_skinned.__len__() == 1:
                dialog(message='Auto find more than one skinned geo', mode=DIALOG_MODE.ERROR)
                return
            skinned_first_component = '{0}.{1}'.format(cmds.listRelatives(geo_skinned[0], p=1, f=1)[0], first_component.rsplit('.', 1)[1])

            weights = [[j, cmds.skinPercent(skin, skinned_first_component, t=j, q=1)] for j in joints if cmds.skinPercent(skin, skinned_first_component, t=j, q=1)]
            max_weight = 0.0
            reference_object = None
            for joint, weight in weights:
                if weight > max_weight:
                    reference_object = joint
            if not reference_object:
                dialog(message='Auto can\'t find reference object', mode=DIALOG_MODE.ERROR)
                return

        # Objects in selection
        objects_in_selection = list(set([o[0].split('.')[0] for o in values]))

        # Previous Rotation
        previous_rototation = cmds.xform(reference_object, q=1, ro=1, ws=1)

        # Orient Control
        if orient == ORIENT_MODE.AS_VERTEX:
            dup_vertex_object = cmds.duplicate(first_component.split('.')[0])[0]
            cmds.select('{0}.{1}'.format(dup_vertex_object, first_component.split('.')[1]), r=1)
            cmds.ConvertSelectionToFaces()
            cmds.select('{0}.f[*]'.format(dup_vertex_object), tgl=1)
            cmds.delete()
            vertex_loc = cmds.spaceLocator()[0]
            vertex_pos = cmds.xform(first_component, q=1, t=1, ws=1)
            cmds.move(vertex_pos[0], vertex_pos[1], vertex_pos[2], vertex_loc)
            cmds.delete(cmds.normalConstraint(dup_vertex_object, vertex_loc, weight=1, aimVector=[1, 0, 0], upVector=[0, 1, 0], worldUpType='object', worldUpObject=reference_object, worldUpVector=[0, 1, 0]))
            mul = cmds.createNode('multMatrix')
            decompose = cmds.createNode('decomposeMatrix')
            cmds.connectAttr('{0}.worldMatrix[0]'.format(reference_object), '{0}.matrixIn[0]'.format(mul))
            cmds.connectAttr('{0}.worldInverseMatrix[0]'.format(vertex_loc), '{0}.matrixIn[1]'.format(mul))
            cmds.connectAttr('{0}.matrixSum'.format(mul), '{0}.inputMatrix'.format(decompose))
            vertex_rotation = cmds.getAttr('{0}.outputRotate'.format(decompose))[0]
            cmds.delete(dup_vertex_object, vertex_loc, mul, decompose)

        if orient == ORIENT_MODE.AS_REFERENCE or orient == ORIENT_MODE.AS_VERTEX:
            original_reference_object = reference_object
            reference_object = cmds.duplicate(reference_object, po=1)[0]
            cluster_reorient = cmds.cluster(objects_in_selection)[1]
            cmds.xform(cluster_reorient, piv=cmds.xform(first_component, q=1, t=1, ws=1))
            constraint_dup_control = cmds.parentConstraint(reference_object, cluster_reorient, mo=1)
            if orient == ORIENT_MODE.AS_VERTEX:
                cmds.rotate(vertex_rotation[0], vertex_rotation[1], vertex_rotation[2], reference_object, ws=1)
            else:
                cmds.rotate(0, 0, 0, reference_object, ws=1)

        # Get Vertex ID
        vertexid = int(re.search('\[([0-9]+)\]$', first_component).groups()[0])

        # Get Transform and shape
        transform = first_component.rsplit('.', 1)[0]
        shape = cmds.listRelatives(transform, shapes=1, ni=1, f=1)[0]

        # Get Position
        position = cmds.xform(first_component, q=1, t=1, ws=1)

        # Get Next Number
        next_number = self.get_next()

        # Create Main System
        if not self.init_system():
            dialog(message='Can\'t create Sticky System', mode=DIALOG_MODE.ERROR)
            return

        # Create Sticky Group
        grp_system = cmds.group(em=1, n=NAME.get_name(NAME.GROUP, next_number))
        cmds.parent(grp_system, NAME.SYSTEM)

        # Create Sticky Point
        sticky_point = cmds.createNode('stickyPoint', n=NAME.get_name(NAME.POINT, next_number))
        cmds.connectAttr(shape + '.worldMesh[0]', sticky_point + '.inputMesh')
        cmds.setAttr(sticky_point + '.vertexId', vertexid)

        # Create Grp with position
        grp_pos = cmds.group(em=1, n=NAME.get_name(NAME.POSITION, next_number))
        current_unit = cmds.currentUnit(q=1, l=1)
        if current_unit != 'cm':
            cmds.currentUnit(l='cm')
        cmds.connectAttr(sticky_point + '.outputTranslate', grp_pos + '.translate')
        if current_unit != 'cm':
            cmds.currentUnit(l=current_unit)
        cmds.parent(grp_pos, grp_system)

        # Create Cluster
        cluster, cluster_handle = cmds.cluster(first_component)
        new_cluster_handle = cmds.group(em=1)
        cmds.setAttr('{0}.translate'.format(new_cluster_handle), position[0], position[1], position[2], type='double3')
        cmds.makeIdentity(new_cluster_handle, apply=1, t=1, r=1, s=1, n=0)
        cmds.cluster(cluster, e=1, weightedNode=[new_cluster_handle, new_cluster_handle])
        cmds.delete(cluster_handle)
        cluster_handle = str(new_cluster_handle)
        cluster = cmds.rename(cluster, NAME.get_name(NAME.CLUSTER, next_number))
        cluster_handle = cmds.rename(cluster_handle, NAME.get_name(NAME.CLUSTER_HANDLE, next_number))
        cluster_handle_shape = cmds.listRelatives(cluster_handle, type='clusterHandle')[0]
        cluster_handle_shape = cmds.rename(cluster_handle_shape, NAME.get_name(NAME.CLUSTER_HANDLE, next_number, True))
        cmds.parent(cluster_handle, grp_system)

        # Weight Cluster
        cluster_set = cmds.listSets(o=cluster)[0]
        for i in range(len(values)):
            cmds.sets(values[i][0], fe=cluster_set)
            cmds.percent(cluster, values[i][0], v=values[i][1])
        cmds.setAttr('{0}.v'.format(cluster_handle), 0)

        # Create Control
        ctl = self.create_control(number=next_number, shape=control_shape, color=color, size=size, first_vertex=first_component, orient_mode=orient)
        cmds.delete(cmds.parentConstraint(grp_pos, ctl, mo=0))

        # Create Group Negative
        grp_neg = cmds.group(em=1, n=NAME.get_name(NAME.NEGATIVE_POSITION, next_number))
        neg = cmds.createNode('multiplyDivide', n=NAME.get_name(NAME.INVERT_POSITION, next_number))
        cmds.setAttr('{0}.input2X'.format(neg), -1)
        cmds.setAttr('{0}.input2Y'.format(neg), -1)
        cmds.setAttr('{0}.input2Z'.format(neg), -1)
        cmds.connectAttr('{0}.translateX'.format(ctl), '{0}.input1X'.format(neg))
        cmds.connectAttr('{0}.translateY'.format(ctl), '{0}.input1Y'.format(neg))
        cmds.connectAttr('{0}.translateZ'.format(ctl), '{0}.input1Z'.format(neg))
        cmds.connectAttr('{0}.outputX'.format(neg), '{0}.translateX'.format(grp_neg))
        cmds.connectAttr('{0}.outputY'.format(neg), '{0}.translateY'.format(grp_neg))
        cmds.connectAttr('{0}.outputZ'.format(neg), '{0}.translateZ'.format(grp_neg))
        cmds.parent(grp_neg, grp_pos)
        cmds.parent(ctl, grp_neg)
        cmds.connectAttr('{0}.translate'.format(ctl), '{0}.translate'.format(cluster_handle))
        cmds.connectAttr('{0}.rotate'.format(ctl), '{0}.rotate'.format(cluster_handle))
        cmds.connectAttr('{0}.scale'.format(ctl), '{0}.scale'.format(cluster_handle))
        cmds.setAttr('{0}.translateX'.format(ctl), 0)
        cmds.setAttr('{0}.translateY'.format(ctl), 0)
        cmds.setAttr('{0}.translateZ'.format(ctl), 0)

        # Create Compensation System
        creation_position = cmds.group(em=1, n=NAME.get_name(NAME.CREATION_POSITION, next_number))
        cmds.delete(cmds.parentConstraint(reference_object, creation_position, mo=0))
        cmds.delete(cmds.scaleConstraint(reference_object, creation_position, mo=0))
        cmds.parent(creation_position, grp_system)

        mult = cmds.createNode('multMatrix', n=NAME.get_name(NAME.MULMATRIX_COMPENSATION, next_number))
        inverse = cmds.createNode('inverseMatrix', n=NAME.get_name(NAME.INVMATRIX_COMPENSATION, next_number))
        cmds.connectAttr('{0}.worldInverseMatrix'.format(creation_position), '{0}.matrixIn[0]'.format(mult))
        cmds.connectAttr('{0}.worldMatrix'.format(reference_object), '{0}.matrixIn[1]'.format(mult))
        cmds.connectAttr('{0}.matrixSum'.format(mult), '{0}.inputMatrix'.format(inverse))
        undo_state = cmds.undoInfo(q=1, state=1)
        cmds.undoInfo(stateWithoutFlush=False)
        cmds.connectAttr('{0}.matrixSum'.format(mult), '{0}.preMatrix'.format(cluster))
        cmds.connectAttr('{0}.outputMatrix'.format(inverse), '{0}.postMatrix'.format(cluster))
        cmds.undoInfo(stateWithoutFlush=undo_state)

        decompose_rotation = cmds.createNode('decomposeMatrix', n=NAME.get_name(NAME.DECOMPOSE_ROTATE, next_number))
        cmds.connectAttr('{0}.matrixSum'.format(mult), '{0}.inputMatrix'.format(decompose_rotation))
        cmds.connectAttr('{0}.outputRotate'.format(decompose_rotation), '{0}.rotate'.format(grp_pos))

        if orient == ORIENT_MODE.AS_REFERENCE or orient == ORIENT_MODE.AS_VERTEX:
            cmds.disconnectAttr('{0}.worldMatrix[0]'.format(reference_object), '{0}.matrixIn[1]'.format(mult))
            cmds.connectAttr('{0}.worldMatrix[0]'.format(original_reference_object), '{0}.matrixIn[1]'.format(mult))
            cmds.delete(constraint_dup_control, cluster_reorient, reference_object)

        cmds.select(ctl, r=1)

        return next_number
