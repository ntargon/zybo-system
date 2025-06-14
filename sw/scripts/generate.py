import vitis
import os
from pathlib import Path
import json


def is_under(base: Path, target: Path) -> bool:
    try:
        # baseとtargetを絶対パスに変換
        base = base.resolve()
        target = target.resolve()
        # targetがbaseの子孫かどうかを判定
        return base in target.parents or base == target
    except (FileNotFoundError, RuntimeError):
        return False


try:
    PROJECT_ROOT_PATH = (Path(os.path.dirname(__file__)) / ".." / "..").resolve()
    VITIS_ROOT_PATH = PROJECT_ROOT_PATH / "sw"
    VIVADO_ROOT_PATH = PROJECT_ROOT_PATH / "hw"
    EXPECTED_XSA_FILE_PATH = VIVADO_ROOT_PATH / "output" / "zybo.xsa"
    COMPONENT_NAME = "app"
    PLATFORM_NAME = "platform"
    DOMAIN_NAME = "mydomainname"

    client = vitis.create_client()

    client.set_workspace(path=str(VITIS_ROOT_PATH))
    ws = client.get_workspace()
    print(f"Workspace: {ws}")

    try:
        platform = client.get_component(name=PLATFORM_NAME)
    except Exception:
        platform = client.create_platform_component(
            name=PLATFORM_NAME,
            hw_design=str(EXPECTED_XSA_FILE_PATH),
            os="standalone",
            cpu="ps7_cortexa9_0",
        )
    print(f"Platform: {platform}")
    platform.build()

    # `VITIS_BUILD_DIR_PATH`以下のリポジトリからプラットフォームを検索
    platform_xpfm_list = client.find_platforms_in_repos(PLATFORM_NAME)
    platform_xpfm = None
    for p in platform_xpfm_list:
        p = Path(p).resolve()
        if is_under(VITIS_ROOT_PATH, p):
            platform_xpfm = str(p)
            break

    try:
        APP_VITIS_COMP_PATH = VITIS_ROOT_PATH / COMPONENT_NAME / "vitis-comp.json"
        APP_VITIS_COMP_TEMPLATE_PATH = (
            VITIS_ROOT_PATH / COMPONENT_NAME / "vitis-comp.template.json"
        )

        if not APP_VITIS_COMP_PATH.exists():
            with open(APP_VITIS_COMP_TEMPLATE_PATH, "r") as f:
                comp_template = json.load(f)

            comp_template["platform"] = str(platform_xpfm)

            with open(APP_VITIS_COMP_PATH, "w") as f:
                json.dump(comp_template, f, indent=2)

        APP_YAML_PATH = VITIS_ROOT_PATH / COMPONENT_NAME / "src" / "app.yaml"

        APP_TEMPLATE_YAML_PATH = (
            VITIS_ROOT_PATH / COMPONENT_NAME / "src" / "app.template.yaml"
        )

        if not APP_YAML_PATH.exists():
            with open(APP_TEMPLATE_YAML_PATH, "r") as f:
                app_template = f.read()

            with open(APP_YAML_PATH, "w") as f:
                f.write(app_template)

        comp = client.get_component(name=COMPONENT_NAME)
    except Exception:
        comp = client.create_app_component(
            name=COMPONENT_NAME,
            platform=platform_xpfm,
            domain=DOMAIN_NAME,
            template="hello_world",
        )
    print(f"Component: {comp}")
    comp.clean()
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
finally:
    vitis.dispose()
