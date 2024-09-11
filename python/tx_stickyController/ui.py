import os
import re
import json
from functools import partial
import maya.cmds as cmds
import maya.mel as mel
from . import __version__, __author__, __web__
import controller
reload(controller)


class StickyControllerUI(object):
    def __init__(self):

        self.controller = controller.StickyController()

        self.main_path = os.path.dirname(__file__)
        self.path_icon_refresh = '{0}/icons/refresh.png'.format(self.main_path)
        self.path_icon_load = '{0}/icons/load.png'.format(self.main_path)
        self.path_icon_save = '{0}/icons/save.png'.format(self.main_path)
        self.path_icon_orient_world = '{0}/icons/orient_world.png'.format(self.main_path)
        self.path_icon_orient_reference = '{0}/icons/orient_reference.png'.format(self.main_path)
        self.path_icon_orient_vertex = '{0}/icons/orient_vertex.png'.format(self.main_path)
        self.path_icon_select_reference = '{0}/icons/select_reference.png'.format(self.main_path)
        self.path_icon_ok = '{0}/icons/ok.png'.format(self.main_path)
        self.path_icon_error = '{0}/icons/error.png'.format(self.main_path)
        self.path_icon_warning = '{0}/icons/warning.png'.format(self.main_path)
        self.path_icon_trash = '{0}/icons/trash.png'.format(self.main_path)
        self.path_icon_edit_members = '{0}/icons/edit_members.png'.format(self.main_path)
        self.path_icon_paint_weights = '{0}/icons/paint_weights.png'.format(self.main_path)
        self.path_icon_help = '{0}/icons/help.png'.format(self.main_path)
        self.path_icon_options = '{0}/icons/options.png'.format(self.main_path)
        self.main_window = 'tx_stickyControllerUI'

        self.icon_size = 20
        self.color_reference = [0.35, 0.35, 0.35]
        self.color_bad = [0.5, 0.22, 0.22]
        self.color_ok = [0.22, 0.5, 0.35]
        self.color_disabled_a = [0.424, 0.424, 0.424]
        self.color_disabled_b = [0.4, 0.4, 0.4]
        self.color_01 = [0.470588, 0.470588, 0.470588]
        self.color_02 = [0, 0, 0]
        self.color_03 = [0.25098, 0.25098, 0.25098]
        self.color_04 = [0.6, 0.6, 0.6]
        self.color_05 = [0.607843, 0, 0.156863]
        self.color_06 = [0, 0.0156863, 0.376471]
        self.color_07 = [0, 0, 1]
        self.color_08 = [0, 0.27451, 0.0980392]
        self.color_09 = [0.14902, 0, 0.262745]
        self.color_10 = [0.784314, 0, 0.784314]
        self.color_11 = [0.541176, 0.282353, 0.2]
        self.color_12 = [0.247059, 0.137255, 0.121569]
        self.color_13 = [0.6, 0.14902, 0]
        self.color_14 = [1, 0, 0]
        self.color_15 = [0, 1, 0]
        self.color_16 = [0, 0.254902, 0.6]
        self.color_17 = [1, 1, 1]
        self.color_18 = [1, 1, 0]
        self.color_19 = [0.392157, 0.862745, 1]
        self.color_20 = [0.262745, 1, 0.639216]
        self.color_21 = [1, 0.690196, 0.690196]
        self.color_22 = [0.894118, 0.67451, 0.47451]
        self.color_23 = [1, 1, 0.388235]
        self.color_24 = [0, 0.6, 0.329412]
        self.color_25 = [0.631373, 0.411765, 0.188235]
        self.color_26 = [0.623529, 0.631373, 0.188235]
        self.color_27 = [0.407843, 0.631373, 0.188235]
        self.color_28 = [0.188235, 0.631373, 0.364706]
        self.color_29 = [0.188235, 0.631373, 0.631373]
        self.color_30 = [0.188235, 0.403922, 0.631373]
        self.color_31 = [0.435294, 0.188235, 0.631373]
        self.color_32 = [0.631373, 0.188235, 0.411765]

        self.sticky_color_size_w = 10
        self.sticky_color_size_h = 10
        self.sticky_shape_size_w = 20
        self.sticky_shape_size_h = 20

        self.name_width = 80
        self.button_height = 24

        # if window exists erase it
        if cmds.window(self.main_window, exists=1):
            cmds.deleteUI(self.main_window)

        # Main Window
        if cmds.pluginInfo('tx_stickyPoint', query=1, p=1).endswith('.py'):
            cmds.window(self.main_window, t='Sticky Controller UI ' + __version__)
        else:
            cmds.window(self.main_window, t='Sticky Controller UI ' + __version__ + ' FAST')

        # Main Layout
        self.main_layout = cmds.formLayout(p=self.main_window)

        # Creation Layout
        self.creation_layout = cmds.formLayout(p=self.main_layout)

        self.creation_title = cmds.text(p=self.creation_layout,
                                        label='Creation',
                                        font='boldLabelFont',
                                        align='left')

        self.reference_mode_radio = cmds.radioButtonGrp(p=self.creation_layout,
                                                        numberOfRadioButtons=2,
                                                        label='',
                                                        labelArray2=['Auto', 'Manual'],
                                                        cw3=[0, 55, 60],
                                                        select=1)

        self.creation_reference_object_button = cmds.iconTextButton(p=self.creation_layout,
                                                                    label='Reference',
                                                                    i=self.path_icon_select_reference,
                                                                    style='iconAndTextHorizontal',
                                                                    w=self.name_width, h=self.button_height,
                                                                    bgc=self.color_reference,
                                                                    ann='Select Object with Reference Rotation')

        self.creation_reference_object = cmds.text(p=self.creation_layout,
                                                   label='',
                                                   align='center',
                                                   font='obliqueLabelFont',
                                                   h=self.button_height,
                                                   ann='Reference Object')

        self.creation_reference_object_icon = cmds.iconTextButton(p=self.creation_layout,
                                                                  label='',
                                                                  i=self.path_icon_warning,
                                                                  style='iconOnly',
                                                                  h=self.button_height, w=self.button_height,
                                                                  ann='WARNING: Select Reference Object')

        self.creation_world_button = cmds.iconTextButton(p=self.creation_layout,
                                                         label='World',
                                                         i=self.path_icon_orient_world,
                                                         style='iconAndTextHorizontal',
                                                         h=self.button_height,
                                                         bgc=self.color_bad,
                                                         ann='Create Sticky Controller oriented as world')

        self.creation_reference_button = cmds.iconTextButton(p=self.creation_layout,
                                                             label='Reference',
                                                             i=self.path_icon_orient_reference,
                                                             style='iconAndTextHorizontal',
                                                             h=self.button_height,
                                                             bgc=self.color_bad,
                                                             ann='Create Sticky Controller oriented as reference object')

        self.creation_vertex_button = cmds.iconTextButton(p=self.creation_layout,
                                                          label='Vertex',
                                                          i=self.path_icon_orient_vertex,
                                                          style='iconAndTextHorizontal',
                                                          h=self.button_height,
                                                          bgc=self.color_bad,
                                                          ann='Create Sticky Controller oriented as main vertex')

        cmds.formLayout(self.creation_layout, e=1,
                        attachForm=[
                            (self.creation_title, 'top', 5),
                            (self.creation_title, 'left', 5),
                            (self.creation_title, 'right', 5),

                            (self.reference_mode_radio, 'top', 2),
                            (self.reference_mode_radio, 'left', 90),
                            (self.reference_mode_radio, 'right', 5),

                            (self.creation_reference_object_button, 'left', 5),
                            (self.creation_reference_object_icon, 'right', 5),
                        ],
                        attachControl=[
                            (self.creation_reference_object_button, 'top', 5, self.creation_title),
                            (self.creation_reference_object, 'top', 5, self.creation_title),
                            (self.creation_reference_object_icon, 'top', 5, self.creation_title),
                            (self.creation_reference_object, 'left', 0, self.creation_reference_object_button),
                            (self.creation_reference_object, 'right', 0, self.creation_reference_object_icon),

                            (self.creation_world_button, 'top', 5, self.creation_reference_object_button),
                            (self.creation_reference_button, 'top', 5, self.creation_reference_object_button),
                            (self.creation_vertex_button, 'top', 5, self.creation_reference_object_button),
                        ],
                        attachPosition=[
                            (self.creation_world_button, 'left', 5, 0),
                            (self.creation_world_button, 'right', 2, 33),
                            (self.creation_reference_button, 'left', 2, 33),
                            (self.creation_reference_button, 'right', 2, 66),
                            (self.creation_vertex_button, 'left', 2, 66),
                            (self.creation_vertex_button, 'right', 5, 100),
                        ])

        # Sticky Layout
        self.sticky_layout = cmds.formLayout(p=self.main_layout)

        self.sticky_title = cmds.text(p=self.sticky_layout,
                                      label='Controllers',
                                      font='boldLabelFont',
                                      align='left')

        self.sticky_buttons_layout = cmds.rowLayout(p=self.sticky_layout,
                                                    nc=4)
        self.sticky_load_button = cmds.iconTextButton(p=self.sticky_buttons_layout,
                                                      label='Load',
                                                      image=self.path_icon_load,
                                                      style='iconOnly',
                                                      w=self.icon_size, h=self.icon_size,
                                                      ann='Load Sticky Controllers')
        self.sticky_save_button = cmds.iconTextButton(p=self.sticky_buttons_layout,
                                                      label='Save',
                                                      image=self.path_icon_save,
                                                      style='iconOnly',
                                                      w=self.icon_size, h=self.icon_size,
                                                      ann='Save Selected Sticky Controllers')
        cmds.separator(p=self.sticky_buttons_layout,
                       horizontal=False,
                       w=self.icon_size / 2.0, h=self.icon_size)
        self.sticky_refresh_button = cmds.iconTextButton(p=self.sticky_buttons_layout,
                                                         label='Refresh',
                                                         image=self.path_icon_refresh,
                                                         style='iconOnly',
                                                         w=self.icon_size, h=self.icon_size,
                                                         ann='Refresh Sticky Controllers')

        self.sticky_list = cmds.textScrollList(p=self.sticky_layout,
                                               allowMultiSelection=True)

        cmds.formLayout(self.sticky_layout, e=1,
                        attachForm=[
                            (self.sticky_title, 'top', 5),
                            (self.sticky_title, 'left', 5),
                            (self.sticky_buttons_layout, 'top', 5),
                            (self.sticky_buttons_layout, 'right', 5),
                            (self.sticky_list, 'left', 5),
                            (self.sticky_list, 'right', 5),
                            (self.sticky_list, 'bottom', 5),
                        ],
                        attachControl=[
                            (self.sticky_list, 'top', 5, self.sticky_buttons_layout),
                        ])

        # Configuration Layout
        self.configuration_layout = cmds.formLayout(p=self.main_layout)
        self.configuration_title = cmds.text(p=self.configuration_layout,
                                             l='Configuration',
                                             font='boldLabelFont',
                                             align='left')

        self.configuration_options_layout = cmds.rowLayout(p=self.configuration_layout,
                                                           nc=3)
        self.configuration_weight_button = cmds.iconTextButton(p=self.configuration_options_layout,
                                                               label='Weight',
                                                               image=self.path_icon_paint_weights,
                                                               style='iconOnly',
                                                               w=self.icon_size, h=self.icon_size,
                                                               ann='Weight')
        self.configuration_member_button = cmds.iconTextButton(p=self.configuration_options_layout,
                                                               label='Members',
                                                               image=self.path_icon_edit_members,
                                                               style='iconOnly',
                                                               w=self.icon_size, h=self.icon_size,
                                                               ann='Members')
        self.configuration_delete_button = cmds.iconTextButton(p=self.configuration_options_layout,
                                                               label='Delete',
                                                               image=self.path_icon_trash,
                                                               style='iconOnly',
                                                               w=self.icon_size, h=self.icon_size,
                                                               ann='Delete')

        self.configuration_shape_layout_00 = cmds.formLayout(p=self.configuration_layout)
        self.configuration_shape_01 = cmds.iconTextButton(p=self.configuration_shape_layout_00, l='', i=controller.CONTROL.SPHERE.icon, style='iconOnly', w=self.sticky_shape_size_w, h=self.sticky_shape_size_h, c=partial(self.__change_shape, controller.CONTROL.SPHERE), ann=controller.CONTROL.SPHERE.name)
        self.configuration_shape_02 = cmds.iconTextButton(p=self.configuration_shape_layout_00, l='', i=controller.CONTROL.CUBE.icon, style='iconOnly', w=self.sticky_shape_size_w, h=self.sticky_shape_size_h, c=partial(self.__change_shape, controller.CONTROL.CUBE), ann=controller.CONTROL.CUBE.name)
        self.configuration_shape_03 = cmds.iconTextButton(p=self.configuration_shape_layout_00, l='', i=controller.CONTROL.CIRCLE_X.icon, style='iconOnly', w=self.sticky_shape_size_w, h=self.sticky_shape_size_h, c=partial(self.__change_shape, controller.CONTROL.CIRCLE_X), ann=controller.CONTROL.CIRCLE_X.name)
        self.configuration_shape_04 = cmds.iconTextButton(p=self.configuration_shape_layout_00, l='', i=controller.CONTROL.CIRCLE_Y.icon, style='iconOnly', w=self.sticky_shape_size_w, h=self.sticky_shape_size_h, c=partial(self.__change_shape, controller.CONTROL.CIRCLE_Y), ann=controller.CONTROL.CIRCLE_Y.name)
        self.configuration_shape_05 = cmds.iconTextButton(p=self.configuration_shape_layout_00, l='', i=controller.CONTROL.CIRCLE_Z.icon, style='iconOnly', w=self.sticky_shape_size_w, h=self.sticky_shape_size_h, c=partial(self.__change_shape, controller.CONTROL.CIRCLE_Z), ann=controller.CONTROL.CIRCLE_Z.name)
        self.configuration_shape_06 = cmds.iconTextButton(p=self.configuration_shape_layout_00, l='', i=controller.CONTROL.PYRAMID_INV.icon, style='iconOnly', w=self.sticky_shape_size_w, h=self.sticky_shape_size_h, c=partial(self.__change_shape, controller.CONTROL.PYRAMID_INV), ann=controller.CONTROL.PYRAMID_INV.name)
        self.configuration_shape_07 = cmds.iconTextButton(p=self.configuration_shape_layout_00, l='', i=controller.CONTROL.PYRAMID.icon, style='iconOnly', w=self.sticky_shape_size_w, h=self.sticky_shape_size_h, c=partial(self.__change_shape, controller.CONTROL.PYRAMID), ann=controller.CONTROL.PYRAMID.name)
        self.configuration_shape_08 = cmds.iconTextButton(p=self.configuration_shape_layout_00, l='', i=controller.CONTROL.CROSS.icon, style='iconOnly', w=self.sticky_shape_size_w, h=self.sticky_shape_size_h, c=partial(self.__change_shape, controller.CONTROL.CROSS), ann=controller.CONTROL.CROSS.name)
        cmds.formLayout(self.configuration_shape_layout_00, e=1,
                        attachPosition=[
                            (self.configuration_shape_01, 'left', 0, 0),
                            (self.configuration_shape_02, 'left', 0, 12.5),
                            (self.configuration_shape_03, 'left', 0, 25),
                            (self.configuration_shape_04, 'left', 0, 37.5),
                            (self.configuration_shape_05, 'left', 0, 50),
                            (self.configuration_shape_06, 'left', 0, 62.5),
                            (self.configuration_shape_07, 'left', 0, 75),
                            (self.configuration_shape_08, 'left', 0, 87.5),

                            (self.configuration_shape_01, 'right', 0, 12.5),
                            (self.configuration_shape_02, 'right', 0, 25),
                            (self.configuration_shape_03, 'right', 0, 37.5),
                            (self.configuration_shape_04, 'right', 0, 50),
                            (self.configuration_shape_05, 'right', 0, 62.5),
                            (self.configuration_shape_06, 'right', 0, 75),
                            (self.configuration_shape_07, 'right', 0, 87.5),
                            (self.configuration_shape_08, 'right', 0, 100),
                        ],
                        )

        self.configuration_color_layout_00 = cmds.formLayout(p=self.configuration_layout)
        self.configuration_color_01 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_01, ann='Color 01', c=partial(self.__change_color, 0))
        self.configuration_color_02 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_02, ann='Color 02', c=partial(self.__change_color, 1))
        self.configuration_color_03 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_03, ann='Color 03', c=partial(self.__change_color, 2))
        self.configuration_color_04 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_04, ann='Color 04', c=partial(self.__change_color, 3))
        self.configuration_color_05 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_05, ann='Color 05', c=partial(self.__change_color, 4))
        self.configuration_color_06 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_06, ann='Color 06', c=partial(self.__change_color, 5))
        self.configuration_color_07 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_07, ann='Color 07', c=partial(self.__change_color, 6))
        self.configuration_color_08 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_08, ann='Color 08', c=partial(self.__change_color, 7))
        self.configuration_color_09 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_09, ann='Color 09', c=partial(self.__change_color, 8))
        self.configuration_color_10 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_10, ann='Color 10', c=partial(self.__change_color, 9))
        self.configuration_color_11 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_11, ann='Color 11', c=partial(self.__change_color, 10))
        self.configuration_color_12 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_12, ann='Color 12', c=partial(self.__change_color, 11))
        self.configuration_color_13 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_13, ann='Color 13', c=partial(self.__change_color, 12))
        self.configuration_color_14 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_14, ann='Color 14', c=partial(self.__change_color, 13))
        self.configuration_color_15 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_15, ann='Color 15', c=partial(self.__change_color, 14))
        self.configuration_color_16 = cmds.iconTextButton(p=self.configuration_color_layout_00, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_16, ann='Color 16', c=partial(self.__change_color, 15))
        cmds.formLayout(self.configuration_color_layout_00, e=1,
                        attachPosition=[
                            (self.configuration_color_01, 'left', 0, 0),
                            (self.configuration_color_02, 'left', 0, 6.25),
                            (self.configuration_color_03, 'left', 0, 12.5),
                            (self.configuration_color_04, 'left', 0, 18.75),
                            (self.configuration_color_05, 'left', 0, 25),
                            (self.configuration_color_06, 'left', 0, 31.25),
                            (self.configuration_color_07, 'left', 0, 37.5),
                            (self.configuration_color_08, 'left', 0, 43.75),
                            (self.configuration_color_09, 'left', 0, 50),
                            (self.configuration_color_10, 'left', 0, 56.25),
                            (self.configuration_color_11, 'left', 0, 62.5),
                            (self.configuration_color_12, 'left', 0, 68.75),
                            (self.configuration_color_13, 'left', 0, 75),
                            (self.configuration_color_14, 'left', 0, 81.25),
                            (self.configuration_color_15, 'left', 0, 87.5),
                            (self.configuration_color_16, 'left', 0, 93.75),

                            (self.configuration_color_01, 'right', 0, 6.25),
                            (self.configuration_color_02, 'right', 0, 12.5),
                            (self.configuration_color_03, 'right', 0, 18.75),
                            (self.configuration_color_04, 'right', 0, 25),
                            (self.configuration_color_05, 'right', 0, 31.25),
                            (self.configuration_color_06, 'right', 0, 37.5),
                            (self.configuration_color_07, 'right', 0, 43.75),
                            (self.configuration_color_08, 'right', 0, 50),
                            (self.configuration_color_09, 'right', 0, 56.25),
                            (self.configuration_color_10, 'right', 0, 62.5),
                            (self.configuration_color_11, 'right', 0, 68.75),
                            (self.configuration_color_12, 'right', 0, 75),
                            (self.configuration_color_13, 'right', 0, 81.25),
                            (self.configuration_color_14, 'right', 0, 87.5),
                            (self.configuration_color_15, 'right', 0, 93.75),
                            (self.configuration_color_16, 'right', 0, 100),
                        ],
                        )

        self.configuration_color_layout_01 = cmds.formLayout(p=self.configuration_layout)
        self.configuration_color_17 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_17, ann='Color 17', c=partial(self.__change_color, 16))
        self.configuration_color_18 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_18, ann='Color 18', c=partial(self.__change_color, 17))
        self.configuration_color_19 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_19, ann='Color 19', c=partial(self.__change_color, 18))
        self.configuration_color_20 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_20, ann='Color 20', c=partial(self.__change_color, 19))
        self.configuration_color_21 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_21, ann='Color 21', c=partial(self.__change_color, 20))
        self.configuration_color_22 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_22, ann='Color 22', c=partial(self.__change_color, 21))
        self.configuration_color_23 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_23, ann='Color 23', c=partial(self.__change_color, 22))
        self.configuration_color_24 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_24, ann='Color 24', c=partial(self.__change_color, 23))
        self.configuration_color_25 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_25, ann='Color 25', c=partial(self.__change_color, 24))
        self.configuration_color_26 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_26, ann='Color 26', c=partial(self.__change_color, 25))
        self.configuration_color_27 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_27, ann='Color 27', c=partial(self.__change_color, 26))
        self.configuration_color_28 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_28, ann='Color 28', c=partial(self.__change_color, 27))
        self.configuration_color_29 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_29, ann='Color 29', c=partial(self.__change_color, 28))
        self.configuration_color_30 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_30, ann='Color 30', c=partial(self.__change_color, 29))
        self.configuration_color_31 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_31, ann='Color 31', c=partial(self.__change_color, 30))
        self.configuration_color_32 = cmds.iconTextButton(p=self.configuration_color_layout_01, l='', style='iconOnly', w=self.sticky_color_size_w, h=self.sticky_color_size_h, bgc=self.color_32, ann='Color 32', c=partial(self.__change_color, 31))

        cmds.formLayout(self.configuration_color_layout_01, e=1,
                        attachPosition=[
                            (self.configuration_color_17, 'left', 0, 0),
                            (self.configuration_color_18, 'left', 0, 6.25),
                            (self.configuration_color_19, 'left', 0, 12.5),
                            (self.configuration_color_20, 'left', 0, 18.75),
                            (self.configuration_color_21, 'left', 0, 25),
                            (self.configuration_color_22, 'left', 0, 31.25),
                            (self.configuration_color_23, 'left', 0, 37.5),
                            (self.configuration_color_24, 'left', 0, 43.75),
                            (self.configuration_color_25, 'left', 0, 50),
                            (self.configuration_color_26, 'left', 0, 56.25),
                            (self.configuration_color_27, 'left', 0, 62.5),
                            (self.configuration_color_28, 'left', 0, 68.75),
                            (self.configuration_color_29, 'left', 0, 75),
                            (self.configuration_color_30, 'left', 0, 81.25),
                            (self.configuration_color_31, 'left', 0, 87.5),
                            (self.configuration_color_32, 'left', 0, 93.75),

                            (self.configuration_color_17, 'right', 0, 6.25),
                            (self.configuration_color_18, 'right', 0, 12.5),
                            (self.configuration_color_19, 'right', 0, 18.75),
                            (self.configuration_color_20, 'right', 0, 25),
                            (self.configuration_color_21, 'right', 0, 31.25),
                            (self.configuration_color_22, 'right', 0, 37.5),
                            (self.configuration_color_23, 'right', 0, 43.75),
                            (self.configuration_color_24, 'right', 0, 50),
                            (self.configuration_color_25, 'right', 0, 56.25),
                            (self.configuration_color_26, 'right', 0, 62.5),
                            (self.configuration_color_27, 'right', 0, 68.75),
                            (self.configuration_color_28, 'right', 0, 75),
                            (self.configuration_color_29, 'right', 0, 81.25),
                            (self.configuration_color_30, 'right', 0, 87.5),
                            (self.configuration_color_31, 'right', 0, 93.75),
                            (self.configuration_color_32, 'right', 0, 100),
                        ],
                        )

        self.configuration_scale_slider = cmds.floatSliderGrp(p=self.configuration_layout,
                                                              l='',
                                                              field=True,
                                                              cw3=[0, 50, 100],
                                                              cl3=['left', 'left', 'left'],
                                                              ann='Scale')

        cmds.formLayout(self.configuration_layout, e=1,
                        attachForm=[
                            (self.configuration_title, 'top', 5),
                            (self.configuration_title, 'left', 5),

                            (self.configuration_options_layout, 'top', 5),
                            (self.configuration_options_layout, 'right', 5),

                            (self.configuration_shape_layout_00, 'left', 5),
                            (self.configuration_shape_layout_00, 'right', 5),

                            (self.configuration_color_layout_00, 'left', 5),
                            (self.configuration_color_layout_00, 'right', 5),

                            (self.configuration_color_layout_01, 'left', 5),
                            (self.configuration_color_layout_01, 'right', 5),

                            (self.configuration_scale_slider, 'right', 5),
                            (self.configuration_scale_slider, 'left', 5),
                            (self.configuration_scale_slider, 'bottom', 5),

                        ],
                        attachControl=[
                            (self.configuration_shape_layout_00, 'top', 10, self.configuration_options_layout),
                            (self.configuration_color_layout_00, 'top', 5, self.configuration_shape_layout_00),
                            (self.configuration_color_layout_01, 'top', 5, self.configuration_color_layout_00),
                            (self.configuration_scale_slider, 'top', 5, self.configuration_color_layout_01),
                        ]
                        )

        # Help Layout
        self.help_layout = cmds.formLayout(p=self.main_layout)
        self.help_button = cmds.iconTextButton(p=self.help_layout,
                                               l='Help',
                                               i=self.path_icon_help,
                                               style='iconOnly',
                                               w=self.icon_size, h=self.icon_size,
                                               ann='Help/About')
        self.help_line = cmds.helpLine(p=self.help_layout, w=100)

        cmds.formLayout(self.help_layout, e=1,
                        attachForm=[
                            (self.help_button, 'top', 0),
                            (self.help_button, 'left', 0),
                            (self.help_button, 'bottom', 0),
                            (self.help_line, 'top', 0),
                            (self.help_line, 'right', 0),
                            (self.help_line, 'bottom', 0),
                        ],
                        attachControl=[
                            (self.help_line, 'left', 0, self.help_button)
                        ])

        # Separators
        self.sticky_separator = cmds.separator(p=self.main_layout)
        self.configuration_separator = cmds.separator(p=self.main_layout)
        self.help_separator = cmds.separator(p=self.main_layout)

        # Main Layout
        cmds.formLayout(self.main_layout, e=1,
                        attachForm=[
                            (self.creation_layout, 'top', 0),
                            (self.creation_layout, 'left', 0),
                            (self.creation_layout, 'right', 0),

                            (self.sticky_separator, 'left', 0),
                            (self.sticky_separator, 'right', 0),
                            (self.sticky_layout, 'left', 0),
                            (self.sticky_layout, 'right', 0),

                            (self.configuration_separator, 'left', 0),
                            (self.configuration_separator, 'right', 0),
                            (self.configuration_layout, 'left', 0),
                            (self.configuration_layout, 'right', 0),

                            (self.help_separator, 'left', 0),
                            (self.help_separator, 'right', 0),
                            (self.help_layout, 'left', 0),
                            (self.help_layout, 'right', 0),
                            (self.help_layout, 'bottom', 0),
                        ],
                        attachControl=[
                            (self.sticky_separator, 'top', 5, self.creation_layout),
                            (self.sticky_layout, 'top', 5, self.sticky_separator),
                            (self.sticky_layout, 'bottom', 5, self.configuration_separator),
                            (self.configuration_separator, 'bottom', 5, self.configuration_layout),
                            (self.configuration_layout, 'bottom', 5, self.help_separator),
                            (self.help_separator, 'bottom', 5, self.help_layout),
                        ]
                        )

        # Connect
        cmds.radioButtonGrp(self.reference_mode_radio, e=1, cc=self.__reference_mode_change)
        cmds.iconTextButton(self.creation_reference_object_button, e=1, c=self.__select_reference_object)
        cmds.iconTextButton(self.creation_world_button, e=1, c=partial(self.__create, controller.ORIENT_MODE.WORLD))
        cmds.iconTextButton(self.creation_reference_button, e=1, c=partial(self.__create, controller.ORIENT_MODE.AS_REFERENCE))
        cmds.iconTextButton(self.creation_vertex_button, e=1, c=partial(self.__create, controller.ORIENT_MODE.AS_VERTEX))
        cmds.textScrollList(self.sticky_list, e=1, sc=self.__selection_change, dcc=self.__double_click_on_name)
        cmds.iconTextButton(self.configuration_weight_button, e=1, c=self.__weight_cluster)
        cmds.iconTextButton(self.configuration_member_button, e=1, c=self.__edit_members)
        cmds.iconTextButton(self.configuration_delete_button, e=1, c=self.__delete)

        cmds.iconTextButton(self.sticky_load_button, e=1, c=self.__load)
        cmds.iconTextButton(self.sticky_save_button, e=1, c=self.__save)
        cmds.iconTextButton(self.sticky_refresh_button, e=1, c=self.__refresh_list)

        cmds.floatSliderGrp(self.configuration_scale_slider, e=1, cc=self.__change_scale, dc=self.__change_scale)

        cmds.iconTextButton(self.help_button, e=1, c=self.__help)

        # Configuration
        self.__refresh_list()
        self.__selection_change(ui_mode=False)
        self.__reference_mode_change()

        # Script Jobs
        cmds.scriptJob(event=['SelectionChanged', self.__maya_selection_change], parent=self.main_window)
        cmds.scriptJob(event=['PostSceneRead', self.__new_scene], parent=self.main_window)
        cmds.scriptJob(event=['NewSceneOpened', self.__new_scene], parent=self.main_window)

        # Init
        cmds.showWindow(self.main_window)

    @property
    def selected(self):
        stickys = cmds.textScrollList(self.sticky_list, q=1, si=1)
        if not stickys:
            return []
        return [s.split(' ', 1)[0] for s in stickys]

    @property
    def selected_controls(self):
        controls = []
        for number in self.selected:
            ctl = self.controller.get_info_control(number)
            if cmds.objExists(ctl):
                controls.append(ctl)
        return controls

    @property
    def selected_clusters(self):
        clusters = []
        for number in self.selected:
            clusters.append(self.controller.get_info_cluster(number))
        return clusters

    @property
    def selected_names(self):
        names = []
        for number in self.selected:
            names.append(self.controller.get_info_name(number))
        return names

    @property
    def scale(self):
        return cmds.floatSliderGrp(self.configuration_scale_slider, q=1, v=1)

    @property
    def reference_mode(self):
        return cmds.radioButtonGrp(self.reference_mode_radio, q=1, sl=1)

    def __new_scene(self):
        self.__reference_mode_change()
        self.__refresh_list()

    def __reference_mode_change(self, *args):
        if self.reference_mode == controller.REFERENCE_MODE.AUTO:
            self.__disable_reference_object()
        else:
            self.__clear_reference_object()

    def __refresh_list(self, *args):
        cmds.textScrollList(self.sticky_list, e=1, ra=1)
        stickys = self.controller.list_systems()
        for number in stickys:
            name = self.controller.get_info_name(number)
            cmds.textScrollList(self.sticky_list, e=1, a='{0} {1}'.format(number, name))
        self.__maya_selection_change()

    def __maya_selection_change(self, *args):
        cmds.textScrollList(self.sticky_list, e=1, da=1)
        selected = self.controller.list_selected_systems()
        items = cmds.textScrollList(self.sticky_list, q=1, ai=1)
        for sel in selected:
            if not items:
                continue
            for item in items:
                if item.split(' ', 1)[0] == sel:
                    cmds.textScrollList(self.sticky_list, e=1, si=item)
        self.__selection_change(ui_mode=False)

    def __double_click_on_name(self, *args):
        selected = self.selected
        if selected.__len__() != 1:
            return
        old_name = self.controller.get_info_name(selected[0])
        result = cmds.promptDialog(title='Rename Sticky',
                                   message='New Name:',
                                   button=['OK', 'Cancel'],
                                   text=old_name,
                                   defaultButton='OK',
                                   cancelButton='Cancel',
                                   dismissString='Cancel')

        if result != 'OK':
            return

        name = cmds.promptDialog(query=True, text=True)

        for number in self.selected:
            self.controller.set_name(number, name)
        self.__refresh_list()

    def __selection_change(self, ui_mode=True, *args):
        controls = self.selected_controls

        if not controls:
            cmds.iconTextButton(self.configuration_weight_button, e=1, en=0)
            cmds.iconTextButton(self.configuration_member_button, e=1, en=0)
            cmds.iconTextButton(self.configuration_delete_button, e=1, en=0)
            cmds.formLayout(self.configuration_shape_layout_00, e=1, en=0)
            cmds.formLayout(self.configuration_color_layout_00, e=1, en=0)
            cmds.formLayout(self.configuration_color_layout_01, e=1, en=0)
            cmds.floatSliderGrp(self.configuration_scale_slider, e=1, en=0)
            cmds.iconTextButton(self.configuration_color_01, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_02, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_03, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_04, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_05, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_06, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_07, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_08, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_09, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_10, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_11, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_12, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_13, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_14, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_15, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_16, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_17, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_18, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_19, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_20, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_21, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_22, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_23, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_24, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_25, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_26, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_27, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_28, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_29, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_30, e=1, bgc=self.color_disabled_a)
            cmds.iconTextButton(self.configuration_color_31, e=1, bgc=self.color_disabled_b)
            cmds.iconTextButton(self.configuration_color_32, e=1, bgc=self.color_disabled_a)
            if ui_mode:
                cmds.select(cl=1)
            return
        elif controls.__len__() > 1:
            cmds.iconTextButton(self.configuration_weight_button, e=1, en=0)
            cmds.iconTextButton(self.configuration_member_button, e=1, en=0)
        else:
            cmds.iconTextButton(self.configuration_weight_button, e=1, en=1)
            cmds.iconTextButton(self.configuration_member_button, e=1, en=1)

        cmds.iconTextButton(self.configuration_color_01, e=1, bgc=self.color_01)
        cmds.iconTextButton(self.configuration_color_02, e=1, bgc=self.color_02)
        cmds.iconTextButton(self.configuration_color_03, e=1, bgc=self.color_03)
        cmds.iconTextButton(self.configuration_color_04, e=1, bgc=self.color_04)
        cmds.iconTextButton(self.configuration_color_05, e=1, bgc=self.color_05)
        cmds.iconTextButton(self.configuration_color_06, e=1, bgc=self.color_06)
        cmds.iconTextButton(self.configuration_color_07, e=1, bgc=self.color_07)
        cmds.iconTextButton(self.configuration_color_08, e=1, bgc=self.color_08)
        cmds.iconTextButton(self.configuration_color_09, e=1, bgc=self.color_09)
        cmds.iconTextButton(self.configuration_color_10, e=1, bgc=self.color_10)
        cmds.iconTextButton(self.configuration_color_11, e=1, bgc=self.color_11)
        cmds.iconTextButton(self.configuration_color_12, e=1, bgc=self.color_12)
        cmds.iconTextButton(self.configuration_color_13, e=1, bgc=self.color_13)
        cmds.iconTextButton(self.configuration_color_14, e=1, bgc=self.color_14)
        cmds.iconTextButton(self.configuration_color_15, e=1, bgc=self.color_15)
        cmds.iconTextButton(self.configuration_color_16, e=1, bgc=self.color_16)
        cmds.iconTextButton(self.configuration_color_17, e=1, bgc=self.color_17)
        cmds.iconTextButton(self.configuration_color_18, e=1, bgc=self.color_18)
        cmds.iconTextButton(self.configuration_color_19, e=1, bgc=self.color_19)
        cmds.iconTextButton(self.configuration_color_20, e=1, bgc=self.color_20)
        cmds.iconTextButton(self.configuration_color_21, e=1, bgc=self.color_21)
        cmds.iconTextButton(self.configuration_color_22, e=1, bgc=self.color_22)
        cmds.iconTextButton(self.configuration_color_23, e=1, bgc=self.color_23)
        cmds.iconTextButton(self.configuration_color_24, e=1, bgc=self.color_24)
        cmds.iconTextButton(self.configuration_color_25, e=1, bgc=self.color_25)
        cmds.iconTextButton(self.configuration_color_26, e=1, bgc=self.color_26)
        cmds.iconTextButton(self.configuration_color_27, e=1, bgc=self.color_27)
        cmds.iconTextButton(self.configuration_color_28, e=1, bgc=self.color_28)
        cmds.iconTextButton(self.configuration_color_29, e=1, bgc=self.color_29)
        cmds.iconTextButton(self.configuration_color_30, e=1, bgc=self.color_30)
        cmds.iconTextButton(self.configuration_color_31, e=1, bgc=self.color_31)
        cmds.iconTextButton(self.configuration_color_32, e=1, bgc=self.color_32)

        cmds.iconTextButton(self.configuration_delete_button, e=1, en=1)
        cmds.formLayout(self.configuration_shape_layout_00, e=1, en=1)
        cmds.formLayout(self.configuration_color_layout_00, e=1, en=1)
        cmds.formLayout(self.configuration_color_layout_01, e=1, en=1)
        cmds.floatSliderGrp(self.configuration_scale_slider, e=1, en=1)

        size = cmds.getAttr('{0}.size'.format(controls[-1]))
        cmds.floatSliderGrp(self.configuration_scale_slider, e=1, v=size)

        if ui_mode:
            cmds.select(controls, r=1)

    def __load(self, *args):
        path = cmds.fileDialog2(fileFilter='*.txs', dialogStyle=2, fileMode=1, caption='Save Selected Sticky Controllers', okCaption='Load')
        if not path:
            return

        StickyLoaderUI(self, path[0])

        self.__refresh_list()

    def __save(self, *args):
        selected = self.selected
        if not selected:
            return

        path = cmds.fileDialog2(fileFilter='*.txs', dialogStyle=2, fileMode=0, caption='Save Selected Sticky Controllers', okCaption='Save')
        if not path:
            return

        self.controller.save_systems(self.selected, path[0])

    def __weight_cluster(self, *args):
        clusters = self.selected_clusters
        if clusters.__len__() != 1:
            return
        cluster = clusters[0]
        shapes = cmds.cluster(cluster, q=1, geometry=1)
        if not shapes:
            return

        transforms = cmds.listRelatives(shapes, p=1)
        if not transforms:
            return

        cmds.select(transforms, r=1)

        cmds.toolPropertyWindow(inMainWindow=1)
        mel.eval('artSetToolAndSelectAttr( "artAttrCtx", "cluster.' + cluster + '.weights" );')

    def __edit_members(self, *args):
        clusters = self.selected_clusters
        if clusters.__len__() == 1:
            cmds.EditMembershipTool()
            cmds.select(clusters[0], r=1)

    def __change_color(self, color, *args):
        for number in self.selected:
            self.controller.set_color(number, color)

    def __change_shape(self, shape, *args):
        for number in self.selected:
            self.controller.set_shape(number, shape)

    def __change_scale(self, *args):
        scale = self.scale
        for number in self.selected:
            self.controller.set_scale(number, scale)

    def __select_reference_object(self, *args):
        selected = self.controller.get_reference_object()
        if not selected:
            cmds.confirmDialog(title='Select One Object', message='Select One Object for reference')
            self.__clear_reference_object()
            return

        cmds.text(self.creation_reference_object, e=1, label=selected, en=1)
        cmds.iconTextButton(self.creation_reference_object_icon, e=1, vis=0, en=1)
        cmds.iconTextButton(self.creation_world_button, e=1, bgc=self.color_ok, en=1)
        cmds.iconTextButton(self.creation_reference_button, e=1, bgc=self.color_ok, en=1)
        cmds.iconTextButton(self.creation_vertex_button, e=1, bgc=self.color_ok, en=1)

    def __clear_reference_object(self, *args):
        cmds.iconTextButton(self.creation_reference_object_button, e=1, en=1)
        cmds.text(self.creation_reference_object, e=1, label='', en=1)
        cmds.iconTextButton(self.creation_reference_object_icon, e=1, vis=1, en=1)
        cmds.iconTextButton(self.creation_world_button, e=1, bgc=self.color_bad, en=1)
        cmds.iconTextButton(self.creation_reference_button, e=1, bgc=self.color_bad, en=1)
        cmds.iconTextButton(self.creation_vertex_button, e=1, bgc=self.color_bad, en=1)

    def __disable_reference_object(self, *args):
        cmds.iconTextButton(self.creation_reference_object_button, e=1, en=0)
        cmds.text(self.creation_reference_object, e=1, label='AUTO (Experimental)', en=0)
        cmds.iconTextButton(self.creation_reference_object_icon, e=1, vis=0, en=0)
        cmds.iconTextButton(self.creation_world_button, e=1, bgc=self.color_ok, en=1)
        cmds.iconTextButton(self.creation_reference_button, e=1, bgc=self.color_ok, en=1)
        cmds.iconTextButton(self.creation_vertex_button, e=1, bgc=self.color_ok, en=1)

    def __create(self, orient, *args):
        if self.reference_mode == controller.REFERENCE_MODE.AUTO:
            self.controller.create(reference_object=None, reference_mode=controller.REFERENCE_MODE.AUTO, orient=orient, scui=self)
            self.__refresh_list()
            self.__selection_change()
        else:
            reference_object = cmds.text(self.creation_reference_object, q=1, label=1)
            if reference_object and cmds.objExists(reference_object):
                self.controller.create(reference_object=reference_object, orient=orient, scui=self)
                self.__refresh_list()
                self.__selection_change()

    def external_refresh(self, *args):
        self.__refresh_list()
        self.__selection_change()

    def __delete(self, *args):
        if cmds.confirmDialog(title='Delete Sticky Controllers', message='Delete Selected Sticky Controller.\nAre you sure?', button=['Yes', 'No'], defaultButton='No', cancelButton='No', dismissString='No') == 'Yes':
            for number in self.selected:
                self.controller.delete_system(number)
            self.__refresh_list()

    def __help(self, *args):
        import webbrowser
        webbrowser.open(__web__)


