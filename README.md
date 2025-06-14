
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
vitis -s ./scripts/generate.py
```

### 基本戦略

- clone後はgenerate.pyでコンポーネント作成
- platformはgitに登録しない
- appは登録する
- appのvitis-comp.jsonはテンプレートを用意しておき、環境に応じて、親パスを変更する。

## QEMU

C:\Xilinx\Vitis\2024.1\data\emulation\qemu_win\qemu\qemu-system-aarch64.exe -M xilinx-zynq-a9 -serial null -serial mon:stdio -device loader,addr=0xf8000008,data=0xDF0D,data-len=4 -device loader,addr=0xf8000140,data=0x00500801,data-len=4 -device loader,addr=0xf800012c,data=0x1ed044d,data-len=4 -device loader,addr=0xf8000108,data=0x0001e008,data-len=4 -device loader,addr=0xF800025C,data=0x00000005,data-len=4 -device loader,addr=0xF8000240,data=0x00000000,data-len=4 -nographic -kernel .\app\build\app.elf
