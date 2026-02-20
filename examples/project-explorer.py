#!/usr/bin/env python3
# coding: utf-8
"""
Assimilate Example - Project Browser
"""

from __future__ import absolute_import
import os
import sys
from datetime import datetime
from pathlib import Path

# Import the generated library
try:
    from assimilate_client import *
    from assimilate_client.api import *
    from assimilate_client.models import *
    from assimilate_client.rest import *
except ImportError as e:
    print(f"Error importing assimilate_client: {e}")
    print("Make sure the library is in your PYTHONPATH:")
    sys.exit(1)


def safe_get_attr(obj, attr_name, default=None):
    """Helper to safely retrieve attributes, works with dicts and objects"""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(attr_name, default)
    return getattr(obj, attr_name, default)


class AssimilateProjectExplorer:
    def __init__(self, host="http://localhost:8080/APIV2"):
        # Swagger configuration
        self.config = Configuration()
        self.config.host = host
        self.config.debug = False
        
        # API Client
        self.api_client = ApiClient(self.config)
        
        # API endpoints (swagger generated)
        self.system_api = SystemApi(self.api_client)
        self.projects_api = ProjectsApi(self.api_client)
        self.application_api = ApplicationApi(self.api_client)
        
        # Status tracking
        self.current_project = None
        self.current_group = None
        self.current_construct = None

    # ============================================================
    # STEP 1: Retrieve system information
    # ============================================================
    def get_system_info(self):
        """Retrieve system settings"""
        print("🔧 Retrieving system info...")
        try:
            system = self.system_api.get_system_properties()
            print(f"   System name: {system.system_name}")
            print(f"   Software version: {system.version} "
                  f"(build {system.build})")
            return system
        except ApiException as e:
            if e.body:
                error_dict = json.loads(e.body.decode('utf-8'))
                print(f"❌ API Error: {json.dumps(error_dict, indent=4)}")
            raise

    # ============================================================
    # STEP 2: Project management
    # ============================================================
    def list_projects(self):
        """List all available projects"""
        print("\n📁 Retrieving projects...")
        try:
            projects = self.projects_api.get_projects().projects
            print(type(projects))
            for proj in projects:
                print(f"   - {proj.name} (last modified: {proj.modified})")
            return projects
        except ApiException as e:
            if e.body:
                error_dict = json.loads(e.body.decode('utf-8'))
                print(f"❌ Error retrieving projects: {json.dumps(error_dict, indent=4)}")
            return []
    
    def enter_project(self, project_name):
        """Open a specific project"""
        try:
            self.application_api.do_application_project_exit()
        except ApiException as e:
            e=0 # Ignore errors when leaving project (may already be in a project)
        

        print(f"\n🎬 Opening project '{project_name}'...")
        try:
            # Swagger uses 'do_' prefix for POST operations
            self.application_api.do_application_project_enter(project_name)
            
            current = self.projects_api.get_projects_current()
            print(f"   ✅ Current project: {current.name}")
            return current
        except ApiException as e:
            if e.body:
                error_dict = json.loads(e.body.decode('utf-8'))
                print(f"❌ Error opening project: {json.dumps(error_dict, indent=4)}")

            raise

    # ============================================================
    # STEP 3: Explore groups and Timelines
    # ============================================================
    def get_groups(self, detailed=False):
        """Retrieve all groups from the current project"""
        print("\n📂 Retrieving groups...")
        try:
            level = "ALL" if detailed else ""
            groups = self.projects_api.get_groups(level = level).groups
            print(f"   {len(groups)} group(s) found:")
            for group in groups:
                name = group.name
                status = " (active)" if group.active else ""
                print(f"   - {name}{status}")
                if detailed:
                    constructs = group.constructs
                    if constructs:
                        print(f"     └─ {len(constructs)} timeline(s)")
            return groups
        except ApiException as e:
            error_dict = json.loads(e.body.decode('utf-8'))
            print(f"❌ Error retrieving groups: {json.dumps(error_dict, indent=4)}")
            return []
    
    def select_group(self, group_uuid):
        """Activate a specific group"""
        print(f"\n👉 Selecting group...")
        try:
            # Swagger: post_group to select
            result = self.projects_api.select_group(group_uuid, level="ALL")
            self.current_group = result
            
            name = safe_get_attr(result, 'name', 'Unknown')
            print(f"   ✅ Group '{name}' is now active")
            return result
        except ApiException as e:
            print(f"❌ Error selecting group: {e.reason}")
            raise

    # ============================================================
    # STEP 4: Collect shots and generate thumbnails
    # ============================================================
    def get_current_construct(self):
        """Retrieve the active timeline (construct)"""
        print("\n🎞️  Retrieving active timeline...")
        try:
            construct = self.projects_api.get_constructs_current(level="ALL")
            self.current_construct = construct
            
            name = safe_get_attr(construct, 'name', 'Unknown')
            resolution = safe_get_attr(construct, 'resolution', {})
            fps = safe_get_attr(construct, 'fps', 0)
            
            print(f"   Timeline: {name}")
            if resolution:
                w = safe_get_attr(resolution, 'w', '?')
                h = safe_get_attr(resolution, 'h', '?')
                print(f"   Resolution: {w}x{h}")
            print(f"   FPS: {fps}")
            return construct
        except ApiException as e:
            print(f"❌ Error retrieving construct: {e.reason}")
            raise
    
    def get_all_shots(self):
        """Retrieve all shots from the current timeline"""
        print("\n🎬 Collecting shots...")
        try:
            construct = self.projects_api.get_constructs_current(level="ALL")
            all_shots = []
            
            slots = safe_get_attr(construct, 'slots', [])
            for slot_idx, slot in enumerate(slots):
                slot_shots = safe_get_attr(slot, 'shots', [])
                for version_idx, shot in enumerate(slot_shots):
                    shot_info = {
                        'uuid': shot.uuid,
                        'name': shot.name,
                        'slot_idx': slot_idx,
                        'version_idx': version_idx,
                        'file': safe_get_attr(shot, 'file', 'N/A'),
                        'length': safe_get_attr(shot, 'length', 0),
                        'timecode': safe_get_attr(shot, 'timecode', '00:00:00:00')
                    }
                    all_shots.append(shot_info)
                    print(f"   Slot {slot_idx}, Version {version_idx}: {shot_info['name']} "
                          f"({shot_info['length']} frames)")
            
            print(f"   Total: {len(all_shots)} shot(s) found")
            return all_shots
            
        except ApiException as e:
            print(f"❌ Error collecting shots: {e.reason}")
            return []

    def generate_thumbnail(self, shot_uuid, frame=0, output_path=None):
        """Generate a thumbnail (snapshot) of a specific shot"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/tmp/thumbnail_{shot_uuid[:8]}_{timestamp}.jpg"
        
        try:
            # Use ImageSnapshot model
            snapshot = ImageSnapshot(
                uuid=shot_uuid,
                frame=frame,
                proxy=True,
                #file=output_path
                # Note: The API support direct file output, if 'file' is not pressent in ImageSnapShot we will handle the binary response ourselves
            )
            
            # Swagger API call - returns JPEG binary
            response = self.application_api.do_application_render_snapshot(
                body=snapshot,
                _preload_content=False  # Important: we want the raw response
            )
            
            # Save the image
            if response.headers.get('Content-Type') == 'image/jpeg':
                if hasattr(response, 'data'):
                    with open(output_path, 'wb') as f:
                        f.write(response.data)
                        
            return output_path
        except ApiException as e:
            print(f"   ⚠️  Thumbnail failed: {e.reason}")
            return None

    # ============================================================
    # STEP 5: Render Queue management
    # ============================================================
    def get_render_queue(self):
        """Retrieve the current render queue"""
        print("\n⏳ Render queue status...")
        try:
            queue = self.application_api.get_application_render_queue()
            
            if not queue:
                print("   Queue is empty")
                return []
            
            for item in queue:
                name = safe_get_attr(item, 'name', 'Unknown')
                status = safe_get_attr(item, 'status', 'unknown')
                
                status_icon = {
                    "Idle": "⚪",
                    "waiting": "⏸️",
                    "processing": "🔄",
                    "finished": "✅",
                    "error": "❌"
                }.get(status, "❓")
                
                frames_done = safe_get_attr(item, 'frames_done', 0)
                frames_total = safe_get_attr(item, 'frames_total', 0)
                
                print(f"   {status_icon} {name}: {status} "
                      f"({frames_done}/{frames_total} frames)")
            return queue
            
        except ApiException as e:
            print(f"❌ Error retrieving queue: {e.reason}")
            return []
    
    def add_output_to_queue(self, output_uuid, auto_start=False):
        """Add an output node to the render queue"""
        print(f"\n🚀 Adding output to render queue...")
        try:
            if auto_start:
                # Use DeleteMediaData model for the body
                delete_data = DeleteMediaData(delete_existing_media=False)
                result = self.application_api.post_application_render_queue_item(
                    output_uuid, 
                    delete_existing_media=False
                )
                name = safe_get_attr(result, 'name', 'Unknown')
                print(f"   ✅ Render started for: {name}")
            else:
                result = self.application_api.put_application_render_queue_item(output_uuid)
                name = safe_get_attr(result, 'name', 'Unknown')
                print(f"   ✅ Added to queue: {name}")
            
            return result
            
        except ApiException as e:
            print(f"❌ Error adding: {e.reason}")
            raise
    
    def start_render(self, delete_existing=False):
        """Start the render queue"""
        print("\n▶️  Starting render queue...")
        try:
            delete_data = DeleteMediaData(delete_existing_media=delete_existing)
            self.application_api.post_application_render_start(
                delete_existing_media=delete_existing
            )
            print("   ✅ Render queue started!")
        except ApiException as e:
            print(f"❌ Error starting: {e.reason}")
            raise

    # ============================================================
    # STEP 6: Player controls (for review)
    # ============================================================
    def enter_player(self, construct_uuid=None):
        """Enter player mode for review"""
        try:
            if construct_uuid:
                self.application_api.do_application_player_enter_timeline(construct_uuid)
            else:
                self.application_api.do_application_player_enter_timeline_current()
            print("\n▶️  Player mode activated")
        except ApiException as e:
            print(f"❌ Error opening player: {e.reason}")
            raise
    
    def set_playback_mode(self, mode="PAUSE", frame=None, loop="LOOP"):
        """Configure playback settings"""
        try:
            # Use PlaymodeData model
            playmode = PlaymodeData(
                mode=mode,
                loop=loop,
                audio="ON",
                speed=1,
                range=False
            )
            
            self.application_api.set_application_player_playmode(body=playmode)
            print(f"   Playback: {mode}, Loop: {loop}")
        except ApiException as e:
            print(f"❌ Error setting playback: {e.reason}")
            raise

    # ============================================================
    # MAIN WORKFLOW: Browse through Project elements
    # ============================================================
    def browse_project(self, project_name, target_group_name=None):
        """
        Browse through the elements of an Assimilate project using the REST API
        
        Args:
            project_name: Name of the project
            target_group_name: Specific group (None = last group)
        """
        print("=" * 60)
        print("🎬 ASSIMILATE PROJECT BROWSER - REST API")
        print("=" * 60)
        
        try:
            # 1. System check
            self.get_system_info()
            
            # 2. Open project
            self.enter_project(project_name)
            
            # 3. Explore and select groups
            groups = self.get_groups(detailed=True)
            
            if not groups:
                print("❌ No groups found!")
                return False
            
            # Select target group
            target_group = None
            if target_group_name:
                target_group = next((
                    g for g in groups 
                    if g.name == target_group_name
                ), None)
            else:
                target_group = groups[-1]
            
            if not target_group:
                print(f"❌ Group '{target_group_name}' not found!")
                return False
            
            self.select_group(target_group.uuid)
            
            # 4. Explore timeline
            construct = self.get_current_construct()
            
            # 5. Collect shots
            shots = self.get_all_shots()
            
            if not shots:
                print("⚠️  No shots found in this timeline!")
                return False
            
            # 6. Generate thumbnails
            print("\n📸 Generating thumbnails...")
            thumbnails = []
            for i, shot in enumerate(shots[:5]):
                print(f"   Generating thumbnail for: {shot['name']}...")
                thumb_path = f"/tmp/project_thumb_{i}_{shot['uuid'][:8]}.jpg"
                result = self.generate_thumbnail(shot['uuid'], frame=0, output_path=thumb_path)
                if result:
                    thumbnails.append(result)
                    print(f"      ✅ Saved: {thumb_path}")
            
            # 7. Check render queue
            self.get_render_queue()
            
            # 8. Open player
            print("\n👁️  Opening player for review...")
            self.enter_player()
            self.set_playback_mode(mode="PLAY_FRW", loop="LOOP")
            
            # Summary
            group_name = safe_get_attr(target_group, 'name', 'Unknown')
            print("\n" + "=" * 60)
            print("✅ PROJECT EXPLORER COMPLETED")
            print(f"   Project: {project_name}")
            print(f"   Group: {group_name}")
            print(f"   Shots processed: {len(shots)}")
            print(f"   Thumbnails: {len(thumbnails)} generated")
            print("=" * 60)
            
            return True
            
        except ApiException as e:
            print(f"\n❌ API Error in workflow: {e.reason}")
            print(f"   Status code: {e.status}")
            if e.body:
                print(f"   Details: {e.body}")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return False


# ============================================================
# USAGE EXAMPLE
# ============================================================
if __name__ == "__main__":
    explorer = AssimilateProjectExplorer()
    
    PROJECT_NAME = "Project"  # <-- Change this!
    
    success = explorer.browse_project(
        project_name=PROJECT_NAME,
        target_group_name=None
    )
    
    if not success:
        print("\n--- Debug info ---")
        try:
            explorer.get_system_info()
            projects = explorer.list_projects()
            if projects:
                names = [p.name for p in projects]
                print(f"\nAvailable projects: {names}")
        except Exception as e:
            print(f"Debug failed: {e}")
    
    sys.exit(0 if success else 1)