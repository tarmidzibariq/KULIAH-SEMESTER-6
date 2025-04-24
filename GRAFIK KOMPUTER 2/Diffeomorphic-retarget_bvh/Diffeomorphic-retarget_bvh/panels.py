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
from bpy.props import BoolProperty
from . import utils
from .buildnumber import BUILD

#----------------------------------------------------------
#   Panels
#----------------------------------------------------------

class MCP_PT_Base:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BVH"
    bl_options = {'DEFAULT_CLOSED'}

#-------------------------------------------------------------
#   Main panel
#-------------------------------------------------------------

class MCP_PT_Main(MCP_PT_Base, bpy.types.Panel):
    bl_label = "Retarget BVH (version 2.2.%04d)" % BUILD
    bl_options = set()

    def draw(self, context):
        self.layout.operator("mcp.load_and_retarget")
        self.layout.separator()
        self.layout.operator("mcp.load_bvh")


class MCP_PT_Debug(MCP_PT_Base, bpy.types.Panel):
    bl_parent_id = "MCP_PT_Main"
    bl_label = "Debug"

    def draw(self, context):
        self.layout.operator("mcp.retarget_selected_to_active")
        self.layout.operator("mcp.rename_active_to_selected")
        self.layout.operator("mcp.load_and_rename_bvh")
        self.layout.operator("mcp.retarget_renamed_to_active")

#-------------------------------------------------------------
#   Options panel
#-------------------------------------------------------------

class MCP_PT_Options(MCP_PT_Base, bpy.types.Panel):
    bl_parent_id = "MCP_PT_Main"
    bl_label = "Options"

    def draw(self, context):
        scn = context.scene
        self.layout.prop(scn, "McpVerbose")
        self.layout.prop(scn, "McpIncludeFingers")
        self.layout.prop(scn, "McpUseLimits")
        self.layout.prop(scn, "McpClearLocks")

#-------------------------------------------------------------
#   Edit panel
#-------------------------------------------------------------

class MCP_PT_Edit(MCP_PT_Base, bpy.types.Panel, utils.IsArmature):
    bl_label = "Edit Actions"

    def draw(self, context):
        pass


class MCP_PT_GlobalEdit(MCP_PT_Base, bpy.types.Panel):
    bl_parent_id = "MCP_PT_Edit"
    bl_label = "Global Edit"

    def draw(self, context):
        self.layout.operator("mcp.shift_animation")
        self.layout.operator("mcp.center_animation")
        #layout.operator("mcp.limbs_bend_positive")
        self.layout.operator("mcp.fixate_bone")
        self.layout.operator("mcp.simplify_fcurves")
        self.layout.operator("mcp.timescale_fcurves")


class MCP_PT_LocalEdit(MCP_PT_Base, bpy.types.Panel):
    bl_parent_id = "MCP_PT_Edit"
    bl_label = "Local Edit"

    def draw(self, context):
        self.layout.operator("mcp.start_edit")
        self.layout.operator("mcp.undo_edit")

        row = self.layout.row()
        op = row.operator("mcp.insert_key", text="Loc")
        op.loc = True
        op.rot = False
        op.delete = False
        op = row.operator("mcp.insert_key", text="Rot")
        op.loc = False
        op.rot = True
        op.delete = False
        row = self.layout.row()
        op = row.operator("mcp.insert_key", text="LocRot")
        op.loc = True
        op.rot = True
        op.delete = False
        op = row.operator("mcp.insert_key", text="Delete")
        op.loc = True
        op.rot = True
        op.delete = True

        row = self.layout.row()
        op = row.operator("mcp.move_to_marker", text="|<")
        op.left = True
        op.last = True
        op = row.operator("mcp.move_to_marker", text="<")
        op.left = True
        op.last = False
        op = row.operator("mcp.move_to_marker", text=">")
        op.left = False
        op.last = False
        op = row.operator("mcp.move_to_marker", text=">|")
        op.left = False
        op.last = True

        self.layout.operator("mcp.confirm_edit")
        self.layout.separator()
        self.layout.operator("mcp.clear_temp_props")


class MCP_PT_LoopRepeat(MCP_PT_Base, bpy.types.Panel):
    bl_parent_id = "MCP_PT_Edit"
    bl_label = "Loop And Repeat"

    def draw(self, context):
        self.layout.operator("mcp.loop_fcurves")
        self.layout.operator("mcp.repeat_fcurves")
        self.layout.operator("mcp.stitch_actions")

