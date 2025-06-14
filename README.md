
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