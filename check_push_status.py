#!/usr/bin/env python3
"""
Script pour vérifier l'état du push Git
"""

import subprocess
import sys
import time

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except:
        return False, "", ""

def main():
    print("=" * 70)
    print("🔍 VÉRIFICATION DE L'ÉTAT DU PUSH GIT")
    print("=" * 70)
    print()
    
    # Vérifier si un push est en cours
    success, output, _ = run_command("ps aux | grep -i 'git push' | grep -v grep")
    if success and output:
        print("⚠️  Un processus git push est en cours...")
        print(f"   {output}")
        print()
        print("💡 Le push peut prendre plusieurs minutes pour 937 MB")
        print("   Patientez ou annulez avec: pkill -f 'git push'")
    else:
        print("✅ Aucun push en cours")
        print()
        print("💡 Pour lancer le push:")
        print("   git push origin main --force")
    
    print()
    print("📊 État du dépôt local:")
    success, output, _ = run_command("git log --oneline -1")
    if success:
        print(f"   Dernier commit: {output}")
    
    success, output, _ = run_command("git count-objects -vH")
    if success:
        for line in output.split('\n'):
            if 'size-pack' in line:
                print(f"   Taille: {line.split(':')[1].strip()}")
    
    print()
    print("🌐 Vérification du dépôt GitHub...")
    success, output, _ = run_command("git ls-remote origin main")
    if success and output:
        print("   ✅ Le dépôt GitHub existe")
        remote_commit = output.split()[0]
        local_commit = subprocess.run("git rev-parse HEAD", shell=True, capture_output=True, text=True).stdout.strip()
        if remote_commit == local_commit:
            print("   ✅ Le push a réussi! Les commits correspondent.")
        else:
            print(f"   ⚠️  Les commits ne correspondent pas encore")
            print(f"      Local:  {local_commit[:8]}...")
            print(f"      Remote: {remote_commit[:8]}...")
    else:
        print("   ⚠️  Impossible de vérifier le dépôt GitHub")
        print("      (peut-être que le dépôt est vide ou le push est en cours)")

if __name__ == '__main__':
    main()

