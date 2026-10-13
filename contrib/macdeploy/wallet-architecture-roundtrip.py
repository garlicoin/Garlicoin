#!/usr/bin/env python3
"""Throwaway regtest BDB wallet interchange: Intel -> ARM64 -> Intel."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('mode', choices=['initialize', 'update', 'verify'])
parser.add_argument('--bin-dir', required=True, type=Path)
parser.add_argument('--fixture', required=True, type=Path)
args = parser.parse_args()
binaries, fixture = args.bin_dir.resolve(), args.fixture.resolve()
fixture.mkdir(parents=True, exist_ok=True)
metadata_file = fixture / 'public-checks.json'
metadata = {} if args.mode == 'initialize' else json.loads(metadata_file.read_text())

with tempfile.TemporaryDirectory(prefix='grlc-wallet-interchange-') as temporary:
    datadir = Path(temporary)
    if args.mode != 'initialize':
        (datadir / 'regtest').mkdir()
        shutil.copy2(fixture / 'wallet.dat', datadir / 'regtest/wallet.dat')
    options = ['-regtest', f'-datadir={datadir}']
    process = subprocess.Popen([str(binaries / 'garlicoind'), *options, '-server=1',
                                '-listen=0', '-connect=0', '-dnsseed=0', '-discover=0', '-keypool=5'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    def rpc(method, *arguments):
        result = subprocess.run([str(binaries / 'garlicoin-cli'), *options, method, *arguments],
                                capture_output=True, text=True, timeout=15)
        if result.returncode:
            raise RuntimeError(f'RPC {method} failed: {result.stderr}')
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return result.stdout.strip()
    try:
        for _ in range(120):
            if process.poll() is not None:
                raise RuntimeError('Node exited while opening test wallet')
            try:
                rpc('getwalletinfo')
                break
            except RuntimeError:
                time.sleep(0.5)
        else:
            raise RuntimeError('Wallet RPC readiness timeout')
        version = rpc('getwalletinfo')['walletversion']
        if args.mode == 'initialize':
            metadata['walletversion'] = version
            metadata['message'] = 'Garlicoin BDB 4.8 architecture interchange'
            metadata['intel_address'] = rpc('getnewaddress', 'intel-fixture', 'legacy')
            metadata['intel_signature'] = rpc('signmessage', metadata['intel_address'], metadata['message'])
        assert version == metadata['walletversion']
        for architecture in ['intel', 'arm64']:
            if architecture + '_address' not in metadata:
                continue
            address = metadata[architecture + '_address']
            assert rpc('validateaddress', address)['ismine']
            assert rpc('verifymessage', address, metadata[architecture + '_signature'], metadata['message']) is True
            new_signature = rpc('signmessage', address, metadata['message'])
            assert rpc('verifymessage', address, new_signature, metadata['message']) is True
        if args.mode == 'update':
            metadata['arm64_address'] = rpc('getnewaddress', 'arm64-fixture', 'legacy')
            metadata['arm64_signature'] = rpc('signmessage', metadata['arm64_address'], metadata['message'])
        rpc('stop')
        assert process.wait(timeout=30) == 0
        if args.mode != 'verify':
            wallets = list(datadir.rglob('wallet.dat'))
            assert len(wallets) == 1
            shutil.copy2(wallets[0], fixture / 'wallet.dat')
            metadata_file.write_text(json.dumps(metadata, indent=2) + '\n')
        else:
            assert 'arm64_address' in metadata
        print(f'PASS: {args.mode}; wallet version, ownership and private-key message signing preserved')
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
