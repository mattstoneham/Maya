import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import subprocess

command_dict = {'cmds.ArtPaintSkinWeightsToolOptions()': ['skin', 'paint', 'painting', 'weight', 'weights', 'white', 'whites', 'tool'],
                'set_timeline_to_selected()': ['set', 'timeline', 'selected', 'selection'],
                'toggle_state()': ['toggle', 'node', 'state'],
                'skin_copy()': ['copy', 'skin', 'weights', 'whites'],
                'snap(\'parent\')': ['parent', 'snap'],
                'snap(\'point\')': ['point', 'translate', 'translation', 'snap'],
                'snap(\'orient\')': ['orient', 'Orient', 'orientation', 'rotate', 'rotation', 'snap']
}


def get_all_command_keywords():
    keywords = []
    for key, values in command_dict.items():
        for value in values:
            keywords.append(value)
    return keywords

def strip_non_keywords_from_text(text):
    stripped = []
    all_keywords = get_all_command_keywords()
    for item in text.split(' '):
        if item in all_keywords:
            stripped.append(item)
    return stripped


def get_command(command, confidence_threshold=50):
    # strip all non keywords from the passed speech-to-text result
    strippedcommand = strip_non_keywords_from_text(command)
    if strippedcommand:
        percentmatch_dict = {}
        # count speech-to-text keyword occurrences in command dict
        for key, values in command_dict.items():
            occurrences = len(list(set(strippedcommand) & set(values)))
            percentmatch_dict[key] = ((100 / len(strippedcommand)) * occurrences)
        #print(percentmatch_dict)
        # filter out highest match above confidence threshold
        high = 0
        for key, value in percentmatch_dict.items():
            if value > confidence_threshold and value > high:
                key_store = key
                value_store = value
                high = value
        returned_command = {}
        returned_command[key_store] = value_store
        return returned_command

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



# test below this line


def test_voice_commands(command_list, confidence_threshold=50):
    for command in command_list:
        returned_command = get_command(command, confidence_threshold=confidence_threshold)
        print(command, ':', returned_command)

'''

command_list = ['cpen the skin weights paint tool',
                'copy skin weights',
                'paint skin weights',
                'copy weights',
                'I need a cup of tea',
                'snap orientation',
                'snap to point',
                'parent snap',
                'set timeline to selection'
]
test_voice_commands(command_list)

text = 'Open the skin weights paint tool'
strip_non_keywords_from_text(text)

'''