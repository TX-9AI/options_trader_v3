#!/bin/bash
# =============================================================================
# install.sh — options_trader v3.0 Web Installer
# v1.0 — original release
# v2.0 — 2026-06-27 — updated repo URL to options_trader_v2
# v3.0 — 2026-07-10 — repo-wide v3.0 bump: Yahoo-Finance purge & data stream
#         mapping optimization (single shared TastyTrade candle feed). No
#         logic change in this file.
#
# Run on a fresh EC2:
#   curl -fsSL https://raw.githubusercontent.com/TX-9AI/options_trader_v2/main/install.sh -o install.sh && bash install.sh
# =============================================================================

set -e

REPO="https://github.com/TX-9AI/options_trader_v2.git"
DEPLOY_DIR="$HOME/options-trader-deploy"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║     options_trader v2.0  |  Web Installer           ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Install git if needed
sudo apt-get update -qq
sudo apt-get install -y -qq git

# Clone or update repo into deploy dir
if [ -d "$DEPLOY_DIR/.git" ]; then
    echo "  Updating existing repo..."
    cd "$DEPLOY_DIR" && git pull
else
    echo "  Cloning repository..."
    git clone "$REPO" "$DEPLOY_DIR"
fi

echo "  Repository ready."
echo ""

# Run setup from the deploy dir
chmod +x "$DEPLOY_DIR/setup_ec2.sh"
bash "$DEPLOY_DIR/setup_ec2.sh"