class StickyLoaderUI(object):
    def __init__(self, sc_ui, path):
        self.sc_ui = sc_ui
        self.path = path
        self.__sticky_controllers = []

        self.position_name_size = 100
        self.position_orient_size = 100
        self.position_reference_vertex_middle = 52

        # Main Window
        self.main_window = 'tx_stickyLoaderUI'
        if cmds.window(self.main_window, exists=1):
            cmds.deleteUI(self.main_window)
        cmds.window(self.main_window, t='Sticky Loader UI')

        # Main Layout
        self.main_layout = cmds.formLayout(parent=self.main_window, w=500)

        self.title_layout = cmds.formLayout(parent=self.main_window)
        self.checkbox_label = cmds.checkBox(parent=self.title_layout, label='')
        self.name_label = cmds.text(parent=self.title_layout, label=' Name', align='left', w=self.position_name_size)
        self.reference_label = cmds.text(parent=self.title_layout, label=' Reference', align='left')
        self.vertex_label = cmds.text(parent=self.title_layout, label=' Vertex', align='left')
        self.orient_label = cmds.text(parent=self.title_layout, label=' Orient', align='left', w=self.position_orient_size)

        cmds.formLayout(self.title_layout, e=1,
                        attachForm=[
                            (self.checkbox_label, 'top', 5),
                            (self.checkbox_label, 'left', 5),

                            (self.name_label, 'top', 5),

                            (self.reference_label, 'top', 5),

                            (self.vertex_label, 'top', 5),

                            (self.orient_label, 'top', 5),
                            (self.orient_label, 'right', 5),
                        ],
                        attachControl=[
                            (self.name_label, 'left', 5, self.checkbox_label),
                            (self.reference_label, 'left', 5, self.name_label),
                            (self.vertex_label, 'right', 5, self.orient_label),
                        ],
                        attachPosition=[
                            (self.reference_label, 'right', 5, self.position_reference_vertex_middle),
                            (self.vertex_label, 'left', 5, self.position_reference_vertex_middle),
                        ],
                        )

        self.sticky_layout = cmds.scrollLayout(parent=self.main_layout, cr=1, bv=1)

        self.load_button = cmds.button(parent=self.main_layout, label='CREATE')

        cmds.formLayout(self.main_layout, e=1,
                        attachForm=[
                            (self.title_layout, 'top', 5),
                            (self.title_layout, 'left', 9),
                            (self.title_layout, 'right', 9),

                            (self.sticky_layout, 'top', 30),
                            (self.sticky_layout, 'left', 5),
                            (self.sticky_layout, 'right', 5),
                            (self.sticky_layout, 'bottom', 32),

                            (self.load_button, 'left', 5),
                            (self.load_button, 'right', 5),
                            (self.load_button, 'bottom', 5),
                        ],

                        # attachPosition=[
                        #     (self.name_label, 'right', 5, 25),
                        #
                        #     (self.reference_label, 'left', 8, 25),
                        #     (self.reference_label, 'right', 5, 50),
                        #
                        #     (self.vertex_label, 'left', 5, 50),
                        #     (self.vertex_label, 'right', 110, 100),
                        #
                        # ],
                        )

        # Connect
        cmds.button(self.load_button, e=1, c=self.__load_controllers)
        cmds.checkBox(self.checkbox_label, e=1, cc=self.__change_global_selection)

        # Configuration
        self.__refresh()
        cmds.showWindow(self.main_window)

    @property
    def global_selection(self):
        return cmds.checkBox(self.checkbox_label, q=1, v=1)

    @property
    def sticky_controllers(self):
        return self.__sticky_controllers

    @global_selection.setter
    def global_selection(self, value):
        cmds.checkBox(self.checkbox_label, e=1, v=value)

    def __refresh(self):
        self.__sticky_controllers = []
        try:
            with open(self.path) as json_file:
                dic = json.load(json_file)
        except:
            return

        for number in dic:
            self.__sticky_controllers.append(StickyLoaderWidget(parent=self,
                                                                name=dic[number]['name'],
                                                                reference_object=dic[number]['reference_object'],
                                                                color=dic[number]['color'],
                                                                first_vertex=dic[number]['first_vertex'],
                                                                orient_mode=dic[number]['orient_mode'],
                                                                shape=dic[number]['shape'],
                                                                weight_members=dic[number]['weight_members'],
                                                                size=dic[number]['size']))

    def __change_global_selection(self, *args):
        for sc in self.__sticky_controllers:
            sc.state = self.global_selection

    def __load_controllers(self, *args):
        for sc in self.__sticky_controllers:
            sc.load_controller()


