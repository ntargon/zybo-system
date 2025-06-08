# Vivadoプロジェクトを開く
open_project ./vivado_proj/zybo.xpr

# Block Designファイルを明示的に指定して開く（必要）
set bd_path "./vivado_proj/zybo.srcs/sources_1/bd/design_1/design_1.bd"
open_bd_design $bd_path

# ① Output Products の生成（必要！）
generate_target all [get_files $bd_path]

# # HDLラッパー生成（ラッパーがない場合のみ必要）
# make_wrapper -files [get_files $bd_path] -top

# コンパイル順を更新（安全のため）
update_compile_order -fileset sources_1

# ⑤ Bitstream の生成（`-include_bit` を使う場合は必要）
# Bitstream 生成が必要かどうかチェック
set run_state [get_property STATUS [get_runs impl_1]]

if { $run_state ne "write_bitstream Complete!" } {
    puts "INFO: Bitstream not yet generated. Launching write_bitstream..."
    launch_runs impl_1 -to_step write_bitstream -jobs 16
    wait_on_run impl_1
} else {
    puts "INFO: Bitstream already generated. Skipping write_bitstream step."
}

# .xsa を出力
set xsa_output_path "./output/zybo.xsa"
# write_hw_platform -fixed $xsa_output_path
write_hw_platform -fixed -include_bit $xsa_output_path