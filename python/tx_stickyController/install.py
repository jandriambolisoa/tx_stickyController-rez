import os
import re
import shutil
import maya.cmds as cmds
import maya.mel as mel


def install():
    # Search paths
    main_path = os.path.dirname(__file__)
    main_shelf = mel.eval('$tempMelVar=$gShelfTopLevel')
    current_shelf = cmds.tabLayout(main_shelf, query=1, selectTab=1)
    icon_path = '{0}/icons/icon.png'.format(main_path)
    maya_version = os.path.basename(os.path.dirname(cmds.about(env=1)))
    plugin_extension = 'py'
    if cmds.about(win64=1):
        plugin_extension = 'mll'
    elif cmds.about(macOSx86=1):
        plugin_extension = 'lib'
    elif cmds.about(linux64=1):
        plugin_extension = 'os'
    plugin_folder = '{0}/tx_stickyPoint'.format(main_path)
    plugin_path_universal = '{0}/universal/tx_stickyPoint.py'.format(plugin_folder)
    plugin_path_compiled = '{0}/{1}/tx_stickyPoint.{2}'.format(plugin_folder, maya_version, plugin_extension)
    if os.path.exists(plugin_path_compiled):
        plugin_path = plugin_path_compiled
    else:
        plugin_path = plugin_path_universal
        plugin_extension = 'py'
    plugin_folder = os.path.dirname(plugin_path)
    maya_env = cmds.about(env=1)
    maya_env_temp = maya_env + '_temp'

    # Write new maya.env
    f_src = open(maya_env, 'rt')
    f_dst = open(maya_env_temp, 'wt')
    valid_paths = []
    for l in f_src:
        if re.search('MAYA_PLUG_IN_PATH', l):
            paths_search = re.search('MAYA_PLUG_IN_PATH *= *(.*)', l)
            if paths_search:
                valid_paths = [p for p in paths_search.groups()[0].split(';') if not re.search('tx_stickyPoint', p)]
        else:
            if re.search('\n$', l):
                f_dst.write(l)
            else:
                f_dst.write('{0}\n'.format(l))
    valid_paths.append(plugin_folder)
    valid_paths = ';'.join(valid_paths)
    f_dst.write('MAYA_PLUG_IN_PATH = {0}'.format(valid_paths))
    f_src.close()
    f_dst.close()
    os.remove(maya_env)
    shutil.copy(maya_env_temp, maya_env)
    os.remove(maya_env_temp)

    # Add plugin folder to Maya Plugins
    mel.eval('putenv "MAYA_PLUG_IN_PATH" (`getenv "MAYA_PLUG_IN_PATH"`+";{0}")'.format(plugin_folder))

    # Try autoload Sticky Controller
    load_exception = False
    try:
        cmds.loadPlugin(plugin_path, qt=True)
    except:
        cmds.confirmDialog(title='WARNING: Restart Maya', message='\nCan\'t enable Sticky Controller automatically\n\nYou need restart Maya and run Sticky Controller\n', button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK')

    # Set autoload for next restart
    try:
        cmds.pluginInfo(plugin_path, edit=1, autoload=True)
    except:
        cmds.confirmDialog(title='WARNING: Restart Maya', message='\nCan\'t enable Sticky Controller automatically\n\nYou need restart Maya and run Sticky Controller\n', button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK')

    # Delete previous Sticky Controller buttons in current Shelf
    delete_buttons = []
    shelf_buttons = cmds.shelfLayout(current_shelf, q=1, ca=1)
    if shelf_buttons:
        for b in shelf_buttons:
            button_name = ''
            try:
                button_name = cmds.shelfButton(b, q=1, l=1)
            except:
                continue
            if button_name == 'Sticky Controller':
                delete_buttons.append(b)
    for b in delete_buttons:
        cmds.deleteUI(b)

    # Add new Sticky Controller button
    cmds.shelfButton(command='import sys\nif not sys.path.__contains__(\'{0}\'):\n    sys.path.insert(0, \'{0}\')\nimport tx_stickyController.ui\ntx_stickyController.ui.StickyControllerUI()'.format(os.path.dirname(main_path)),
                     annotation='Sticky Controller',
                     label='Sticky Controller',
                     sourceType='python',
                     imageOverlayLabel='txSC',
                     image=icon_path,
                     image1=icon_path,
                     p=current_shelf)


def onMayaDroppedPythonFile(*args):
    install()
