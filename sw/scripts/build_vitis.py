import vitis
import os

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
VITIS_BUILD_DIR_PATH = os.path.join(ROOT_PATH, "..", "build")
os.makedirs(VITIS_BUILD_DIR_PATH, exist_ok=True)
EXPECTED_XSA_FILE_PATH = os.path.join(ROOT_PATH, "..", "..", "hw", "output", "zybo.xsa")
COMPONENT_NAME = "hello_world"
MAIN_SRC_PATH = os.path.join(ROOT_PATH, "src")
client = vitis.create_client()
client.set_workspace(path=VITIS_BUILD_DIR_PATH)
PLATFORM_NAME = "platform_baremetal"
platform = client.create_platform_component(
    name=PLATFORM_NAME,
    hw_design=EXPECTED_XSA_FILE_PATH,
    os="standalone",
    cpu="ps7_cortexa9_0",
)
# platform = client.get_platform_component(name=PLATFORM_NAME)
platform.build()

# This returns the platform xpfm path
platform_xpfm = client.find_platform_in_repos(PLATFORM_NAME)

comp = client.create_app_component(
    name=COMPONENT_NAME,
    platform=platform_xpfm,
    domain="mydomainname",
    template="hello_world",
)
# comp = client.get_component(name=COMPONENT_NAME)
# status = comp.import_files(
#     from_loc=MAIN_SRC_PATH,
#     files=["CMakeLists.txt", "UserConfig.cmake", "lscript.ld", "NOTUSED.cpp"],
#     dest_dir_in_cmp="src",
# )
comp.build()

# # Create system project
# sys_proj = client.create_sys_project(
#     name="system_project",
#     platform=platform_xpfm,
#     template="empty_accelerated_application",
# )
# # Add application component to the system project
# sys_proj_comp = sys_proj.add_component(name=COMPONENT_NAME)
# # Build system project
# sys_proj_comp.build()

vitis.dispose()