class StickyLoaderWidget(object):
    def __init__(self, parent, name, reference_object, color, first_vertex, orient_mode, shape, weight_members, size):
        self.main_path = os.path.dirname(__file__)
        self.path_icon_select = '{0}/icons/select_reference.png'.format(self.main_path)
        self.path_icon_change = '{0}/icons/refresh.png'.format(self.main_path)
        self.path_icon_options = '{0}/icons/options.png'.format(self.main_path)
        self.color_ok = [0.22, 0.8, 0.22]
        self.color_bad = [0.8, 0.22, 0.22]
        self.color_change = [0.46, 0.46, 0.46]
        self.color_default = [0.25, 0.25, 0.25]

        self.__color = color
        self.__shape = getattr(controller.CONTROL, shape)
        self.__weight_members = weight_members
        self.__size = size
        self.__reference_object = reference_object
        self.__first_vertex = first_vertex
        self.parent = parent

        self.main_layout = cmds.formLayout(parent=self.parent.sticky_layout)

        self.state_checkbox = cmds.checkBox(parent=self.main_layout, label='')

        self.name_textfield = cmds.textField(parent=self.main_layout, text=name, w=self.parent.position_name_size)

        self.reference_object_layout = cmds.rowLayout(parent=self.main_layout, adj=1, nc=2)
        self.reference_object_textfield = cmds.textField(parent=self.reference_object_layout, text=reference_object, ed=0)
        self.reference_object_icon = cmds.iconTextButton(parent=self.reference_object_layout, label='Select', style='iconOnly', i=self.path_icon_options, w=20, h=20)
        self.reference_object_popupmenu = cmds.popupMenu(parent=self.reference_object_icon, button=1)
        self.reference_object_popupmenu_check = cmds.menuItem(parent=self.reference_object_popupmenu, label='Check')
        self.reference_object_popupmenu_select = cmds.menuItem(parent=self.reference_object_popupmenu, label='Select')
        self.reference_object_popupmenu_change = cmds.menuItem(parent=self.reference_object_popupmenu, label='Change')
        self.reference_object_popupmenu_restore = cmds.menuItem(parent=self.reference_object_popupmenu, label='Restore')

        self.first_vertex_layout = cmds.rowLayout(parent=self.main_layout, adj=1, nc=2)
        self.first_vertex_textfield = cmds.textField(parent=self.first_vertex_layout, text=first_vertex, ed=0)
        self.first_vertex_icon = cmds.iconTextButton(parent=self.first_vertex_layout, label='Select', style='iconOnly', i=self.path_icon_options, w=20, h=20)
        self.first_vertex_popupmenu = cmds.popupMenu(parent=self.first_vertex_icon, button=1)
        self.first_vertex_popupmenu_check = cmds.menuItem(parent=self.first_vertex_popupmenu, label='Check')
        self.first_vertex_popupmenu_select = cmds.menuItem(parent=self.first_vertex_popupmenu, label='Select')
        self.first_vertex_popupmenu_change = cmds.menuItem(parent=self.first_vertex_popupmenu, label='Change')
        self.first_vertex_popupmenu_restore = cmds.menuItem(parent=self.first_vertex_popupmenu, label='Restore')

        self.orient_mode_optionmenu = cmds.optionMenu(parent=self.main_layout, w=self.parent.position_orient_size)
        cmds.menuItem(parent=self.orient_mode_optionmenu, label='World')
        cmds.menuItem(parent=self.orient_mode_optionmenu, label='Reference')
        cmds.menuItem(parent=self.orient_mode_optionmenu, label='Vertex')
        cmds.optionMenu(self.orient_mode_optionmenu, e=1, select=int(orient_mode) + 1)

        cmds.formLayout(self.main_layout, e=1,
                        attachForm=[
                            (self.state_checkbox, 'top', 8),
                            (self.state_checkbox, 'left', 5),

                            (self.name_textfield, 'top', 5),

                            (self.reference_object_layout, 'top', 3),

                            (self.first_vertex_layout, 'top', 3),

                            (self.orient_mode_optionmenu, 'top', 5),
                            (self.orient_mode_optionmenu, 'right', 5),
                        ],
                        attachControl=[
                            (self.name_textfield, 'left', 5, self.state_checkbox),
                            (self.first_vertex_layout, 'right', 5, self.orient_mode_optionmenu),
                            (self.reference_object_layout, 'left', 5, self.name_textfield),
                        ],
                        attachPosition=[
                            (self.reference_object_layout, 'right', 5, self.parent.position_reference_vertex_middle),
                            (self.first_vertex_layout, 'left', 5, self.parent.position_reference_vertex_middle),
                        ],
                        )

        # Connect
        cmds.menuItem(self.reference_object_popupmenu_check, e=1, c=self.__check_reference)
        cmds.menuItem(self.reference_object_popupmenu_select, e=1, c=self.__select_reference)
        cmds.menuItem(self.reference_object_popupmenu_change, e=1, c=self.__change_reference)
        cmds.menuItem(self.reference_object_popupmenu_restore, e=1, c=self.__restore_reference)

        cmds.menuItem(self.first_vertex_popupmenu_check, e=1, c=self.__check_vertex)
        cmds.menuItem(self.first_vertex_popupmenu_select, e=1, c=self.__select_vertex)
        cmds.menuItem(self.first_vertex_popupmenu_change, e=1, c=self.__change_vertex)
        cmds.menuItem(self.first_vertex_popupmenu_restore, e=1, c=self.__restore_vertex)

    @property
    def state(self):
        return cmds.checkBox(self.state_checkbox, q=1, v=1)

    @state.setter
    def state(self, value):
        cmds.checkBox(self.state_checkbox, e=1, v=value)

    @property
    def name(self):
        return cmds.textField(self.name_textfield, q=1, text=1)

    @property
    def reference_object(self):
        return cmds.textField(self.reference_object_textfield, q=1, text=1)

    @property
    def color(self):
        return self.__color

    @property
    def first_vertex(self):
        return cmds.textField(self.first_vertex_textfield, q=1, text=1)

    @property
    def orient_mode(self):
        return cmds.optionMenu(self.orient_mode_optionmenu, q=1, sl=1) - 1

    @property
    def shape(self):
        return self.__shape

    @property
    def weight_members(self):
        return self.__weight_members

    @property
    def size(self):
        return self.__size

    def load_controller(self, *args):
        if self.state:
            self.parent.sc_ui.controller.create(reference_object=self.reference_object,
                                                orient=self.orient_mode,
                                                control_shape=self.shape,
                                                color=self.color,
                                                size=self.size,
                                                values=self.weight_members,
                                                first_component=self.first_vertex)

            self.parent.sc_ui.external_refresh()
            self.state = False

    def __select_reference(self, *args):
        if cmds.objExists(self.reference_object):
            cmds.select(self.reference_object, r=1)
        else:
            cmds.select(cl=1)

    def __change_reference(self, *args):
        selection = cmds.ls(sl=1, type='transform')
        if selection and len(selection) == 1:
            cmds.textField(self.reference_object_textfield, e=1, text=selection[0])
            cmds.textField(self.reference_object_textfield, e=1, bgc=self.color_change)

    def __restore_reference(self, *args):
        cmds.textField(self.reference_object_textfield, e=1, text=self.__reference_object)
        cmds.textField(self.reference_object_textfield, e=1, bgc=self.color_default)

    def __check_reference(self, *args):
        if cmds.objExists(self.reference_object):
            cmds.textField(self.reference_object_textfield, e=1, bgc=self.color_ok)
        else:
            cmds.textField(self.reference_object_textfield, e=1, bgc=self.color_bad)

    def __select_vertex(self, *args):
        if cmds.objExists(self.first_vertex):
            cmds.select(self.first_vertex, r=1)
        else:
            cmds.select(cl=1)

    def __change_vertex(self, *args):
        selection = cmds.ls(sl=1, fl=1)
        if selection and len(selection) == 1 and re.search('\.vtx\[[0-9]+\]$', selection[0]):
            cmds.textField(self.first_vertex_textfield, e=1, text=selection[0])
            cmds.textField(self.first_vertex_textfield, e=1, bgc=self.color_change)

    def __restore_vertex(self, *args):
        cmds.textField(self.first_vertex_textfield, e=1, text=self.__first_vertex)
        cmds.textField(self.first_vertex_textfield, e=1, bgc=self.color_default)

    def __check_vertex(self, *args):
        if cmds.objExists(self.first_vertex):
            cmds.textField(self.first_vertex_textfield, e=1, bgc=self.color_ok)
        else:
            cmds.textField(self.first_vertex_textfield, e=1, bgc=self.color_bad)