#-------------------------------------------------------------
#    Source rigs panel
#-------------------------------------------------------------

class MCP_PT_SourceRigs(MCP_PT_Base, bpy.types.Panel, utils.IsArmature):
    bl_label = "Source Armature"

    def draw(self, context):
        from .source import isSourceInited
        scn = context.scene
        if not isSourceInited(scn):
            self.layout.operator("mcp.init_known_rigs")
            return
        self.layout.operator("mcp.init_known_rigs", text="Reinit Known Rigs")
        self.layout.prop(scn, "McpSourceRig")
        self.layout.prop(scn, "McpSourceTPose")
        self.layout.prop(scn, "McpIncludeFingers")
        self.layout.separator()
        self.layout.operator("mcp.identify_source_rig")
        self.layout.operator("mcp.verify_source_rig")
        self.layout.operator("mcp.list_source_rig")
        self.layout.operator("mcp.put_in_src_t_pose")

#-------------------------------------------------------------
#    Target rigs panel
#-------------------------------------------------------------

class MCP_PT_TargetRigs(MCP_PT_Base, bpy.types.Panel, utils.IsArmature):
    bl_label = "Target Armature"

    def draw(self, context):
        from .target import isTargetInited
        rig = context.object
        scn = context.scene
        if not isTargetInited(scn):
            self.layout.operator("mcp.init_known_rigs")
            return
        self.layout.operator("mcp.init_known_rigs", text="Reinit Known Rigs")
        self.layout.separator()
        self.layout.prop(scn, "McpTargetRig")
        self.layout.prop(scn, "McpTargetTPose")
        self.layout.prop(scn, "McpIncludeFingers")
        self.layout.prop(rig, "McpReverseHip")
        self.layout.separator()
        self.layout.operator("mcp.identify_target_rig")
        self.layout.operator("mcp.verify_target_rig")
        self.layout.operator("mcp.list_target_rig")
        self.layout.operator("mcp.put_in_trg_t_pose")

#-------------------------------------------------------------
#   T-pose panel
#-------------------------------------------------------------

class MCP_PT_TPose(MCP_PT_Base, bpy.types.Panel, utils.IsArmature):
    bl_label = "T-Pose"

    def draw(self, context):
        scn = context.scene
        self.layout.prop(scn, "McpSourceTPose", text="Source T-Pose")
        self.layout.prop(scn, "McpTargetTPose", text="Target T-Pose")
        self.layout.prop(scn, "McpIncludeFingers")
        self.layout.operator("mcp.put_in_src_t_pose")
        self.layout.operator("mcp.put_in_trg_t_pose")
        self.layout.separator()
        #self.layout.operator("mcp.define_t_pose")
        #self.layout.operator("mcp.undefine_t_pose")
        self.layout.operator("mcp.load_t_pose")
        self.layout.operator("mcp.save_t_pose")
        self.layout.operator("mcp.rest_current_pose")

#-------------------------------------------------------------
#   Action panel
#-------------------------------------------------------------

class MCP_PT_Actions(MCP_PT_Base, bpy.types.Panel, utils.IsArmature):
    bl_label = "Actions"

    def draw(self, context):
        self.layout.operator("mcp.set_current_action")
        self.layout.operator("mcp.set_fake_user")
        self.layout.operator("mcp.set_all_fake_user")
        self.layout.operator("mcp.delete_action")
        self.layout.operator("mcp.delete_all_actions")
        self.layout.operator("mcp.delete_hash")

#----------------------------------------------------------
#   Initialize
#----------------------------------------------------------

classes = [
    MCP_PT_Main,
    MCP_PT_Debug,
    MCP_PT_Options,
    MCP_PT_Edit,
    MCP_PT_GlobalEdit,
    MCP_PT_LocalEdit,
    MCP_PT_LoopRepeat,
    MCP_PT_SourceRigs,
    MCP_PT_TargetRigs,
    MCP_PT_TPose,
    MCP_PT_Actions,

    utils.ErrorOperator,
    utils.MessageOperator
]

def initialize():
    bpy.types.Scene.McpVerbose = BoolProperty(
        name="Verbose",
        description="Verbose mode for debugging",
        default=False)

    for cls in classes:
        bpy.utils.register_class(cls)


def uninitialize():

    for cls in classes:
        bpy.utils.unregister_class(cls)