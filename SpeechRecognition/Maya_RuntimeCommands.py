import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import subprocess

def get_command_from_dict(command):

    command_dict = {'paint weights': 'cmds.ArtPaintSkinWeightsToolOptions()',
                    'paint skin weights': 'cmds.ArtPaintSkinWeightsToolOptions()',
                    'paint whites': 'cmds.ArtPaintSkinWeightsToolOptions()',
                    'paint skin whites': 'cmds.ArtPaintSkinWeightsToolOptions()',
                    'set timeline to selected': 'set_timeline_to_selected()',
                    'timeline to selected': 'set_timeline_to_selected()',
                    'set timeline to selection': 'set_timeline_to_selected()',
                    'timeline to selection': 'set_timeline_to_selected()',
                    'toggle state': 'toggle_state()',
                    'skin copy': 'skin_copy()',
                    'parent snap': 'snap(\'parent\')',
                    'orient snap': 'snap(\'orient\')',
                    'point snap': 'snap(\'point\')'
                    }
    try:
        return command_dict[command]
    except:
        return(False)

def get_command(command):
command = 'paint skin weights'
command_dict = {'cmds.ArtPaintSkinWeightsToolOptions()': ['skin', 'paint', 'weight', 'weights', 'white', 'whites', 'tool'],
                'set_timeline_to_selected()': ['set', 'timeline', 'selected', 'selection'],
                'toggle_state()': ['toggle', 'node', 'state'],
                'skin_copy()': ['copy', 'skin', 'weights', 'whites'],
                'snap(\'parent\')': ['parent', 'snap'],
                'snap(\'point\')': ['point', 'snap'],
                'snap(\'orient\')': ['orient', 'Orient', 'snap']
}
probability = []
for key, value in command_dict.items():
    print(key, value)


def set_timeline_to_selected():
    try:
        firstframe = min(pm.keyframe(pm.ls(sl=1), q=1))
        lastframe = max(pm.keyframe(pm.ls(sl=1), q=1))
        pm.playbackOptions(ast=firstframe, aet=lastframe, min=firstframe, max=lastframe)
    except Exception as e:
        print(e)

def toggle_state():
    constraintTypes = ['parentConstraint',
                        'pointConstraint',
                        'orientConstraint',
                        'scaleConstraint']
    
    currentState = False
    newState = False
    
    for s in pm.ls(sl=1):
        if str(s.nodeType()) in constraintTypes:
            if not currentState:
                currentState = s.nodeState.get()
                if not currentState == 0:
                    newState = 0
                else:
                    newState = 2
            if newState == 0:
                print('setting {0}.nodeState to normal'.format(s.name()))
            if newState == 2:
                print('setting {0}.nodeState to blocking'.format(s.name()))
            s.nodeState.set(newState)

def skin_copy():
    sources = pm.ls(sl=1)
    target = sources.pop(-1)
    
    influences = []
    source_skinclusters = []
    for source in sources:
        skincluster = pm.PyNode(mel.eval('findRelatedSkinCluster("'+source.name()+'")'))
        source_skinclusters.append(skincluster)
        for inf in skincluster.getInfluence():
            if not inf in influences:
                influences.append(inf)
               
    
    
    if mel.eval('findRelatedSkinCluster("'+target.name()+'")'):
        pm.delete(mel.eval('findRelatedSkinCluster("'+target.name()+'")'))
    trgt_skincluster = pm.skinCluster(influences, target, tsb=True)
    
    
    # using mel.eval for copy weight as pymel doesn't support multiple sources :-/
    pm.select(sources, target, r=1)
    cmds.copySkinWeights(noMirror=True,
                                surfaceAssociation='closestPoint',
                                influenceAssociation='oneToOne',
                                normalize=True)

def snap(type = ''):
    if type == 'parent':
        source = pm.ls(sl=1)
        target = source.pop()
        pm.delete(pm.parentConstraint(source, target))
    if type == 'orient':
        source = pm.ls(sl=1)
        target = source.pop()
        pm.delete(pm.orientConstraint(source, target))
    if type == 'point':
        source = pm.ls(sl=1)
        target = source.pop()
        pm.delete(pm.pointConstraint(source, target))


def main():
    pl = subprocess.run('python D:/GitHub/Maya/SpeechRecognition/speechrec.py', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('\n\nReturned string: {0}'.format(pl.stdout))
    slice = str(pl.stdout)[2:-5].lower()
    print('Sliced string: {0}'.format(slice))
    command = get_command_from_dict(str(pl.stdout)[2:-5])
    print('Command : {0}\n\n'.format(command))
    exec(command)

main()
