#!/usr/bin/env bash
set -euo pipefail

# Day 011 – Network Tuning: MTU, IRQ Affinity & Backlog
# Minimal helper to capture current network-related settings.

echo "## net.core.somaxconn"
sysctl net.core.somaxconn || true

echo
echo "## Listening TCP sockets (ss -ltn)"
ss -ltn || true

echo
echo "## Interfaces (ip addr show)"
ip addr show || true

