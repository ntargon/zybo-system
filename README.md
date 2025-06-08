
## vivado

git clone後、以下を実行。

```cmd
cd hw
vivado -mode batch -source ./scripts/create_vivado_project.tcl
vivado -mode batch -source ./scripts/export_xsa.tcl
```

## vitis

mada

```cmd
cd sw
vitis -s ./scripts/build_vitis.py
```