#!/usr/bin/env python3
"""Isolated 0.18.x RPC, BDB wallet and offline transaction smoke test."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

root = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--node-binary', type=Path, default=root / 'src/garlicoind')
daemon = parser.parse_args().node_binary.resolve()
cli = root / 'src/garlicoin-cli'
tx = root / 'src/garlicoin-tx'

with tempfile.TemporaryDirectory(prefix='garlicoin-arm64-') as temporary:
    datadir = Path(temporary)
    base = ['-regtest', f'-datadir={datadir}']
    process = None

    def rpc(method, *arguments):
        args = [json.dumps(x) if not isinstance(x, str) else x for x in arguments]
        result = subprocess.run([str(cli), *base, method, *args], capture_output=True, text=True, timeout=15)
        if result.returncode:
            raise RuntimeError(f'RPC {method} failed: {result.stderr}')
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return result.stdout.strip()

    def start():
        global process
        process = subprocess.Popen([str(daemon), *base, '-server=1', '-listen=0', '-connect=0',
                                    '-dnsseed=0', '-discover=0', '-keypool=5'],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(120):
            if process.poll() is not None:
                raise RuntimeError('daemon exited before RPC readiness')
            try:
                rpc('getblockchaininfo')
                return
            except RuntimeError:
                time.sleep(0.5)
        raise RuntimeError('RPC readiness timeout')

    def stop():
        rpc('stop')
        assert process.wait(timeout=30) == 0

    try:
        start()  # This baseline creates the default BDB wallet at first startup.
        assert rpc('getblockchaininfo')['chain'] == 'regtest'
        info = rpc('getwalletinfo')
        wallet_version = info['walletversion']
        address = rpc('getnewaddress', 'arm64-smoke', 'legacy')
        assert rpc('validateaddress', address)['ismine']
        message = 'Garlicoin Apple Silicon wallet smoke'
        signature = rpc('signmessage', address, message)
        assert rpc('verifymessage', address, signature, message) is True
        destination = rpc('getnewaddress', 'offline-destination', 'legacy')
        # Synthetic prevout: exercise signing entirely offline; never broadcast.
        txid = '01' * 32
        previous = [{'txid': txid, 'vout': 0,
                     'scriptPubKey': rpc('validateaddress', address)['scriptPubKey'], 'amount': 1}]
        unsigned = rpc('createrawtransaction', [{'txid': txid, 'vout': 0}], {destination: 0.9})
        signed = rpc('signrawtransaction', unsigned, previous)
        assert signed['complete'] is True
        decoded = rpc('decoderawtransaction', signed['hex'])
        assert decoded['vin'][0]['scriptSig']['hex']
        # Test the standalone transaction signer using throwaway keys in a private temp file.
        keys = datadir / 'keys.json'
        prev = datadir / 'prev.json'
        keys.write_text(json.dumps([rpc('dumpprivkey', address)]))
        keys.chmod(0o600)
        prev.write_text(json.dumps(previous))
        offline = subprocess.check_output([str(tx), '-regtest', unsigned,
                         f'load=privatekeys:{keys}', f'load=prevtxs:{prev}', 'sign=ALL'], text=True, timeout=15).strip()
        keys.unlink()
        assert rpc('decoderawtransaction', offline)['vin'][0]['scriptSig']['hex']
        backup = datadir / 'backup.dat'
        rpc('backupwallet', str(backup))
        assert backup.is_file() and backup.stat().st_size > 0
        stop()
        assert list(datadir.rglob('wallet.dat'))
        start()
        assert rpc('getwalletinfo')['walletversion'] == wallet_version
        assert rpc('validateaddress', address)['ismine']
        assert rpc('verifymessage', address, signature, message) is True
        signature2 = rpc('signmessage', address, message)
        assert rpc('verifymessage', address, signature2, message) is True
        stop()
        print('PASS: RPC, BDB wallet creation/read/restart, addresses, message signing, RPC and offline TX signing, clean shutdown')
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
