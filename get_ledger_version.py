"""
*******************************************************************************
*   Ledger Blue
*   (c) 2016 Ledger
*
*	Modified by muXxer 
*
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
*  Unless required by applicable law or agreed to in writing, software
*  distributed under the License is distributed on an "AS IS" BASIS,
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*  limitations under the License.
********************************************************************************
"""

import argparse

def get_argparser():
	parser = argparse.ArgumentParser(description="Checks the minimum version of the ledger device.")
	parser.add_argument("--targetId", help="The device's target ID (default is Ledger Blue)", type=auto_int)
	parser.add_argument("--rootPrivateKey", help="""The Signer private key used to establish a Secure Channel (otherwise
a random one will be generated)""")
	parser.add_argument("--apdu", help="Display APDU log", action='store_true')
	parser.add_argument("--deployLegacy", help="Use legacy deployment API", action='store_true')
	parser.add_argument("--offline", help="Request to only output application load APDUs", action="store_true")
	parser.add_argument("--minVersionOS", help="Minimum version of the ledger OS", type=auto_int)
	parser.add_argument("--minVersionMCU", help="Minimum version of the MCU firmware", type=auto_int)
	return parser

def auto_int(x):
	return int(x, 0)

if __name__ == '__main__':
	from ledgerblue.ecWrapper import PrivateKey
	from ledgerblue.comm import getDongle
	from ledgerblue.hexLoader import HexLoader
	from ledgerblue.hexLoader import *
	from ledgerblue.deployed import getDeployedSecretV1, getDeployedSecretV2
	import binascii, sys

	args = get_argparser().parse_args()

	if args.targetId == None:
		args.targetId = 0x31000002
	if args.rootPrivateKey == None:
		privateKey = PrivateKey()
		publicKey = binascii.hexlify(privateKey.pubkey.serialize(compressed=False))
		print("Generated random root public key : %s" % publicKey)
		args.rootPrivateKey = privateKey.serialize()

	dongle = None
	secret = None
	if not args.offline:
		dongle = getDongle(args.apdu)

		if args.deployLegacy:
			secret = getDeployedSecretV1(dongle, bytearray.fromhex(args.rootPrivateKey), args.targetId)
		else:
			secret = getDeployedSecretV2(dongle, bytearray.fromhex(args.rootPrivateKey), args.targetId)

	loader = HexLoader(card=dongle, cla=0xe0, secure=not(args.offline), mutauth_result=secret)
	version_dict = loader.getVersion()

	print("Ledger OS version: %s, Ledger MCU version: %s" % (version_dict['osVersion'], version_dict['mcuVersion']))

	if args.minVersionOS != None:
		version_os_act = 0x00000000
		parts_count    = 0
		for version_part in version_dict['osVersion'].split('.'):
			version_os_act <<= 8
			version_os_act |= (int(version_part) & 0xFF)
			parts_count += 1
		
		while parts_count < 4:
			version_os_act <<= 8
			parts_count += 1
		
		if version_os_act < args.minVersionOS:
			print("ERROR: Ledger OS version too old! version_os_act: 0x%08X, minVersionOS: 0x%08X" % (version_os_act, args.minVersionOS))
			sys.exit(1)
	
	if args.minVersionMCU != None:
		version_mcu_act = 0x00000000
		parts_count    	= 0
		for version_part in version_dict['mcuVersion'].split('.'):
			version_mcu_act <<= 8
			version_mcu_act |= (int(version_part) & 0xFF)
			parts_count += 1
		
		while parts_count < 4:
			version_mcu_act <<= 8
			parts_count += 1
		
		if version_mcu_act < args.minVersionMCU:
			print("ERROR: Ledger MCU version too old! version_mcu_act: 0x%08X, minVersionMCU: 0x%08X" % (version_mcu_act, args.minVersionMCU))
			sys.exit(2)
