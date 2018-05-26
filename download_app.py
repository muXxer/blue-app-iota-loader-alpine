import os, sys

python_cmd  = "python3"
target_id   = 0x31100003
file_name   = "/root/iota-ledger/download/app.hex"
data_size   = 0x00000040    # `cat debug/app.map |grep _nvram_data_size | tr -s ' ' | cut -f2 -d' '`
icon_hex    = "0100000000ffffff001000800008004002000000050800220208000100840200100081020400200000"  # python $(BOLOS_SDK)/icon.py $(ICONNAME) hexbitmaponly
script_cmd  = "-m ledgerblue.loadApp --path \"44'/4218'\" --path \"44'/01'\" --appFlags 0x00 --tlv --targetId 0x%08X --delete --fileName %s --appName \"IOTA\" --appVersion 0.0.1 --dataSize 0x%08X --icon %s" % (target_id, file_name, data_size, icon_hex)

exit_code = 1
try:
    exit_code = os.system("%s %s" % (python_cmd, script_cmd))
    if exit_code != 0:      # muXxer: Otherwise it returned 256, which was recognized as 0 in the shell
        exit_code = 1
except:
    pass
sys.exit(exit_code)
