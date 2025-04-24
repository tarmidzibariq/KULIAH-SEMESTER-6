# ------------------------------------------------------------------------------
#   BSD 2-Clause License
#
# Copyright (c) 2019-2023, Thomas Larsson
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice, this
#      list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#   FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#   DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#   SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#   CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ------------------------------------------------------------------------------

import bpy
from .utils import *

#-------------------------------------------------------------
#   Bone layers
#-------------------------------------------------------------

L_MAIN =    0
L_SPINE = 1

L_LARMIK =  2
L_LARMFK =  3
L_LLEGIK =  4
L_LLEGFK =  5
L_LHAND = 6
L_LFINGER = 7
L_LEXTRA =  12
L_LTOE = 13

L_RARMIK =  18
L_RARMFK =  19
L_RLEGIK =  20
L_RLEGFK =  21
L_RHAND = 22
L_RFINGER = 23
L_REXTRA =  28
L_RTOE = 29

L_FACE =   8
L_TWEAK =   9
L_HEAD =    10
L_CUSTOM = 16

L_HELP =    14
L_HELP2 =   15
L_DEF =     31


MhxLayers = [
    ((L_MAIN,       'Root', 'MhxRoot'),
     (L_SPINE ,     'Spine', 'MhxFKSpine')),
    ((L_HEAD,       'Head', 'MhxHead'),
     (L_FACE,       'Face', 'MhxFace')),
    ((L_TWEAK,      'Tweak', 'MhxTweak'),
     (L_CUSTOM,     'Custom', 'MhxCustom')),
    ('Left', 'Right'),
    ((L_LARMIK,     'IK Arm', 'MhxIKArm'),
     (L_RARMIK,     'IK Arm', 'MhxIKArm')),
    ((L_LARMFK,     'FK Arm', 'MhxFKArm'),
     (L_RARMFK,     'FK Arm', 'MhxFKArm')),
    ((L_LLEGIK,     'IK Leg', 'MhxIKLeg'),
     (L_RLEGIK,     'IK Leg', 'MhxIKLeg')),
    ((L_LLEGFK,     'FK Leg', 'MhxFKLeg'),
     (L_RLEGFK,     'FK Leg', 'MhxFKLeg')),
    ((L_LEXTRA,     'Extra', 'MhxExtra'),
     (L_REXTRA,     'Extra', 'MhxExtra')),
    ((L_LHAND,      'Hand', 'MhxHand'),
     (L_RHAND,      'Hand', 'MhxHand')),
    ((L_LFINGER,    'Fingers', 'MhxFingers'),
     (L_RFINGER,    'Fingers', 'MhxFingers')),
    ((L_LTOE,       'Toes', 'MhxToe'),
     (L_RTOE,       'Toes', 'MhxToe')),
]

OtherLayers = [
    ((L_SPINE,      'Spine', 'MhxFKSpine'),
     (L_HEAD,       'Head', 'MhxHead')),
    ((L_TWEAK,      'Tweak', 'MhxTweak'),
     (L_FACE,       'Face', 'MhxFace')),
    ('Left', 'Right'),
    ((L_LARMFK,     'Arm', 'MhxFKArm'),
     (L_RARMFK,     'Arm', 'MhxFKArm')),
    ((L_LLEGFK,     'Leg', 'MhxFKLeg'),
     (L_RLEGFK,     'Leg', 'MhxFKLeg')),
    ((L_LFINGER,    'Fingers', 'MhxFingers'),
     (L_RFINGER,    'Fingers', 'MhxFingers')),
    ((L_LTOE,       'Toes', 'MhxToe'),
     (L_RTOE,       'Toes', 'MhxToe')),
]


class DAZ_OT_McpEnableAllLayers(BvhOperator, IsArmature):
    bl_idname = "mcp.enable_all_layers"
    bl_label = "Enable all layers"
    bl_options = {'UNDO'}

    def run(self, context):
        rig = context.object
        for (left,right) in MhxLayers:
            if type(left) != str:
                for (n, name, prop) in [left,right]:
                    rig.data.layers[n] = True


class DAZ_OT_McpDisableAllLayers(BvhOperator, IsArmature):
    bl_idname = "mcp.disable_all_layers"
    bl_label = "Disable all layers"
    bl_options = {'UNDO'}

    def run(self, context):
        rig = context.object
        layers = 32*[False]
        pb = context.active_pose_bone
        if pb:
            for n in range(32):
                if pb.bone.layers[n]:
                    layers[n] = True
                    break
        else:
            layers[0] = True
        if rig:
            rig.data.layers = layers

#----------------------------------------------------------
#   Initialize
#----------------------------------------------------------

classes = [
    DAZ_OT_McpEnableAllLayers,
    DAZ_OT_McpDisableAllLayers,
]

def initialize():
    for cls in classes:
        bpy.utils.register_class(cls)


def uninitialize():
    for cls in classes:
        bpy.utils.unregister_class(cls)



